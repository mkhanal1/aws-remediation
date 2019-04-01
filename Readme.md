# Auto Remediation of AWS Controls
Auto remediation of resources failed against the Controls specified in Qualys CloudView

## License
_**THIS SCRIPT IS PROVIDED TO YOU "AS IS."  TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT.  IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS**_

## Table of Contents
Here's an overview of this repository and how they map to different sections:

<table style="text-align:center width:100%" align="center" >
  <tr>
    <th rowspan="3" width="20%"> 
    	Understand  <br> 
    	<a href="#Description">Description </a>
	<a href="#Different-Deployment-Modes">Deployment Options</a>
	 </th>
    <th width="60%">
    	<span style="font-weight:bold">Deploy</span> <br> 
    	<a href="#Usage">Usage, </a>
    	<a href="/Remediation/Readme.md">Modules Per ControlIDs, </a>
	<a href="/Release_notes">Release Notes</a>
    </th>
    <th width="20%" colspan="3" rowspan="3">FAQ & Logging
    	<a href="/Debug/Readme.md">Debugging, </a>
	<a href="#FAQ">FAQs</a>
</th>
  </tr>
    <td align="center" width="60%">
    	<span style="font-weight:bold">Add Module or Action</span><br> 	    
    	<a href="#Controls-supported-and-proposed-remediations-against-them">ControlIds, Remediation and Actions,</a>
	<a href="/Advanced/Readme.md">Addition of New Module or Action</a>
    </td>
  </tr>
</table>


## Description
This Cloudformation Template deploys a lambda function and subsequent modules against each controls.

It deploys ==>

  1. **A main lambda function and associated role** 
  2. **ControlID remediation modules**
  3. **A CloudWatch Event and permission to invoke lambda**
  4. **A output SNS Topic and associated sns policy**

## Different Deployment Modes

* **A lambda function per account**: 
   * A single lambda function with subsequent modules per account. 
   * Disabling remediation of control per account is possible.
![](/Images/RemediationSingleAccountModeV2.png?raw=true)

   > * _How does this deployment work?_
   
        1. The main lambda  will make an API call to Qualys CloudView API to list all the failed controls for the account.
        2. Based on the control id, the remediation module will be called.
        3. The module, if present, will take the remediation action specified in the table below.
        4. The module will send the logs to main lambda, which sends it to Output SNS topic.
        5. The SNS topic, if subscribed, will send information to email or slack channel.

* **A lambda function across multiple accounts**: 
  * A single lambda function with subsequent modules for all your accounts. 
  * Disabling remediation of control per account is not possible; it will be effective for all accounts.
 
![Images](/Images/RemediationMultiAccountModeV2.png?raw=true)

   > * _Prerequisites_
   
     - [ ] A new cross account role must be created in sub accounts for the base account.
     - [ ] The role must have similar permissions as the one assigned to the role associated with lambda of base account.
     - [ ] Input that role in input parameters of Cloudformation template.
  
   > * _How does this deployment work?_
   
        1. The main lambda  will make an API call to Qualys CloudView API to list all the failed controls for the account.
        2. It will verify if the account id mentioned in alert is same as the one where lambda function resides.
        3. If different, it will try to assume a role mentioned by customer during input parameters.
        4. if success, STS will return credentials/keys to assume that role for a specified period.
        5. A session is created and Based on the control id, the remediation module will be called and that session will be passed as input.
        6. The module, if present, will take the remediation action specified in the table below.
        7. The module will send the logs to main lambda, which sends it to Output SNS topic.
        8. The SNS topic, if subscribed, will send information to email or slack channel.



## Usage

#### Get started and deploy this into your AWS account
You can launch this CloudFormation stack in the US East 1 (North Virginia) Region in your account 
[![Launch Stack](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=QualysRemediation&templateURL=https://s3.amazonaws.com/my-great-stack.json)

It needs following input parameters:( An example file enlisting parameters is [here](/Config/parameters.yml).)

  * **QualysUsername:** Qualys username to call CloudView API to download the evaluation results
  * **QualysPassword:** Qualys password to call CloudView API to download the evaluation results
  * **QualysBaseUrl:** Qualys baseurl to download the evaluation results
  * **RemediationFrequency:** Frequency for setting up remediation of Controls. [For proper syntax, check this link.](https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html)
  * **EmailAddress:** email address for receiving logs about resources affected by controls being remediated
  * **SlackChannelWebHook:** Webhook to post logs in Slack channel
  * **AccountList:** comma delimeted list of accounts
  * **ControlsIdforRemediation:** ControlId for which you want to enable remediation
