import requests
import json
import configparser
import csv
import boto3

lat = 42.36
lon = 71.05
lat_log_params = {"lat": lat, "lon": lon}

api_response = requests.get(
    "http://api.open-notify.org/iss-pass.json", params=lat_log_params)

# Utworzenie obiektu json na podstawie zawartości udzielonej odpowiedzi.
response_json = json.loads(api_response.content)

all_passes = []
for response in response_json['response']:
    current_pass = []

    # Zapisanie współrzędnych geograficznych z żądania.
    current_pass.append(lat)
    current_pass.append(lon)

    # Przechowywanie daty pojawienia się stacji nad danym miejscem i czasu jej przelotu.
    current_pass.append(response['duration'])
    current_pass.append(response['risetime'])

    all_passes.append(current_pass)

export_file = "export_file_rest_api.csv"

with open(export_file, 'w') as fp:
	csvw = csv.writer(fp, delimiter='|')
	csvw.writerows(all_passes)

fp.close()

# Wczytanie wartości aws_boto_credentials.
parser = configparser.ConfigParser()
parser.read("pipeline.conf")
access_key = parser.get("aws_boto_credentials",
                "access_key")
secret_key = parser.get("aws_boto_credentials",
                "secret_key")
bucket_name = parser.get("aws_boto_credentials",
                "bucket_name")

s3 = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key)

s3.upload_file(
    export_file,
    bucket_name,
    export_file)
