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
