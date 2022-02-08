import json
import base64
import requests as r

class Map:
    with open('target.json', 'r') as data:
        target = json.loads(data.read())

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def map_to_target():
        pass

    def upload_assets(domain, assets_file):
        url = domain + "/rest/2.0/import/json-job"

        username=base64.b64decode('RGF0YUxha2VBZG1pbg=='\
            .encode('utf-8'))\
                .decode('utf-8')

        password=base64.b64decode('Y29sbGlicmFkYXRhY2l0aXplbnM='\
            .encode('utf-8'))\
                .decode('utf-8')

        assets = {'file': open(str(assets_file), 'rb')}

        response = r.post(
                url, 
                auth=(username, password),
                files=assets
            )
        return response

class Collect:
    def __init__(self, **kwargs):
        pass

    def CollectServerData(server):
        pass

