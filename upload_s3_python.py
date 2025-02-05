#!/usr/bin/env python
# -*- coding: utf8 -*- 

import boto3
from botocore.client import ClientError
import requests
import subprocess
import os

user_data = 'http://169.254.169.254/latest/user-data'
meta_data = 'http://169.254.169.254/latest/meta-data'
ec2InsDatafile = 'ec2InsDatafile'
ec2_params = {
    'Instance ID': 'instance-id',
    'Reservation ID': 'reservation-id',
    'Public IP': 'public-ipv4',
    'Public Hostname': 'public-hostname',
    'Private IP': 'local-ipv4',
    'Security Groups': 'security-groups',
    'AMI ID': 'ami-id'
}


try:
    with open(ec2InsDatafile, 'w') as fh:
        for param, value in ec2_params.items():
            try:
                response = requests.get(meta_data + '/' + value)
                if response.status_code == 200:
                    data = f"{param}: {response.text}"
                    fh.write(data + '\r\n')
                else:
                    print(f"Error: {param} not found")
            except requests.exceptions.RequestException as e:
                print(f"Error during request for {param}: {e}")
except Exception as e:
    print(f"Error while opening file for writing: {e}")


try:
    os_name = subprocess.check_output("grep ^NAME /etc/os-release", shell=True).decode('utf-8').strip().split('=')[1]
    os_version = subprocess.check_output("grep ^VERSION /etc/os-release", shell=True).decode('utf-8').strip().split('=')[1]
    os_users = subprocess.check_output("grep -E 'bash|sh' /etc/passwd | awk -F : '{print $1}'", shell=True).decode('utf-8').strip()

    with open(ec2InsDatafile, 'a') as fh:
        fh.write(f"OS NAME: {os_name}\r\n")
        fh.write(f"OS VERSION: {os_version}\r\n")
        fh.write(f"Login able users: {os_users}\r\n")
except subprocess.CalledProcessError as e:
    print(f"Error while fetching system info: {e}")


s3_bucket_name = 'applicant-task'
s3_key = 'r2d2/system_info.txt'
s3_conn = boto3.client('s3')

try:
    with open(ec2InsDatafile, 'r') as fh:
        s3_conn.put_object(
            Bucket=s3_bucket_name,
            Key=s3_key,
            Body=fh.read()
        )
    print(f"File has been uploaded to {s3_bucket_name} S3 bucket under the 'r2d2' folder.")
except ClientError as e:
    print(f"Error uploading file to S3: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
