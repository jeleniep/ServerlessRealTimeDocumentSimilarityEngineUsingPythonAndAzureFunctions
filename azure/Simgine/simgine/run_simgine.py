from gensim.models.doc2vec import Doc2Vec
from azure.storage.blob import BlobClient
import os
import yaml
connection_string = os.getenv('AzureWebJobsStorage')


def get_file_from_blob(name):
    blob = BlobClient.from_connection_string(
        conn_str=connection_string, container_name="simgine-data", blob_name=name
    )
    data = None
    blob_data = blob.download_blob()
    data =  blob_data.readall()
    return data


def simgine(article_title, model_path='doc2vec.model'):

    try:
        yaml_file = get_file_from_blob(f"{article_title}.yaml")
        parsed = yaml.load(yaml_file, Loader=yaml.FullLoader)
        cats = set(parsed['Categories'])
        print("Oooo", flush=True)
        print(cats, flush=True)

    except:
        print(f'No YAML file for {article_title}')
        cats = None

    model = Doc2Vec.load(model_path)

    acc = 0
    TOP = 20
    row = '\t{:<40}{:<13}{}'

    similar_doc = model.docvecs.most_similar(article_title, topn=TOP)
    response = {}

    for i, pair in enumerate(similar_doc[0:TOP]):
        other_title = pair[0]
        q = 0
        if cats:
            q = mutual_cats(cats, other_title)
            acc += int(q > 0)
        print(f'{i+1}.' + row.format(other_title,
                                     str(round(pair[1], 2)), q if q else 0))
        response[i+1] = {
            'Article': pair[0],
            'Cosine Sim': str(round(pair[1], 2)),
            'Mutual Categories': q if q else 0
        }

    return response


def mutual_cats(cats, other):
    try:
        yaml_file = get_file_from_blob(f"{other}.yaml")
        parsed = yaml.load(yaml_file, Loader=yaml.FullLoader)
        other_cats = set(parsed['Categories'])
    except:
        print(f'No YAML file for {other}')
        return 0
    q = len(cats.intersection(other_cats))
    return q
