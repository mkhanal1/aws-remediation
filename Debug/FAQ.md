## FAQ
  1. Do we need to provide extra permissions to already existing Qualys role?
      - No. However, a new role will be created for lambda function so that it can act on resources to remediate them. The list of permissions is mentioned in [lambdarole.yml](/Config/lambdarole.yml) file.
  2. Can we add our own modules or actions?
      - Yes, we can build your own lambda functions against unsupported modules or add a different remediation action against the supported module. You will have to store it under [Remediation](/Remediation) folder for new module and edit the run function under the module for the new action.
  3. How will the new update/modules be cascaded to us?
      - This GitHub Readme will be updated with new modules which can be imported under [Remediation](/Remediation) folder or customer can re run the CloudFormation template. The information about the change in the new releases are added in [Release Notes](/Release_notes)
  4. How can we disable remediation for few controls?
      - Yes, you can disable remediation for controls. For multiple account mode, the disabled remediation for controls will be applicable for all accounts.
  5. How can we debug the issue related to the remediation functions?
      - You can look into the SNS message and Cloudwatch logs to debug further. The sample is provided [here](/Debug/Reademe.md).
