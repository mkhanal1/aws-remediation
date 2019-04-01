## FAQ
  1. What permissions do Lambda functions need?
      - A role will be created for lambda function so that it can act on resources to remediate them. The list of permissions is mentioned in [lambdarole.yml](/Config/lambdarole.yml) file. This needs to be updated if a new module is added depending upon the remediation action.
  2. Can we add our own modules or change actions taken for current module?
      - Yes, you can build your own lambda functions against unsupported modules or add a different remediation action against the supported module. You will have to store it under [Remediation](/Remediation) folder for new module and edit the run function under the module for the new action.
  3. How will the new update/modules be cascaded to us?
      - This GitHub Readme will be updated with new modules in [Remediation](/Remediation) folder which can be imported under their Remediation folder in Lambda or customer can re run the CloudFormation template. The information about the change are added in [Release Notes](/Release_notes)
  4. How can we disable remediation for few controls?
      - Yes, you can Change the SSM Parameter named ControlsIdforRemediation to include only ControlIds for which you want remediation. For a single lambda accross multiple account , the disabled remediation for controls will be applicable for all accounts.
  5. How can we debug the issue related to the remediation functions?
      - You can look into the SNS message and Cloudwatch logs to debug further. The sample is provided [here](/Debug/Reademe.md).
