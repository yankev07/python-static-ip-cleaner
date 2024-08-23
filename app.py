# Importing regular python libraries
import os
import glob
import logging
import requests

# Flask and Google Cloud Libraries
from flask import Flask, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Methods from the api.py file
from api.api import list_regions
from api.api import get_project_id
from api.api import list_ip_addresses

# Defining the Flask app and logger
app = Flask(__name__)
logger = logging.getLogger(__name__)


#`@app` is a Python decorator that Flask provides to bind a function to a URL.
@app.route('/', methods=['GET'])
# The function below is the function that will be executed when the URL is hit
def index():
    deleted_ips_list = []
    service_acct_files = glob.glob("service_acct/*.json")

    # Looping through the service account files (in case we have multiple service accounts)
    for service_acct_json in service_acct_files:
        print('Cleaning static IPs in project: ', service_acct_json.split('/')[1].split('.')[0])
        #`get_project_id` is a function that returns the project ID from the service account JSON file
        project = get_project_id(service_acct_json)
        #`service_account.Credentials.from_service_account_file` is a method from the google.oauth2 library that creates a credential
        credentials = service_account.Credentials.from_service_account_file(service_acct_json)
        #`build` is a method from the googleapiclient.discovery library that creates a service object
        compute = build('compute', 'v1', credentials=credentials)
        regions_list = list_regions(compute, project)
        # Looping through the regions in the project
        for i in range(len(regions_list)):
            #`list_ip_addresses` is a function that returns the list of static IPs in a region
            ip_list = list_ip_addresses(compute, project, regions_list[i])
            # Appending the list of IPs to the `deleted_ips_list`
            if ip_list is not None:
                deleted_ips_list.extend(ip_list)
                print(str(len(ip_list)) + ' Static IP addresses found in region: ', regions_list[i])
    # Removing duplicate IPs from the list
    cleaned_ip_list = list(set(deleted_ips_list))
    print("Process Compteted..")
    # Returning the cleaned list of IPs as a JSON response
    return jsonify(cleaned_ip_list)


# The code below is executed if the file is run as a script
if __name__ == '__main__':
    # Running the Flask app on port 5000
    app.run(host="0.0.0.0", port=3000, debug=True)