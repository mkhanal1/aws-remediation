"""
THIS SCRIPT IS PROVIDED TO YOU "AS IS." 
TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT. 
IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS.

Author: Mikesh Khanal
Created Date: 2018-11-11
Modified Date: 2019-01-31

Usage: This module will enable Auto minor version upgrade for the affected RDS.

"""

from __future__ import print_function
import boto3
import sys
import json

def action(boto_session,query,resourceId,region_name,accountId):
    debug_module = ["-------------------------\n"]
    print ("RESOURCE-ID: " + resourceId)
    debug_module.append("\n\n The resource " + resourceId + " in the region " + region_name + " in the account " + accountId + " fails the control evaluation.")
    client = boto_session.client('rds',region_name=region_name)
    try:
        response = client.modify_db_instance(
            DBInstanceIdentifier=resourceId,
            AutoMinorVersionUpgrade=True,
            ApplyImmediately=True
        )
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code > 400:
            debug_module.append("Auto minor version upgrade could not be enabled!")
            debug_module.append(str(response))
        else:
            debug_module.append("Auto minor version upgrade enabled successfully")
    except Exception as e:
        debug_module.append("Error:{}".format(e))
    print (debug_module)
    return (debug_module)
