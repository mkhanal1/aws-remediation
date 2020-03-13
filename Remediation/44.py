"""
THIS SCRIPT IS PROVIDED TO YOU "AS IS." 
TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT. 
IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS.

Author: Mikesh Khanal
Created Date: 2018-11-11
Modified Date: 2019-01-31

Usage: This module will remove all the rules from the default security group

"""

from __future__ import print_function
import boto3
import sys
import re

def action(boto_session,query,resourceId,region_name,accountId):
	debug_module = ["-------------------------\n"]
	debug_module.append("\n\n The Security Group " + resourceId + " in the region " + region_name + " in the account " + accountId + " fails the control evaluation. It consists of")
	ec2= boto_session.resource('ec2',region_name=region_name)
	sg = ec2.SecurityGroup(resourceId)
	sg_ingress = sg.ip_permissions
	#sg_egress = sg.ip_permissions_egress
	try:
		print ("The Inbound rules in security group:{} are {}\n".format(resourceId,sg_ingress))
		print ("The Outbound rules in security group:{} are {}\n".format(resourceId,sg_egress))
		print ("Removing all the Inbound rules from security group:()\n".format(resourceId))
		sg.revoke_ingress(IpPermissions=sg_ingress)
		print ("Removing all the Inbound rules from security group:()\n".format(resourceId))
		sg.revoke_egress(IpPermissions=sg_egress)
		debug_module.append("Both Inbound & Outbound Rules are removed")
	except Exception as e:
		debug_module.append("Error:{}".format(e))
	print (debug_module)
	return (debug_module)
