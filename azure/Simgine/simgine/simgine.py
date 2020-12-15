import logging
import os

import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

connection_string=os.getenv('AzureWebJobsStorage')

service = BlobServiceClient.from_connection_string(conn_str=connection_string)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req.method

    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name="simgine-data", blob_name="pytania.txt")
    with open("./test.txt", "wb") as my_blob:
        print("asdasd", flush=True)
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
        return func.HttpResponse(f"Hello team, {name}. This HTTP triggered function executed successfully. {req.method}")
    else:
        return func.HttpResponse(
             "This HTTPs triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
