from botocore.exceptions import ClientError
import os
import json
import importlib
import logging
import boto3

# Set up Error Handling
class ControlsRemediationNotSupportedException(Exception): pass
class CouldNotLogintoQualys(Exception): pass

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
debug = []

#Post the alert.
def sendsns(OUTPUTTOPIC_ARN,debug): 
	debug.append("-------------------------------------------------\n")
	#turn it from an array to a string
	debugstr = ''.join((str(f) for f in debug))
	sns = boto3.client('sns')
	response = sns.publish(
		TopicArn=OUTPUTTOPIC_ARN,
		Message=debugstr,
		Subject='QualysRemediationLog',
		MessageStructure='string'
	)

	status_code = response['ResponseMetadata']['HTTPStatusCode']
	if status_code > 400:
		logger.info("SNS message failed to send!")
		logger.info(str(response))
	else:
		logger.info("SNS message posted successfully")

def takeaction(boto_session,alert_account_id,OUTPUTTOPIC_ARN):
	debug.append("\nfor {}:\n".format(alert_account_id))
	ssm = boto3.client('ssm')
	username = (ssm.get_parameter(Name='/Qualys/QualysUsername', WithDecryption=True))['Parameter']['Value']
	password = (ssm.get_parameter(Name='/Qualys/QualysPassword', WithDecryption=True))['Parameter']['Value']
	BASEURL = (ssm.get_parameter(Name='/Qualys/QualysBaseURL', WithDecryption=True))['Parameter']['Value']
	try:
	    kurl = 'curl -k -s -u {}:{} -H "X-Requested-With:Curl" -H "Accept: application/json" -X "GET"  "{}/cloudview-api/rest/1.5/aws/evaluations/{}"'.format(username, password,BASEURL,alert_account_id)
	    eval = os.popen(kurl).read()
	    evalcontent = json.loads(eval)['content']
	except Exception as e:
	    logger.error("Error: could not download the policy list for this account!!!")
	    debug.append("Error: could not download the policy list for this account!!!")
	    sendsns(OUTPUTTOPIC_ARN,debug)
	    raise CouldNotLogintoQualys("Error: could not download the policy list for this account!!!")
	controls = evalcontent [len(evalcontent)-1]['controlId']
	ControlIds = ((ssm.get_parameter(Name='/Qualys/ControlIds', WithDecryption=True))['Parameter']['Value']).split(',')
	for i in  range(1, int(controls)+1):
	    cid = str(i)
	    if cid in ControlIds:
	    	#print ("CIDS" + str(cid))
		    #rule_name = evalcontent[i]["controlName"]
		    try:
		        mod_modl = importlib.import_module('Remediation.' + cid, package=None)
		    except Exception as e:
		        logger.error ("Error:The Control {} is not supported or module could not be imported:{}. \n" .format(cid,e))
		        continue
		    try:
		        qurl = 'curl -k -s -u {}:{} -H "X-Requested-With:Curl" -H "Accept: application/json" -X "GET"  "{}/cloudview-api/rest/1.5/aws/evaluations/{}/resources/{}?filter=control.result%3A%20FAIL&pageNo=1&pageSize=100"'.format(username, password,BASEURL,alert_account_id,cid)
		        result = os.popen(qurl).read()
		        resourceevaluation = json.loads(result)
		        logger.info("Rule violation is found for: {} \n " .format(cid))
		    except Exception as e:
		        logger.error("Error: could not download the evaluation results for this account!!!")
		        debug.append("Error: could not download the evaluation results for this account!!!")
		        continue
		    count = len(resourceevaluation['content'])
		    debug.append ("The Control {} is sent for remediation \n" .format(cid))
		    for j in range(count):
		        resourcecontent = resourceevaluation['content'][j]['evidences']
		        alert_account_id = resourceevaluation['content'][j]['accountId']
		        resource = resourceevaluation['content'][j]['resourceId']
		        region = resourceevaluation['content'][j]["region"]
		        logger.info("Found Remediation module {} for resource {}, invoking it." .format(cid,resource))
		        logger.info ((json.dumps(resourcecontent)))
		        debug.append ("\t {} in {} is being remediated \n".format(resource,region))
		        ## Running the module
		        try:
		            module_run = mod_modl.action(boto_session,resourcecontent,resource,region,alert_account_id)
		            logger.info("resource {} is remediated against module {}".format(resource,cid))
		            #debug.append (module_run)
		        except Exception as e:
		            logger.error ("The Control {} is not functioning as expected:{} \n" .format(cid,e))
		            debug.append ("The Control {} is not functioning as expected \n" .format(cid))
		            continue

		
def lambda_handler(alert, context):
    debug.append("-------------------------------------------------\n")
    accountID = context.invoked_function_arn.split(":")[4]
    region = context.invoked_function_arn.split(":")[3]
    ssm = boto3.client('ssm')
    QualysRemediationRole = (ssm.get_parameter(Name='/Qualys/QualysRemediationRole', WithDecryption=True))['Parameter']['Value']
    accounts = ((ssm.get_parameter(Name='/Qualys/accounts', WithDecryption=True))['Parameter']['Value']).split(',')
    OUTPUTTOPIC_ARN = (ssm.get_parameter(Name='/Qualys/QualysOutputTopicArn', WithDecryption=True))['Parameter']['Value']
    for i in accounts:
        alert_account_id = i
        if int(accountID) != int(alert_account_id):
            role_arn = "arn:aws:iam::" + str(alert_account_id) + ":role/" + QualysRemediationRole
            sts_client = boto3.client('sts')
            try:
                assumed_role_object=sts_client.assume_role(RoleArn=role_arn,RoleSessionName="QualysRemediationRoleSession")
                credentials=assumed_role_object['Credentials']
                boto_session = boto3.Session(region_name=region,aws_access_key_id = credentials['AccessKeyId'],aws_secret_access_key = credentials['SecretAccessKey'],aws_session_token = credentials['SessionToken'])
                takeaction(boto_session,alert_account_id,OUTPUTTOPIC_ARN)
            except Exception as e:
                print (e)
                logger.error("Failed to assume QualysRemediationRole in {} account ".format(alert_account_id))
                debug.append("Failed to assume QualysRemediationRole in {} account ".format(alert_account_id))
                continue
        else:
        	boto_session = boto3.Session(region_name=region)
        	takeaction(boto_session,accountID,OUTPUTTOPIC_ARN)
    sendsns(OUTPUTTOPIC_ARN,debug)
