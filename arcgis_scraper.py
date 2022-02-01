#import pandas as pd
import requests as r
import json
import sys

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
        print(service)
        service_url = url.replace("?f=pjson","/"+service['name'].split("/")[1])+"/"+service['type']+"?f=pjson"
        service_response = r.get(service_url)
        service_json= service_response.json()
        service['metadata']=service_json
        try:
            layers = service['metadata']['layers']
            for layer in layers:
                print(layer['name'])
                layer_url = service_url.replace("?f=pjson","/"+str(layer['id']))+"?f=pjson"
                layer_metadata = r.get(layer_url).json()
                layer['detailed_layer_metadata']=layer_metadata
        except:
            pass


with open("/Users/william.connelly/Desktop/untitled.json", "w") as f:
    # parse through the json to access the fields of a single layer
    data = complete_json['DCGIS_DATA'][20]['metadata']['layers'][0]['detailed_layer_metadata']['fields']
    f.write(str(data))
f.close()

#collect all metadata from the Services listed on the ArcGIS server homepage

for service in services:
    service_url = gis_server[:-2] + "/" + service['name']+"/"+service['type'] + "?f=pjson"
    service_response = r.get(service_url)
    service_json = service_response.json()
    print(service_json)

    for layer in service_json['layers']:
        layer_url = service_url.replace("?f=pjson","/"+str(layer['id']))+"?f=pjson"
        layer_metadata = r.get(layer_url).json()
        print(layer_metadata)



layer_col_data = pd.DataFrame(fields)

server_data = r.get("https:services2.arcgis.comSCn6czzcqKAFwdGUArcGISrestservices?f=json")

server_list = server_data.json()['services']

server = server_list[0]['url']
server1 = server_list[0]['url'] +"?f=json"

layers = r.get(server1).json()['layers']

layer_id = layers[0]['id']

layer_info_json = r.get(server + "" +str(layer_id)+"?f=json").json()

servers = pd.DataFrame(server_list)
servers.to_csv("Userswilliam.connellyDesktopMyDocsCollibraSolano Countyservers.csv")


