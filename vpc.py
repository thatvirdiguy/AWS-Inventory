import json
import boto3
from accounts import accounts

def build_vpc_json():
  vpcl = []
  for account in accounts:
    for region in account['regions']:
      try:
        access_id=account.get('aws_access_key_id')
        access_secret=account.get('aws_secret_access_key')
        ec2 = boto3.client('ec2',aws_access_key_id=access_id,aws_secret_access_key=access_secret,region_name=region)
      except Exception as e:
        print("Unable to connect, reason: {}".format(e))

      vpcs = ec2.describe_vpcs()['Vpcs']

      for vpc in vpcs:
        # id
        vpc_id = vpc.get('VpcId')
        # cidr block
        vpc_cidr = vpc.get('CidrBlock')
        # is default?
        vpc_default = vpc.get('IsDefault')
        # subnets
        vpc_subnets=[]
        subnet_details = ec2.describe_subnets(Filters=[{'Name': 'vpc-id','Values': [vpc_id]}])['Subnets']
        for subnet in subnet_details:
        # id
          subnet_id = subnet.get('SubnetId')
        # availability zone
          subnet_az = subnet.get('AvailabilityZone')
        # cidr block
          subnet_cidr = subnet.get('CidrBlock')
          subnet = {
                     'subnet_id': subnet_id,
                     'subnet_az': subnet_az,
                     'subnet_cidr': subnet_cidr
                   }
          vpc_subnets.append(subnet)
        # endpoint connections
        vpc_endpoints=[]
        try:
          endpoint_details = ec2.describe_vpc_endpoints(Filters=[{'Name': 'vpc-id','Values': [vpc_id]}])['VpcEndpoints']
          for endpoint in endpoint_details:
            vpc_endpointType = endpoint.get('VpcEndpointType')
            vpc_endpointServiceName = endpoint.get('ServiceName')
            endpoint = {
                         'vpc_endpointType': vpc_endpointType,
                         'vpc_endpointServiceName': vpc_endpointServiceName
                       }
            vpc_endpoints.append(endpoint)
        except:
          vpc_endpoints = {
                            'vpc_endpointType': 'N/A',
                            'vpc_endpointServiceName': 'N/A'
                          }
        # peering connections
        vpc_peerings=[]
        try:
          peering_details = ec2.describe_vpc_peering_connections(Filters=[{'Name': 'accepter-vpc-info.vpc-id','Values': [vpc_id]}])['VpcPeeringConnections']
          if peering_details == "[]":
            peering_details = ec2.describe_vpc_peering_connections(Filters=[{'Name': 'requester-vpc-info.vpc-id','Values': [vpc_id]}])['VpcPeeringConnections']
          for peering in peering_details:
            vpc_peeringAccepterCidr = peering['AccepterVpcInfo'].get('CidrBlock')
            vpc_peeringAccepterOwnerId = peering['AccepterVpcInfo'].get('OwnerId')
            vpc_peeringRequesterCidr = peering['RequesterVpcInfo'].get('CidrBlock')
            vpc_peeringRequesterCidr = peering['RequesterVpcInfo'].get('OwnerId')
            peering = {
                        'vpc_peeringAccepterCidr': vpc_peeringAccepterCidr,
                        'vpc_peeringAccepterOwnerId': vpc_peeringAccepterOwnerId,
                        'vpc_peeringRequesterCidr': vpc_peeringRequesterCidr,
                        'vpc_peeringRequesterCidr': vpc_peeringRequesterCidr
                      }
            vpc_peerings.append(peering)
        except:
          vpc_peerings = {
                           'vpc_peeringAccepterCidr': 'N/A',
                           'vpc_peeringAccepterOwnerId': 'N/A',
                           'vpc_peeringRequesterCidr': 'N/A',
                           'vpc_peeringRequesterCidr':'N/A'
                         }
        
        vpcd = {
                 'account': account['name'],
                 'region': region,
                 'vpc_id': vpc_id,
                 'vpc_cidr': vpc_cidr,
                 'vpc_default': vpc_default,
                 'vpc_subnets': vpc_subnets,
                 'vpc_endpoints': vpc_endpoints,
                 'vpc_peerings': vpc_peerings
               }

        vpcl.append(vpcd)

  with open('data/vpc.json', 'w') as f:
    json.dump(vpcl, f, indent=4)
    print("Done building VPC info...")

if __name__ == "__main__":
  build_vpc_json()
