"""
THIS SCRIPT IS PROVIDED TO YOU "AS IS." 
TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT. 
IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS.

Author: Mikesh Khanal
Created Date: 2018-11-11
Modified Date: 2019-01-31

Usage: This module will enable access logging for the affected buckets. The logging bucket will be named "s3sccesslogs-regionaccountId"

"""

from __future__ import print_function
import boto3
import sys

def action(boto_session,query,resourceId,region_name,accountId):
    debug_module = ["-------------------------\n"]
    print ("RESOURCE-ID: " + resourceId)
    debug_module.append("\n\n The resource " + resourceId + " in the region " + region_name + " in the account " + accountId + " fails the control evaluation.")
    bucket_name = resourceId
    s3 = boto_session.client('s3',region_name=region_name)
    bucket = "s3sccesslogs-" + region_name + accountId
    try:
        s3.head_bucket(Bucket=bucket)
    except:
        try:
            if region_name == "us-east-1":
                region = ""
            elif region_name == "eu-west-1":
                region = "EU"
            else:
                region = region_name
            print ("REGION is: " + region)    
            response = s3.create_bucket(Bucket=bucket,ACL='log-delivery-write',CreateBucketConfiguration={'LocationConstraint': region})
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            if status_code > 400:
                debug_module.append("Bucket Could not be created!")
                debug_module.append(str(response))
            else:
                debug_module.append("Bucket created successfully")
        except Exception as e:
            debug_module.append("Error:{}".format(e))
    try:
        response = s3.put_bucket_logging(Bucket=bucket_name,
            BucketLoggingStatus={'LoggingEnabled': {'TargetBucket': bucket,'TargetPrefix': ''}})
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code > 400:
            debug_module.append("Bucket logging could not be set!")
            debug_module.append(str(response))
        else:
                debug_module.append("Bucket logging enabled successfully")    	   
    except Exception as e:
        debug_module.append("Error:{}".format(e))
    print (debug_module)
    return (debug_module)
