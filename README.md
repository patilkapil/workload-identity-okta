# workload-identity-okta
Integrating GCP's Workload Identity and Okta as an IDP



The provided code sample demonstrates how to integrate Okta as an OIDC provider and integrate with GCP's workload identity federation. 

Prerequisite : 

Before running the code please complete the following setup. 

1- Create an application integration in Okta ; Refer : https://help.okta.com/en/prod/Content/Topics/Apps/Apps_App_Integration_Wizard.htm

2- Create an Authorization Server in Okta ; Refer : https://developer.okta.com/docs/guides/customize-authz-server/main/#create-an-authorization-server

3- Setup Workload Identity in GCP's IAM service ; Refer : https://cloud.google.com/iam/docs/configuring-workload-identity-federation

4- Setup Okta as an OIDC Provider ; Refer : https://cloud.google.com/iam/docs/configuring-workload-identity-federation

5- Create a service account and assign GCP's role ( Workload Identity User  & Service Account Token Creator) ; Refer: https://cloud.google.com/iam/docs/creating-managing-service-accounts

6- Assign the service account to OIDC provider ; Refer: https://cloud.google.com/iam/docs/creating-managing-service-accounts

7- Bind IAM policy to the service account ; Refer: https://cloud.google.com/iam/docs/creating-managing-service-accounts


# Python Dependencies

Install the extension dependencies locally.

```
$ pip3 install -r requirements.txt  
```

# client-config.json 

In the code you will notice client-config.json file. This is a config file used by GCP to support  OIDC ID tokens retrieval from a local file . 

```
{
  "type": "external_account",
  "audience": "//iam.googleapis.com/projects/<projectID>/locations/global/workloadIdentityPools/<workloadIdentityPoolID>/providers/<workloadIdentity-OIDCProvider>",
  "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
  "token_url": "https://sts.googleapis.com/v1/token",
  "service_account_impersonation_url": "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/<service-account-name>:generateAccessToken",
  "credential_source": {
    "file": "okta-token.json",
    "format": {
      "type": "json",
      "subject_token_field_name": "access_token"

    }
  }
}
```

# okta-token.json

Code runs the get_Okta function to retrieve Okta's Access Token and store in a file okta-token.json as a temporary file. At the end of the execution this temporary file will be deleted.

 
 # Key Considerations

Code is created for POC/introduction purposes only. For demonstration purposes, I have used hard-coded values. Please refer to Python's best programming practice if you reuse the code.  
