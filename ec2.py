import json
import boto3
from accounts import accounts

def build_ec2_json():
  ec2l = []
  for account in accounts:
    for region in account['regions']:
      try:
        access_id=account.get('aws_access_key_id')
        access_secret=account.get('aws_secret_access_key')
        ec2 = boto3.client('ec2',aws_access_key_id=access_id,aws_secret_access_key=access_secret,region_name=region)
      except Exception as e:
        print("Unable to connect, reason: {}".format(e))

      reservations = ec2.describe_instances().get('Reservations')
      for reservation in reservations:
        instances = reservation['Instances']
        for instance in instances:
          # id
          instance_id = instance.get('InstanceId')
          # name
          try:
            instance_name = get_tag_value(tags=instance.get('Tags'),key='Name')
          except:
            instance_name="N/A"
          # platfrom
          instance_platform = instance.get('Platform')
          # availability zone
          instance_az = instance.get('Placement').get('AvailabilityZone')
          # vpc
          instace_vpc = instance.get('VpcId')
          # subnet
          instance_subnet = instance.get('SubnetId')
          # ami
          instance_ami = instance.get('ImageId')
          # key name
          instance_keyName = instance.get('KeyName')
          # type
          instance_type = instance.get('InstanceType')
          # architecture
          instance_arch = instance.get('Architecture')
          # iam profile
          try:
            instance_profile = instance.get('IamInstanceProfile').get('Arn')
          except:
            instance_profile="N/A"
          # private dns name
          instance_privateDNS = instance.get('PrivateDnsName')
          # private ip address
          instance_privateIP = instance.get('PrivateIpAddress')
          # public dns name
          try:
            instance_publicDNS = instance.get('PublicDnsName')
          except:
            instance_publicDNS="N/A"
          # public ip address
          try:
            instance_publicIP = instance.get('PublicIpAddress')
          except:
            instance_publicIP="N/A"
          # security groups
          secGrp_details = instance.get('SecurityGroups')
          for secGrp in secGrp_details:
            instance_secGrp = secGrp.get('GroupId')
          # volumes
          device_mappings = instance.get('BlockDeviceMappings')
          for mapping in device_mappings:
            instance_volumeId = mapping['Ebs'].get('VolumeId')

          ec2d = {
                   'account': account['name'],
                   'region': region,
                   'instance_az': instance_az,
                   'instance_id': instance_id,
                   'instance_platform': instance_platform,
                   'instace_vpc': instace_vpc,
                   'instance_subnet': instance_subnet,
                   'instance_ami': instance_ami,
                   'instance_type': instance_type,
                   'instance_arch': instance_arch,
                   'instance_keyName': instance_keyName,
                   'instance_secGrp': instance_secGrp,
                   'instance_volumeId': instance_volumeId,
                   'instance_profile': instance_profile,
                   'instance_privateDNS': instance_privateDNS,
                   'instance_privateIP': instance_privateIP,
                   'instance_publicDNS': instance_publicDNS,
                   'instance_publicIP': instance_publicIP
                 }
                    
      ec2l.append(ec2d)

    with open('data/ec2.json', 'w') as f:
      json.dump(ec2l, f, indent=4)
      print("All done with building EC2 info...")

if __name__ == "__main__":
  build_ec2_json()
