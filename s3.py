import json
import boto3
from accounts import accounts

def build_s3_json():
  bucketl = []
  for account in accounts:
    try:
      access_id=account.get('aws_access_key_id')
      access_secret=account.get('aws_secret_access_key')
      s3 = boto3.client('s3',aws_access_key_id=access_id,aws_secret_access_key=access_secret)
    except Exception as e:
      print("Unable to connect, reason: {}".format(e))

    buckets = s3.list_buckets()['Buckets']

    for bucket in buckets:
      # name
      bucket_name = bucket['Name']
      # location
      try:
        bucket_region = s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint']
      except:
        bucket_region="N/A"
      # encryption
      try:
        bucket_encryption = json.loads(s3.get_bucket_encryption(Bucket=bucket['Name'])['ServerSideEncryptionConfiguration']['Rules'][0])
      except:
        bucket_encryption="N/A"
      # policy
      try:
        bucket_policy = json.loads(s3.get_bucket_policy(Bucket=bucket['Name'])['Policy'])
      except:
        bucket_policy="N/A"
      # acl
      try:
        bucket_acl = json.loads(s3.get_bucket_acl(Bucket=bucket['Name']))['Grants']
      except:
        bucket_acl="N/A"
      # public access block
      try:
        bucket_access_block = s3.get_public_access_block(Bucket=bucket['Name'])['PublicAccessBlockConfiguration']
      except:
        bucket_access_block="N/A"
      # lifecycle
      try:
        bucket_lifecycle = json.loads(s3.get_bucket_lifecycle_configuration(Bucket=bucket['Name']))
      except:
        bucket_lifecycle="N/A"

      bucketd = {
                  'account': account['name'],
                  'region': bucket_region,
                  'bucket_name': bucket_name,
                  'bucket_encryption': bucket_encryption,
                  'bucket_policy': bucket_policy,
                  'bucket_acl': bucket_acl,
                  'bucket_access_block': bucket_access_block,
                  'bucket_lifecycle': bucket_lifecycle
                }
                    
      bucketl.append(bucketd)

  with open('data/s3.json', 'w') as f:
    json.dump(bucketl, f, indent=4)
    print("Done building S3 info...")

if __name__ == "__main__":
  build_s3_json()
