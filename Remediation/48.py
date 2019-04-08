"""
THIS SCRIPT IS PROVIDED TO YOU "AS IS." 
TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT. 
IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS.

Author: Mikesh Khanal
Created Date: 2018-11-11
Modified Date: 2019-01-31

Usage: This module will enable versioning for the affected bucket.

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
    try:
        response = s3.put_bucket_versioning(Bucket=bucket_name,VersioningConfiguration={'Status': 'Enabled'})
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
