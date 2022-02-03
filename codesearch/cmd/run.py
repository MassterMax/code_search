import json
import os
from pprint import pprint

import click

from codesearch.es.client import ElasticSearchClient
from codesearch.preproc.extract import extract_from_csv


@click.group()
def cs():
    pass


@cs.command()
@click.argument("index_name")
def init(index_name: str):
    print(ES.create(index_name))


@cs.command()
@click.argument("index_name")
def delete(index_name: str):
    print(ES.delete(index_name))


@cs.command()
@click.argument("index_name")
@click.argument("results_path")
def put(index_name: str, results_path: str):
    directory = os.fsencode(results_path)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            print(f'loading: {filename}')
            with open(f'{results_path}/{filename}', encoding='utf-8') as json_file:
                data = json.load(json_file)
                print(ES.load_data(index_name, data))
                print(f'success: {filename}')


@cs.command()
@click.argument("index_name")
@click.argument("search_request")
def search(index_name: str, search_request: str):
    pprint(ES.search(index_name, search_request))


@cs.command()
@click.argument("index_name")
@click.argument("path_to_json_request")
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
@click.argument("csv_path")
@click.argument("storage_path")
@click.argument("output_path")
@click.argument("file_size_mb")
def extract(csv_path: str, storage_path: str, output_path: str, file_size_mb: int = 1024):
    extract_from_csv(csv_path, storage_path, output_path, file_size_mb)


if __name__ == '__main__':
    ES = ElasticSearchClient()
    cs()
