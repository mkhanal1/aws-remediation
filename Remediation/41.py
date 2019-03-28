"""
THIS SCRIPT IS PROVIDED TO YOU "AS IS." 
TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT. 
IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS.

Author: Mikesh Khanal
Created Date: 2018-11-11
Modified Date: 2019-01-31

Usage: This module will remove the security group

"""

from __future__ import print_function
import boto3
import sys
import re

def action(query,resourceId,region_name,accountId):
	debug_module = ["-------------------------\n"]
	debug_module.append("\n\n The Security Group " + resourceId + " in the region " + region_name + " in the account " + accountId + " fails the control evaluation. It consists of")
	for j in range(len(query)-1):
		PortID=(query[j+1]['actualValue'])[6:]
		Cidr=(query[j+1]['settingName'])[9:]
		if ( (query[j+1]['actualValue']) != 'All' ):
			try:
				match  = re.findall(r'[^\s-]+', PortID)
				fromPort=(match[0])
				toPort=(match[1])
				protocol="tcp"
			except:
				fromPort=(match[0])
				toPort=fromPort
				protocol="tcp"
		else:
			fromPort=''
			toPort=''
			protocol="-1"
		debug_module.append("Source IP address: " + Cidr + " Port Range: " + fromPort + " - " + toPort)
		debug_module.append("* Removing the faulty security group " + resourceId )
		ec2 = boto3.resource('ec2',region_name=region_name)
		sg = ec2.SecurityGroup(resourceId)
		debug_module.append('\nThe Security Group input by the user is ' +resourceId)
		if ("::/0" in Cidr):
			if (fromPort != '' or toPort != ''):
				try:
					sg.revoke_ingress(IpPermissions=[{'FromPort': int(fromPort),'IpProtocol': protocol,'Ipv6Ranges': [{'CidrIpv6': Cidr}], 'ToPort':int(toPort)}])
					debug_module.append('Rules containing Ports ranging from ' + fromPort + ' to ' + toPort + ' from source 0.0.0.0/0 has been removed from SecurityGroup' + resourceId)
				except Exception as f:
					print ('Some Error occurred for IPV6 : ' + str(f))
					return debug_module
			else:
				try:
					sg.revoke_ingress(IpPermissions=[{'IpProtocol': protocol,'Ipv6Ranges': [{'CidrIpv6': Cidr}]}])
					debug_module.append('Rules containing Ports any from from source ' + Cidr +  ' has been removed from SecurityGroup' + resourceId)
				except Exception as f:
					print ('Some Error occurred for non null IPV6 : ' + str(f))
					return debug_module
		else:
			if (fromPort != '' or toPort != ''):
				try:
					sg.revoke_ingress(IpProtocol=protocol, CidrIp=Cidr, ToPort=int(toPort), FromPort=int(fromPort))
					debug_module.append('Rules containing Ports ranging from ' + (fromPort) + ' to ' + (toPort) + ' from source 0.0.0.0/0 has been removed from SecurityGroup' + resourceId)
				except Exception as f:
					print ('Some Error occurred for IPV4 : ' + str(f))
					return debug_module
			else:
				try:
					sg.revoke_ingress(IpProtocol=protocol, CidrIp=Cidr)
					debug_module.append('Rules containing Ports any from source ' + Cidr + ' has been removed from SecurityGroup' + resourceId)
				except Exception as f:
					print ('Some Error occurred for non null IPV4 : ' + str(f))
					return debug_module
	return (debug_module)
