# Auto Remediation of AWS Controls
Auto remediation of resources failed against the Controls specified in Qualys CloudView

[![Launch Stack](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=QualysRemediation&templateURL=https://s3.amazonaws.com/my-great-stack.json)

## License
_**THIS SCRIPT IS PROVIDED TO YOU "AS IS."  TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT.  IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS**_

## Description
This Cloudformation Template deploys a lambda function and subsequent modules against each controls.

It needs following input parameters:

* **QualysUsername:** Qualys username to call CloudView API to download the evaluation results
* **QualysPassword:** Qualys password to call CloudView API to download the evaluation results
* **QualysBaseUrl:** Qualys baseurl to download the evaluation results
* **RemediationFrequency:** Frequency for setting up remediation of Controls. [For syntax, check](https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html)
* **EmailAddress:** email address for receiving logs about resources affected by controls being remediated
* **SlackChannelWebHook:** Webhook to post logs in Slack channel
* **Mode:** single or multiple account mode
* **AccountList:** comma delimeted list of accounts

It deploys

* A main lambda function and associated role 
* ControlID remediation modules
* A CloudWatch Event and permission to invoke lambda
* A output SNS Topic and associated sns policy

## Different Modes

* **Single Account Mode**: 
   * A single lambda function with subsequent modules per account. 
   * Disabling remediation of control per account is possible.
![](/Images/RemediationSingleAccountModeV2.png?raw=true)

* _How does single account mode works?_
    1. The main lambda  will make an API call to Qualys CloudView API to list all the failed controls for the account.
    2. Based on the control id, the remediation module will be called.
    3. The module, if present, will take the remediation action specified in the table below.
    4. The module will send the logs to main lambda, which sends it to Output SNS topic.
    5. The SNS topic, if subscribed, will send information to email or slack channel.

* **Multiple Account Mode**: 
  * A lambda function with subsequent modules for all your accounts. 
  * Disabling remediation of control per account is not possible; it will be effective for all accounts.
 
![Images](/Images/RemediationMultiAccountModeV2.png?raw=true)

* _Prerequisites for Multiple account mode_
   * A new cross account role must be created in sub accounts for the base account
   * The role must have similar permissions as the one assigned to the role associated with lambda of base account
   * Input that role in input parameters of Cloudformation template
  
* _How does multi account mode works?_

    1. The main lambda  will make an API call to Qualys CloudView API to list all the failed controls for the account.
    2. Based on the control id, the remediation module will be called.
    3. The module, if present, will take the remediation action specified in the table below.
    4. The module will send the logs to main lambda, which sends it to Output SNS topic.
    5. The SNS topic, if subscribed, will send information to email or slack channel.

## Controls supported and proposed remediations against them
CID	|	CONTROL NAME	|	SERVICE	|	Remediation|
----| --------------|---------|------------|
19	|	 Ensure CloudTrail is enabled in all regions 	|	CLOUD_TRAIL	|	Enable CloudTrail |
20	|	Ensure CloudTrail log file validation is enabled	|	CLOUD_TRAIL	|	Enable CloudTrail log file validation |
23	|	Ensure AWS Config is enabled in all regions	|	CONFIG	|	yes |
[41](/Remediation/41.py)	|	Ensure no security groups allow ingress from 0.0.0.0/0 to port 22	|	VPC	|	yes |
42	|	Ensure no security groups allow ingress from 0.0.0.0/0 to port 3389	|	VPC	|	yes |
43	|	Ensure VPC flow logging is enabled in all VPCs	|	VPC	|	yes |
44	|	Ensure the default security group of every VPC restricts all traffic	|	VPC	|	yes |
45	|	S3 Bucket Access Control List Grant Access to Everyone or Authenticated Users	|	S3	|	yes |
46	|	Ensure S3 Bucket Policy does not allow anonymous (public) access to S3 bucket	|	S3	|	yes |
47	|	Ensure access logging is enabled for S3 buckets	|	S3	|	yes |
48	|	Ensure versioning is enabled for S3 buckets	|	S3	|	yes |
51	|	Ensure that Public Accessibility is set to No for Database Instances	|	RDS	|	yes |
52	|	Ensure DB snapshot is not publicly visible	|	RDS	|	yes |
53	|	Ensure Encryption is enabled for the database Instance	|	RDS	|	yes |
54	|	Ensure database Instance snapshot is encrypted	|	RDS	|	yes |
55	|	Ensure auto minor version upgrade is enabled for a Database Instance	|	RDS	|	yes |
56	|	Ensure database Instance is not listening on to a standard/default port	|	RDS	|	yes |
57	|	Ensure that bucket policy enforces encryption in transit	|	S3	|	yes |

## Usage
[![Launch Stack](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=QualysRemediation&templateURL=https://s3.amazonaws.com/my-great-stack.json)

## FAQ
1. Do we need to provide extra permissions to already existing Qualys role?
2. Can we add our own modules?
3. How will the new update/modules be cascaded to us?
4. How can we disable remediation for few controls?
