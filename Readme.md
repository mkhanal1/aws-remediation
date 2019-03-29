# Auto Remediation of AWS Controls
Auto remediation of resources failed against the Controls specified in Qualys CloudView

[![Launch Stack](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=QualysRemediation&templateURL=https://s3.amazonaws.com/my-great-stack.json)

## License
_**THIS SCRIPT IS PROVIDED TO YOU "AS IS."  TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT.  IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS**_

## Description
This Cloudformation Template deploys a lambda function and subsequent modules against each controls.

It deploys ==>

  1. **A main lambda function and associated role** 
  2. **ControlID remediation modules**
  3. **A CloudWatch Event and permission to invoke lambda**
  4. **A output SNS Topic and associated sns policy**

## Different Deployment Modes

* **Single Account Mode**: 
   * A single lambda function with subsequent modules per account. 
   * Disabling remediation of control per account is possible.
![](/Images/RemediationSingleAccountModeV2.png?raw=true)

   > * _How does single account mode works?_
   
        1. The main lambda  will make an API call to Qualys CloudView API to list all the failed controls for the account.
        2. Based on the control id, the remediation module will be called.
        3. The module, if present, will take the remediation action specified in the table below.
        4. The module will send the logs to main lambda, which sends it to Output SNS topic.
        5. The SNS topic, if subscribed, will send information to email or slack channel.

* **Multiple Account Mode**: 
  * A lambda function with subsequent modules for all your accounts. 
  * Disabling remediation of control per account is not possible; it will be effective for all accounts.
 
![Images](/Images/RemediationMultiAccountModeV2.png?raw=true)

   > * _Prerequisites for Multiple account mode_
   
     - [ ] A new cross account role must be created in sub accounts for the base account.
     - [ ] The role must have similar permissions as the one assigned to the role associated with lambda of base account.
     - [ ] Input that role in input parameters of Cloudformation template.
  
   > * _How does multi account mode works?_
   
        1. The main lambda  will make an API call to Qualys CloudView API to list all the failed controls for the account.
        2. It will verify if the account id mentioned in alert is same as the one where lambda function resides.
        3. If different, it will try to assume a role mentioned by customer during input parameters.
        4. if success, STS will return credentials/keys to assume that role for a specified period.
        5. A session is created and Based on the control id, the remediation module will be called and that session will be passed as input.
        6. The module, if present, will take the remediation action specified in the table below.
        7. The module will send the logs to main lambda, which sends it to Output SNS topic.
        8. The SNS topic, if subscribed, will send information to email or slack channel.

## Controls supported and proposed remediations against them
CID	|	CONTROL NAME	|	SERVICE	|	Remediation|
----| --------------|---------|------------|
[19](/Remediation/19.py)	|	 Ensure CloudTrail is enabled in all regions 	|	CLOUD_TRAIL	|	Enable CloudTrail |
[20](/Remediation/20.py)	|	Ensure CloudTrail log file validation is enabled	|	CLOUD_TRAIL	|	Enable CloudTrail log file validation |
[23](/Remediation/23.py)	|	Ensure AWS Config is enabled in all regions	|	CONFIG	|	Enable Config |
[41](/Remediation/41.py)	|	Ensure no security groups allow ingress from 0.0.0.0/0 to port 22	|	VPC	|	Remove rule containing port 22 from security group |
[42](/Remediation/42.py)	|	Ensure no security groups allow ingress from 0.0.0.0/0 to port 3389	|	VPC	|	Remove rule containing port 3389 from security group |
[43](/Remediation/43.py)	|	Ensure VPC flow logging is enabled in all VPCs	|	VPC	|	Enable VPC flow logging |
[44](/Remediation/44.py)	|	Ensure the default security group of every VPC restricts all traffic	|	VPC	|	Remove all inbound rules from default security group |
[45](/Remediation/45.py)	|	S3 Bucket Access Control List Grant Access to Everyone or Authenticated Users	|	S3	|	yes |
[46](/Remediation/46.py)	|	Ensure S3 Bucket Policy does not allow anonymous (public) access to S3 bucket	|	S3	|	yes |
[47](/Remediation/47.py)	|	Ensure access logging is enabled for S3 buckets	|	S3	|	Enable access logging |
[48](/Remediation/48.py)	|	Ensure versioning is enabled for S3 buckets	|	S3	|	Enable versioning |
[51](/Remediation/51.py)	|	Ensure that Public Accessibility is set to No for Database Instances	|	RDS	|	Disable public accessibility for RDS instances |
[52](/Remediation/52.py)	|	Ensure DB snapshot is not publicly visible	|	RDS	|	Disable public visibility of DB snapshot |
[53](/Remediation/53.py)	|	Ensure Encryption is enabled for the database Instance	|	RDS	|	Enable encryption |
[54](/Remediation/54.py)	|	Ensure database Instance snapshot is encrypted	|	RDS	|	Enable encryption |
[55](/Remediation/55.py)	|	Ensure auto minor version upgrade is enabled for a Database Instance	|	RDS	|	yes |
[56](/Remediation/56.py)	|	Ensure database Instance is not listening on to a standard/default port	|	RDS	|	yes |
[57](/Remediation/57.py)	|	Ensure that bucket policy enforces encryption in transit	|	S3	|	Enable encryption |

## Usage
[![Launch Stack](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=QualysRemediation&templateURL=https://s3.amazonaws.com/my-great-stack.json)

It needs following input parameters:( An example file enlisting parameters is [here](/Config/parameters.json).)

  * **QualysUsername:** Qualys username to call CloudView API to download the evaluation results
  * **QualysPassword:** Qualys password to call CloudView API to download the evaluation results
  * **QualysBaseUrl:** Qualys baseurl to download the evaluation results
  * **RemediationFrequency:** Frequency for setting up remediation of Controls. [For proper syntax, check this link.](https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html)
  * **EmailAddress:** email address for receiving logs about resources affected by controls being remediated
  * **SlackChannelWebHook:** Webhook to post logs in Slack channel
  * **Mode:** single or multiple account mode
  * **AccountList:** comma delimeted list of accounts



## FAQ
  1. Do we need to provide extra permissions to already existing Qualys role?
      - No. However, a new role will be created for lambda function so that it can act on resources to remediate them. The list of permissions is mentioned in [lambdarole.json](/Config/lambdarole.json) file.
  2. Can we add our own modules?
      - Yes, we can build your own lambda functions against unsupported modules or build a different remediation action against the supported module. You will have to store it under [Remediation](/Remediation) folder.
  3. How will the new update/modules be cascaded to us?
      - This GitHub Readme will be updated with new modules which can be imported under [Remediation](/Remediation) folder or customer can re run the CloudFormation template.
  4. How can we disable remediation for few controls?
      - Yes, you can disable remediation for controls. For multiple account mode, the disabled remediation for controls will be applicable for all accounts.
