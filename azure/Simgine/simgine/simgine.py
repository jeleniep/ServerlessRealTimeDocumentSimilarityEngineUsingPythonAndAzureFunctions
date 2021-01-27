from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import azure.functions as func
from . import simgine
import logging
import os
import sys
import json
import tempfile

sys.path.append("..")

connection_string = os.getenv('AzureWebJobsStorage')

service = BlobServiceClient.from_connection_string(conn_str=connection_string)





def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    blob = BlobClient.from_connection_string(
        conn_str=connection_string, container_name="simgine-data", blob_name="3_doc2vec.model"
        # conn_str=connection_string, container_name="simgine", blob_name="3_doc2vec.model"
    )
    foldername = tempfile.gettempdir()
    print(foldername, flush=True)
    with open(foldername + "/doc2vec.model", "wb") as my_blob:
        blob_data = blob.download_blob()
        blob_data.readinto(my_blob)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        response = simgine(name, foldername + "/doc2vec.model")
        return func.HttpResponse(
            json.dumps(response),
            mimetype='application/json'
        )
    else:
        return func.HttpResponse(
            "Pass article name as 'name' query string. Example: '?name=Jaguar'",
            status_code=400
        )
