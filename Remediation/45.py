"""
THIS SCRIPT IS PROVIDED TO YOU "AS IS." 
TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT. 
IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS.

Author: Mikesh Khanal
Created Date: 2018-11-11
Modified Date: 2019-01-31

Usage: This module will remove public access granted for everyone via ACL for the affected buckets."

"""

from __future__ import print_function
import boto3
import json
import sys

def action(boto_session,query,resourceId,region_name,accountId):
    debug_module = ["-------------------------\n"]
    debug_module.append("\n\n The resource " + resourceId + " in the region " + region_name + " in the account " + accountId + " fails the control evaluation.")
    bucket_name = resourceId
    s3 = boto_session.client('s3',region_name=region_name)
    response1 = s3.get_bucket_acl(
        Bucket=resourceId
    )
    Grants = response1['Grants']
    for i in (range(len(Grants))):
        if (str(Grants[i]['Grantee']) in "{'Type': 'Group', 'URI': 'http://acs.amazonaws.com/groups/global/AllUsers'}"):
            j=i
    del Grants[j]
    try:
        print (Grants)
        response = s3.put_bucket_acl(
            Bucket=resourceId,
            AccessControlPolicy={
                 'Grants':Grants,
                 'Owner': response1['Owner']
            }
        )
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code > 400:
            debug_module.append("Access granted to everyone via ACL could not be removed!")
            debug_module.append(str(response))
        else:
            debug_module.append("Access granted to everyone via ACL removed successfully")
    except Exception as e:
        debug_module.append("Error:{}".format(e))
    print (debug_module)
    return (debug_module)
