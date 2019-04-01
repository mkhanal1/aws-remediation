## Debugging

> A sample SNS message
```
-------------------------------------------------
for 123456789123:
The Control 41 is sent for remediation 
	 sg-9876f5852ny580570 in ap-northeast-2 is being remediated 
	 sg-1234a4f682nyec8ee in ap-northeast-2 is being remediated 

for 987654321987:
The Control 41 is sent for remediation 
	 sg-gdj567sg in us-west-2 is being remediated 
	 sg-98gmn2s3 in us-east-1 is being remediated 
	 sg-0087987t0d30e6980 in us-east-1 is being remediated 
-------------------------------------------------
```
> A sample CloudWatch logs
```
START RequestId: 78jjfa82-4c2d-4efz-9cea-7d223a8e9f65 Version: $LATEST
[INFO]	2019-03-29T11:01:34.367Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Found credentials in environment variables.
[INFO]	2019-03-29T11:01:35.9Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Starting new HTTPS connection (1): ssm.ap-northeast-2.amazonaws.com
[INFO]	2019-03-29T11:01:35.489Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Starting new HTTPS connection (1): ssm.ap-northeast-2.amazonaws.com
[INFO]	2019-03-29T11:01:42.303Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Rule violation is found for: 41 

[INFO]	2019-03-29T11:01:42.303Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Found Remediation module 41 for resource sg-0144th55a6a580599, invoking it.
[INFO]	2019-03-29T11:01:42.303Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	[
{
    "settingName": "VPC Id",
    "actualValue": "vpc-98536k",
    "expectedValue": ""
}
,
{
    "settingName": "Network: 0.0.0.0/0",
    "actualValue": "Port : 22",
    "expectedValue": ""
}
,
{
    "settingName": "Network: ::/0",
    "actualValue": "Port : 22",
    "expectedValue": ""
}
]
[INFO]	2019-03-29T11:01:42.390Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Found credentials in environment variables.
[INFO]	2019-03-29T11:01:43.389Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Starting new HTTPS connection (1): ec2.ap-northeast-2.amazonaws.com
[INFO]	2019-03-29T11:01:43.968Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Starting new HTTPS connection (1): ec2.ap-northeast-2.amazonaws.com
[INFO]	2019-03-29T11:01:44.308Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	resource sg-0144th55a6a580599 is remediated against module 41
[INFO]	2019-03-29T11:01:44.308Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Found Remediation module 41 for resource sg-0349jk7g8a6aec8jj, invoking it.
[INFO]	2019-03-29T11:01:44.308Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	[
{
    "settingName": "VPC Id",
    "actualValue": "vpc-98536k",
    "expectedValue": ""
}
,
{
    "settingName": "Network: 0.0.0.0/0",
    "actualValue": "Port : 22",
    "expectedValue": ""
}
,
{
    "settingName": "Network: ::/0",
    "actualValue": "Port : 22",
    "expectedValue": ""
}
]
[INFO]	2019-03-29T11:01:44.430Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Starting new HTTPS connection (1): ec2.ap-northeast-2.amazonaws.com
[INFO]	2019-03-29T11:01:45.328Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Starting new HTTPS connection (1): ec2.ap-northeast-2.amazonaws.com
[INFO]	2019-03-29T11:01:45.667Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	resource sg-0349jk7g8a6aec8jj is remediated against module 41
[INFO]	2019-03-29T11:01:45.768Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Starting new HTTPS connection (1): sts.ap-northeast-2.amazonaws.com
[INFO]	2019-03-29T11:01:45.990Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Starting new HTTPS connection (1): ssm.ap-northeast-2.amazonaws.com
[INFO]	2019-03-29T11:01:52.182Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Rule violation is found for: 41 

[INFO]	2019-03-29T11:01:52.187Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Found Remediation module 41 for resource sg-d87765a6, invoking it.
[INFO]	2019-03-29T11:01:52.207Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	[
{
    "settingName": "VPC Id",
    "actualValue": "vpc-98545654",
    "expectedValue": ""
}
,
{
    "settingName": "Network: 0.0.0.0/0",
    "actualValue": "All",
    "expectedValue": ""
}
]
[INFO]	2019-03-29T11:01:52.929Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Starting new HTTPS connection (1): ec2.us-west-2.amazonaws.com
[INFO]	2019-03-29T11:01:53.878Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	resource sg-d87765a6 is remediated against module 41
[INFO]	2019-03-29T11:01:53.878Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Found Remediation module 41 for resource sg-cfxyz686, invoking it.
[INFO]	2019-03-29T11:01:53.907Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	[
{
    "settingName": "VPC Id",
    "actualValue": "vpc-cfxyz686",
    "expectedValue": ""
}
,
{
    "settingName": "Network: 0.0.0.0/0",
    "actualValue": "Port : 0-65535",
    "expectedValue": ""
}
]
[INFO]	2019-03-29T11:01:54.87Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Starting new HTTPS connection (1): ec2.us-east-1.amazonaws.com
[INFO]	2019-03-29T11:01:55.65Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	resource sg-cfxyz686 is remediated against module 41
[INFO]	2019-03-29T11:01:55.65Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Found Remediation module 41 for resource sg-008abcd90d30e6789, invoking it.
[INFO]	2019-03-29T11:01:55.65Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	
[
{
    "settingName": "VPC Id",
    "actualValue": "vpc-cfxyz686",
    "expectedValue": ""
}
,
{
    "settingName": "Network: 0.0.0.0/0",
    "actualValue": "Port : 0-65535",
    "expectedValue": ""
}
]
[INFO]	2019-03-29T11:01:55.227Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Starting new HTTPS connection (1): ec2.us-east-1.amazonaws.com
[INFO]	2019-03-29T11:01:56.524Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	resource sg-008abcd90d30e6789 is remediated against module 41
[INFO]	2019-03-29T11:01:56.650Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Starting new HTTPS connection (1): sns.ap-northeast-2.amazonaws.com
[INFO]	2019-03-29T11:01:56.884Z	78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	SNS message posted successfully
END RequestId: 78jjfa82-4c2d-4efz-9cea-7d223a8e9f65
REPORT RequestId: 78jjfa82-4c2d-4efz-9cea-7d223a8e9f65	Duration: 22689.49 ms	Billed Duration: 22700 ms Memory Size: 128 MB	Max Memory Used: 101 MB	
```
