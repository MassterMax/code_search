import datetime
import json
import os
from pprint import pprint

import click
from tqdm import tqdm

from codesearch.es.client import ElasticSearchClient
from codesearch.preproc.extract import extract_from_csv

ES = ElasticSearchClient()


@click.group()
def cs():
    """
    A command of type group. All others are attached to it.
    """
    pass


@cs.command()
@click.argument("index_name")
def init(index_name: str):
    """
    Initialize elastic index with given name
    Args:
        index_name: elastic index name
    """
    print(ES.create(index_name))


@cs.command()
@click.argument("index_name")
def delete(index_name: str):
    """
    Delete elastic index with given name
    Args:
        index_name: elastic index name
    """
    print(ES.delete(index_name))


@cs.command()
@click.argument("index_name")
@click.argument("output_directory", type=click.Path(exists=True))
def put(index_name: str, output_directory: str):
    """
    Put to elastic index entities from directory with jsons
    Args:
        index_name: elastic index
        output_directory: directory with jsons - each json should be
        an array of entities prepared to be stored
    """
    directory = os.fsencode(output_directory)
    for file in tqdm(os.listdir(directory)):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            with open(f'{output_directory}/{filename}', encoding='utf-8') as json_file:
                data = json.load(json_file)
                print(ES.load_data(index_name, data))


@cs.command()
@click.argument("index_name")
@click.argument("search_request")
def search(index_name: str, search_request: str):
    pprint(ES.search(index_name, search_request))


@cs.command()
@click.argument("index_name")
@click.argument("path_to_json_request", type=click.Path(exists=True))
def search2(index_name: str, path_to_json_request: str):
    """
    Args:
        index_name: index where we search
        path_to_json_request: path to request body looks like:
        {
          "query": "bla-bla-bla",
          "from": 0,
          "size": 5,
          "filters": {
            "language": [
              "Python"
            ],
            "stargazers_count": {
              "from": 500,
              "to" : 10000
            },
            "location": {todo}
          }
        }
        // todo - add validation via pydantic

    Returns: request result

    """
    with open(path_to_json_request, 'r') as f:
        data = json.load(f)
    pprint(ES.search_doc(index_name, data))


@cs.command()
@click.argument("csv_path", type=click.Path(exists=True))
@click.argument("storage_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path(exists=True))
@click.argument("file_size_mb", default=1024)
def extract(csv_path: str, storage_path: str, output_path: str, file_size_mb: int):
    """
    Extract data from scv file
    Args:
        csv_path: path to csv file with repos
        storage_path: path where to store repos
        output_path: path where to store output .jsons
        file_size_mb: size of each json file
    """
    extract_from_csv(csv_path, storage_path, output_path, file_size_mb)
