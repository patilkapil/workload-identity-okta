import json
import os

import requests
from google.auth import identity_pool
from google.cloud import storage
import base64


def list_buckets(project, scoped_credentials):
    """Lists all bucket accepts project and scoped credentials as an inputs
       Module will create a storage client and will be used to list all buckets
       storage client will read the buckets and will print the results """
    print("Calling Google Cloud Storage APIs")
    storage_client = storage.Client(
        project=project, credentials=scoped_credentials)
    #Get all the GCS bucket names
    buckets = storage_client.list_buckets()
    #Printing buckets
    for bucket in buckets:
        print(bucket.name)


def get_okta_token():
    '''
    Get Token Funtion is called from the main method
    Function is used to make authenticate application against the Okta Server
    Post successful authentication, application will reqest for the access token and save the token as a temp file
    :return: A temporary JSON File on your local machine
    '''

    cookies = {
        'JSESSIONID': '<Random Session ID>',
    }

    #Client ID and Client Secret from Okta's application configuration section
    client_id = "<Client ID from Okta>"
    client_secret = "<Client Secret from Okta>"
    # Encode data into base 64
    encodedData = base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii")

    # Headers to make a reuest to receive access tokens
    headers = {
        'Accept': '*/*',
        'Authorization': 'Basic '+encodedData,
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # Grant type credentials as this is a machine to machine interactions
    data = {
        'grant_type': 'client_credentials'
    }

    # Make a request to an Okta APi endpoint
    response = requests.post('https://<okta tenant url>/oauth2/aus24shs6sBqXzX8O1d7/v1/token',
                             headers=headers, cookies=cookies, data=data)
    response.raise_for_status()
    print("Creating Okta token file")
    data = response.json()
    print('JWT token')
    print(data)
    # Create a file and dump the token response into a Okta-token file
    with open('okta-token.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



if __name__ == '__main__':
    print("Running main")
    # Call get Okta token function to create a token
    get_okta_token()
    # For service account credentials open the file and load the configs
    file = open('client-config.json')
    json_config_info = json.loads(file.read())
    # Define the scope required
    scopes = ['https://www.googleapis.com/auth/devstorage.read_only']
    # Generate Credentials from the config file
    credentials = identity_pool.Credentials.from_info(json_config_info)
    # Create a scope credentials
    scoped_credentials = credentials.with_scopes(scopes)
    # GCP project name
    project = '<GCP Project ID>'
    # Call list bucket function with scoped credentials
    list_buckets(project, scoped_credentials)
    print("Removing Okta token file")
    os.remove('okta-token.json')