import json
import boto3

from ec2 import build_ec2_json
from vpc import build_vpc_json
from s3 import build_s3_json
from iam import build_iam_json

print("Collecting EC2 info...")
try:
  build_ec2_json()
except Exception as e:
  print("Unable to build json, reason: {}".format(e))

print("Collecting VPC info...")
try:
  build_vpc_json()
except Exception as e:
  print("Unable to build json, reason: {}".format(e))

print("Collecting S3 info...")
try:
  build_s3_json()
except Exception as e:
  print("Unable to build json, reason: {}".format(e))

print("Collecting IAM info...")
try:
  build_iam_json()
except Exception as e:
  print("Unable to build json, reason: {}".format(e))
