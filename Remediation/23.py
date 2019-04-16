"""
THIS SCRIPT IS PROVIDED TO YOU "AS IS." 
TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT. 
IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS.

Author: Mikesh Khanal
Created Date: 2018-11-11
Modified Date: 2019-01-31

Usage: This module will enable the ConfigService across the affected regions.

"""

from __future__ import print_function
import boto3
import sys
import json

def action(boto_session,query,resourceId,region_name,accountId):
    debug_module = ["-------------------------\n"]
    debug_module.append("\n\n The resource " + resourceId + " in the region " + region_name + " in the account " + accountId + " fails the control evaluation.")
    region = []
    for i in query:
        if i['actualValue'] == "Disabled":
            region.append(i['settingName'])
    for j in region:
        region_name = str(j)
        bucket = "config-bucket" + accountId + region_name
        s3 = boto_session.client('s3',region_name=region_name)
        iam = boto_session.client('iam')
        client = boto_session.client('config',region_name=region_name)
        try:
            s3.head_bucket(Bucket=bucket)
        except:
            try:
                if region_name == "us-east-1":
                    response = s3.create_bucket(Bucket=bucket,ACL='log-delivery-write')
                elif region_name == "eu-west-1":
                    response = s3.create_bucket(Bucket=bucket,ACL='log-delivery-write',CreateBucketConfiguration={'LocationConstraint': "EU"})
                else:
                    response = s3.create_bucket(Bucket=bucket,ACL='log-delivery-write',CreateBucketConfiguration={'LocationConstraint': region_name})
                status_code = response['ResponseMetadata']['HTTPStatusCode']
                if status_code > 400:
                    debug_module.append("Bucket Could not be created!")
                    debug_module.append(str(response))
                else:
                    debug_module.append("Bucket created successfully")
            except Exception as e:
                debug_module.append("Error:{}".format(e))
        bucketpolicy = {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Sid": "AWSConfigBucketPermissionsCheck",
              "Effect": "Allow",
              "Principal": {
                "Service": [
                 "config.amazonaws.com"
                ]
              },
              "Action": "s3:GetBucketAcl",
              "Resource": "arn:aws:s3:::" + bucket 
            },
            {
              "Sid": "AWSConfigBucketDelivery",
              "Effect": "Allow",
              "Principal": {
                "Service": [
                 "config.amazonaws.com"    
                ]
              },
              "Action": "s3:PutObject",
              "Resource": "arn:aws:s3:::" + bucket + "/AWSLogs/" + accountId + "/Config/*",
              "Condition": { 
                "StringEquals": { 
                  "s3:x-amz-acl": "bucket-owner-full-control" 
                }
              }
            }
          ]
        }
        try:
            response2 = s3.put_bucket_policy(
                Bucket=bucket,
                ConfirmRemoveSelfBucketAccess=False,
                Policy=json.dumps(bucketpolicy)
            )
            debug_module.append("Bucket policy added successfully")
        except Exception as e:
            debug_module.append("Error:{}".format(e))
        try:
            assumerolepolicy = {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Sid": "",
                  "Effect": "Allow",
                  "Principal": {
                    "Service": "config.amazonaws.com"
                  },
                  "Action": "sts:AssumeRole"
                }
              ]
            }
            response1 = iam.create_role(
                RoleName='configrole',
                AssumeRolePolicyDocument=json.dumps(assumerolepolicy),
                Description='Config Role to collect data'
            )
            status_code1 = response1['ResponseMetadata']['HTTPStatusCode']
            print (response1['Error']['Code'])
            if status_code1 > 400 and response1['Error']['Code'] != "EntityAlreadyExists":
                debug_module.append("Role could not be created!")
                debug_module.append(str(response))
            else:
                debug_module.append("Role created successfully")
                try:
                    response3 = iam.attach_role_policy(
                        RoleName='configrole',
                        PolicyArn='arn:aws:iam::aws:policy/service-role/AWSConfigRole'
                    )
                    debug_module.append("Policy 'AWSConfigRole' attached!")
                except Exception as e:
                    debug_module.append("Error:{}".format(e))
        except Exception as e:
            debug_module.append("Error:{}".format(e))
            try:
                response = client.put_configuration_recorder(
                                ConfigurationRecorder={
                                    'name': 'config',
                                    'roleARN': "arn:aws:iam::" + accountId + ":role/configrole",
                                    'recordingGroup': {
                                        'allSupported': True,
                                        'includeGlobalResourceTypes': True,
                                    }
                                }
                            )
                status_code = response['ResponseMetadata']['HTTPStatusCode']
                if status_code > 400:
                    debug_module.append("Config Recorder could not be created!")
                    debug_module.append(str(response))
                else:
                    debug_module.append("Config Recorder created successfully")
                    try:
                        response4 = client.put_delivery_channel(
                            DeliveryChannel={
                                'name': 'default',
                                's3BucketName': bucket,
                                'configSnapshotDeliveryProperties': {
                                    'deliveryFrequency': 'One_Hour'
                                }
                            }
                        )
                        status_code4 = response4['ResponseMetadata']['HTTPStatusCode']
                        if status_code4 > 400:
                            debug_module.append("Delivery  channel  could not be created!")
                            debug_module.append(str(response))
                        else:
                            debug_module.append("Delivery  channel  created successfully") 
                            try:
                                response1 = client.start_configuration_recorder(
                                                ConfigurationRecorderName='config'
                                            )
                                status_code1 = response1['ResponseMetadata']['HTTPStatusCode']
                                if status_code > 400:
                                    debug_module.append("The config recording could not be started!")
                                    debug_module.append(str(response))
                                else:
                                    debug_module.append("Config Recording has started successfully")
                            except Exception as e:
                                debug_module.append("Error:{}".format(e))
                    except Exception as e:
                        debug_module.append("Error:{}".format(e))
            except Exception as e:
                debug_module.append("Error:{}".format(e))
    print (debug_module)
    return (debug_module)
