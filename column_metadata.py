import requests
import pandas as pd
import json
import os
import sys

#to run from terminal just use the command: python3 column_metadata.py [DOMAIN] [USERNAME] [PASSWORD]

#get the domain
domain = sys.argv[1]

#collect username and password
username = sys.argv[2]
password = sys.argv[3]

#get the current working directory and create output path
output_path = os.getcwd() + "/domain_metadata.csv"

def get_metadata(**kwargs):
    # get the full metadata payload from the platform
    url = "http://api.us.socrata.com/api/catalog/v1?domains={}&only=datasets&search_context={}&limit=100000".format(domain, domain)
    metadata = requests.get(url,
                          auth=(username, password),
                          headers={'Content-Type': 'application/json'}).json()
    #create an empty dict and lists to collect the data
    data = {}
    name_list = []
    id_list = []
    column_names_list = []
    column_field_names_list  = []

    #iterate through the catalog metadata and collect the dataset name, id, column names, and API field names
    for x in range(0,len(metadata['results'])):
        num_ids = len(metadata['results'][x]['resource']['columns_name'])
        for i in range(0, num_ids):
            id_list.append(metadata['results'][x]['resource']['id'])
            name_list.append(metadata['results'][x]['resource']['name'])
            column_names_list.append(metadata['results'][x]['resource']['columns_name'][i])
            column_field_names_list.append(metadata['results'][x]['resource']['columns_field_name'][i])
        data['dataset_name'] = name_list
        data['dataset_id'] = id_list
        data['column_name'] = column_names_list
        data['column_api_field_name'] = column_field_names_list

    #write the lists to a dataframe
    domain_data = pd.DataFrame(data)
    return domain_data

if __name__ == "__main__":
    #run function and write output to a csv
    data = get_metadata(domain=domain, username=username, password=password)
    data.to_csv(output_path, index=False)
