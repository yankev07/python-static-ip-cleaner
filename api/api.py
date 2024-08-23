import os
import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime, timedelta

# Defining variables
deleted_ip_list = []
missed_ip_list = []


# Method to get the project ID from the service account JSON file
def get_project_id(json_file_path):
    with open(json_file_path) as service_acct:
        data = json.load(service_acct)
    return data['project_id']


# Method to list the regions in a project
def list_regions(compute, project):
    regions_list = []
    request = compute.regions().list(project=project)
    while request is not None:
        response = request.execute()
        for region in response['items']:
            regions_list.append(region['name'])
        request = compute.regions().list_next(previous_request=request, previous_response=response)
    return regions_list


# Method to list the static IPs in a region
def list_ip_addresses(compute, project, region):
    # `compute.addresses().list` is a method from the googleapiclient.discovery library that lists the static IPs in a region
    request = compute.addresses().list(project=project, region=region)
    while request is not None:
        response = request.execute()
        # If the response is empty, return
        if len(response) <= 3:
            return
        # Looping through the IPs in the response
        for address in response['items']:
            # If the IP is external and reserved, append it to the `deleted_ip_list` (note that the IP is not actually deleted)
            if address['addressType'] == 'EXTERNAL' and address['status'] == 'RESERVED':
                deleted_ip_list.append(address['name'] + ' ' + address['address'] + ' ' + project + ' ' + address['status'] + ' ' + project + '\n')
        # Getting the next page of IPs
        request = compute.addresses().list_next(previous_request=request, previous_response=response)
    return deleted_ip_list