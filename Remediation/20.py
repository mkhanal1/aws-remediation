"""
THIS SCRIPT IS PROVIDED TO YOU "AS IS." 
TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT. 
IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS.

Author: Mikesh Khanal
Created Date: 2018-11-11
Modified Date: 2019-01-31

Usage: This module will enable the log file validation for all the affected Trails.

"""

from __future__ import print_function
import boto3
import sys
import json

def action(boto_session,query,resourceId,region_name,accountId):
    debug_module = ["-------------------------\n"]
    print ("RESOURCE-ID: " + resourceId)
    debug_module.append("\n\n The resource " + resourceId + " in the region " + region_name + " in the account " + accountId + " fails the control evaluation.")
    client = boto_session.client('cloudtrail',region_name=region_name)
    try:
        response = client.update_trail(
            Name=resourceId,
            EnableLogFileValidation=True
        )
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code > 400:
            debug_module.append("Trail could not be updated to enable log file validation!")
            debug_module.append(str(response))
        else:
            debug_module.append("Trail was updated successfully and enabled for log file validation")
    except Exception as e:
        debug_module.append("Error:{}".format(e))
    print (debug_module)
    return (debug_module)
