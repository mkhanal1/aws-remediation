"""
THIS SCRIPT IS PROVIDED TO YOU "AS IS." 
TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT. 
IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS.

Author: Mikesh Khanal
Created Date: 2018-11-11
Modified Date: 2019-01-31

Usage: This module will enable the CloudTrail across all regions. The default bucket will be named cloudtraillogs-accountId

"""

from __future__ import print_function
import boto3
import sys
import json

def action(boto_session,query,resourceId,region_name,accountId):
    debug_module = ["-------------------------\n"]
    print ("RESOURCE-ID: " + resourceId)
    debug_module.append("\n\n The resource " + resourceId + " in the region " + region_name + " in the account " + accountId + " fails the control evaluation.")
    s3 = boto_session.client('s3',region_name=region_name)
    client = boto_session.client('cloudtrail',region_name=region_name)
    bucket = "cloudtraillogs-" + accountId
    try:
        s3.head_bucket(Bucket=bucket)
    except:
        try:
            response = s3.create_bucket(Bucket=bucket,ACL='log-delivery-write')
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            if status_code > 400:
                debug_module.append("Bucket Could not be created!")
                debug_module.append(str(response))
            else:
                debug_module.append("Bucket created successfully")
                bucketpolicy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "AWSCloudTrailAclCheck20150319",
                            "Effect": "Allow",
                            "Principal": {"Service": "cloudtrail.amazonaws.com"},
                            "Action": "s3:GetBucketAcl",
                            "Resource": "arn:aws:s3:::" + bucket
                        },
                        {
                            "Sid": "AWSCloudTrailWrite20150319",
                            "Effect": "Allow",
                            "Principal": {"Service": "cloudtrail.amazonaws.com"},
                            "Action": "s3:PutObject",
                            "Resource": "arn:aws:s3:::" + bucket + "/AWSLogs/" + accountId + "/*",
                            "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
                        }
                    ]
                }
                response2 = s3.put_bucket_policy(
                    Bucket=bucket,
                    ConfirmRemoveSelfBucketAccess=False,
                    Policy=json.dumps(bucketpolicy)
                )
        except Exception as e:
            debug_module.append("Error:{}".format(e))
    try:
        response = client.create_trail(
            Name='Global-trail',
            S3BucketName=bucket,
            IncludeGlobalServiceEvents=True,
            IsMultiRegionTrail=True,
            EnableLogFileValidation=True
        )
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code > 400:
            debug_module.append("Trail could not be created!")
            debug_module.append(str(response))
        else:
            debug_module.append("Trail created successfully")
            try:
                response1 = client.start_logging(
                    Name=response['TrailARN']
                )
                status_code1 = response1['ResponseMetadata']['HTTPStatusCode']
                if status_code > 400:
                    debug_module.append("The recording of AWS API calls and log file delivery for a Global-trail could not be started!")
                    debug_module.append(str(response))
                else:
                    debug_module.append("Logging for Global-trail has started successfully")
            except Exception as e:
                debug_module.append("Error:{}".format(e))
    except Exception as e:
        debug_module.append("Error:{}".format(e))
    print (debug_module)
    return (debug_module)
