#import pandas as pd
import base64
import requests as r
import re
from requests.auth import HTTPBasicAuth
import json
import sys
import mapper as m


#gis_server = sys.argv[1]
#user_name = sys.argv[2]
#password = sys.argv[3]

gis_server = "https://maps2.dcgis.dc.gov/dcgis/rest/services{}"

server_json = r.get(url=gis_server.format("?f=pjson")).json()

if server_json['folders'] is None:
    pass
else:
 folders =server_json['folders']

if server_json['services'] is None:
    pass
else:
    services = server_json['services']

complete_json={}

#folders=["HSEMA"] #Uncomment this to test just with the HSEMA folder

# Collect all metadata from the folders in the top level of the ArcGIS Server home page
for folder in folders:
    complete_json[folder]=""
    url = gis_server[:-2]+"/"+folder+"?f=pjson"
    try:
        folder_response =r.get(url=url)
    except:
        pass
    folder_services = folder_response.json()['services']
    if folder_services is None:
        pass
    else:
        complete_json[folder]=folder_services
    # except KeyError:
    #     folder_services= "no services in this folder"

    for service in complete_json[folder]:
        #print(service)
        service_url = url.replace("?f=pjson","/"+service['name'].split("/")[1])+"/"+service['type']+"?f=pjson"
        service_response = r.get(service_url)
        service_json= service_response.json()
        service['metadata']=service_json
        try:
            layers = service['metadata']['layers']
            for layer in layers:
                #print(layer['name'])
                layer_url = service_url.replace("?f=pjson","/"+str(layer['id']))+"?f=pjson"
                layer_metadata = r.get(layer_url).json()
                layer['detailed_layer_metadata']=layer_metadata
        except:
            pass
    print(str(folder) + " COMPLETED")


### EXTACT THE DATA AND MAP TO THE IMPORT TEMPLATES ###


#write the data to a local file
with open("server_payload.json", "w") as f:
    # parse through the json to access the fields of a single layer
    data = complete_json#['DCGIS_DATA'][20]['metadata']['layers'][0]['detailed_layer_metadata']['fields']
    f.write(str(data))
f.close()

### - SCRATCH - ###

### SCRATCH FOR EXTACT THE DATA AND MAP TO THE IMPORT TEMPLATES  ###

# funciton to upload assets 
def upload_assets(domain, assets_file):
    url = domain + "/rest/2.0/import/json-job"

    username=base64.b64decode('usn'\
        .encode('utf-8'))\
            .decode('utf-8')
    password=base64.b64decode('pass'\
        .encode('utf-8'))\
            .decode('utf-8')

    assets = {'file': open(str(assets_file), 'rb')}

    response = r.post(
            url, 
            auth=(username, password),
            files=assets
        )
    return response

# Path to parse through the json layers
data = complete_json['HSEMA']#[20]['metadata']['layers'][0]['detailed_layer_metadata']['fields']

# Process to collect the folders from the server home page
with open("templates/import-folder-template.json", 'r') as f:
    f= open("templates/import-folder-template.json", 'r') 
    asset_list=[]
    folder_list=[]
    target_pattern = json.loads(f.read())[0]

    for key, value in complete_json.items():
        folder_list.append(key)

    for i in folder_list:
        print(i)
        # target_pattern = json.loads(f.read())[0]
        target_pattern['identifier']['name'] = i
        new_pattern = json.dumps(target_pattern)
        asset_list.append(json.loads(new_pattern))

with open('uploads/folder-uploads.json', 'w') as f:
    f.write(str(asset_list).replace("'",'"'))

upload_folders = upload_assets('https://wconnellycollibracloud.collibra.com/', 
'uploads/folder-uploads.json')
    

# Path to parse through the json layers
data = complete_json['HSEMA']#[20]['metadata']['layers'][0]['detailed_layer_metadata']['fields']
 
 # Collect all services in the Folders and upload them
 # to the associated folder (Physical Data Dictionary)

    # function to remove escape cahracters from the descriptions
def escape_char_sub(s):
    str = re.sub('[^A-Za-z0-9]+', ' ', s)
    return str

with open("templates/import-schema.json", 'r') as f:
    target_pattern = json.loads(f.read())[0]

    asset_list=[]
    folder_list=[]

    for key, value in complete_json.items():
        folder_list.append(key)

    for folder in folder_list:
        data=complete_json[folder]
        for i in range(0, len(data)):
            target_pattern['identifier']['name']=data[i]['name'] +" - "+ data[i]['type']
            target_pattern['attributes']['Description'][0]['value']=escape_char_sub(data[i]['metadata']['serviceDescription'])
            # need to figure out how to remove escape characters in the descriptions 
            target_pattern['identifier']['domain']['name']=folder
            new_pattern = json.dumps(target_pattern)
            asset_list.append(json.loads(new_pattern))

with open('uploads/schema-uploads.json', 'w') as f:
    f.write(str(asset_list).replace("'",'"'))

upload_schemas= upload_assets(
    'https://wconnellycollibracloud.collibra.com/', 
'uploads/schema-uploads.json')




#collect all metadata from the Services listed on the ArcGIS server homepage




