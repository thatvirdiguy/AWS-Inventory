import json
import boto3
from accounts import accounts

def build_iam_json():
  iaml = []
  for account in accounts:
    try:
      access_id=account.get('aws_access_key_id')
      access_secret=account.get('aws_secret_access_key')
      iam = boto3.client('iam',aws_access_key_id=access_id,aws_secret_access_key=access_secret)
    except Exception as e:
      print("Unable to connect, reason: {}".format(e))

    users = iam.list_users()['Users']

    for user in users:
      # name
      iam_username=user.get('UserName')
      # id
      iam_userid=user.get('UserId')
      # groups
      groups = iam.list_groups_for_user(UserName=iam_username)['Groups']
      iam_groups=[]
      for group in groups:
        iam_groupname=group.get('GroupName')
        iam_groupid=group.get('GroupId')
        iam_group = {
                     'iam_groupname': iam_groupname,
                     'iam_groupid': iam_groupid
                    }
        iam_groups.append(iam_group)
      # policies
      iam_policies = iam.list_user_policies(UserName=iam_username)['PolicyNames']
      
      iamd = { 
               'account': account,
               'iam_username': iam_username,
               'iam_userid': iam_userid,
               'iam_groups': iam_groups,
               'iam_policies': iam_policies
             }

      iaml.append(iamd)

  with open('data/iam.json', 'w') as f:
    json.dump(iaml, f, indent=4)
    print("Done building IAM info...")

if __name__ == "__main__":
  build_iam_json()
