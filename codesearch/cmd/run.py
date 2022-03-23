import datetime
import json
import os
from pprint import pprint

import click
from tqdm import tqdm

import codesearch.constants as consts
from codesearch.es.client import ElasticSearchClient
from codesearch.es.metrics.top_n import calculate_metric
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
    """
    Args:
        search_request: request as a string
        index_name: index in which documents are searched
    """
    pprint(ES.search(index_name, search_request, consts.REALISE_SEARCH_MODE))


@cs.command()
@click.argument("index_name")
@click.argument("search_request")
def explain(index_name: str, search_request: str):
    """
    Same as search but save explain in es/explain_plans
    """
    pprint(ES.search(index_name, search_request, consts.EXPLAIN_SEARCH_MODE))


@cs.command()
@click.argument("index_name")
@click.argument("search_request")
def time(index_name: str, search_request: str):
    pprint(ES.search(index_name, search_request, consts.TIMINGS_SEARCH_MODE))


@cs.command()
@click.argument("index_name")
@click.option('--path_to_json_request', '-p', type=click.Path(exists=True), default=None)
@click.option('--search_query', '-q', default=None)
def search_doc(index_name: str, path_to_json_request: str, search_query: str) -> None:
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
          }
        }
        search_query: or exact query instead of path to doc

    Returns: request result

    """
    if path_to_json_request is None and search_query is None:
        raise ValueError("You should specify path to request or query!")

    if search_query is None:
        with open(path_to_json_request, 'r') as f:
            data = json.load(f)
    else:
        data = {"query": search_query, "from": 0, "size": 5,
                "filters": {"language": ["Python", "C++"],
                            "stargazers_count": {"from": 50}
                            }
                }

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


@cs.command()
@click.argument("index_name")
@click.argument("path_to_json_dataset", type=click.Path(exists=True))
@click.argument("top_n", type=int)
def calculate_top_n_metric(index_name: str, path_to_json_dataset: str, top_n: int) -> None:
    """
    A method to calculate top_n metric of index with given search request
    Args:
        index_name: index where we want to search
        path_to_json_dataset: path to our validation dataset, looks like
            [
                {"query":  "example request", "url": "https://github.com/path/to/func#L42"},
                {"query":  "Gurren Lagann", "url": "https://github.com/another/path#L1337"}
            ]
        top_n: same as top_n parameter of top_n.py/calculate_metric function
    """

    with open(path_to_json_dataset, 'r') as f:
        data = json.load(f)

    queries = [entity["query"] for entity in data]
    answers = [entity["answer"] for entity in data]

    responses = []
    for query in queries:
        result = ES.search_doc(index_name, {"query": query, "from": 0, "size": top_n,
                                            "filters": {"language": ["Python"],
                                                        "stargazers_count": {"from": 0}
                                                        }
                                            })
        responses.append(result)

    metric = calculate_metric(responses, answers, top_n)
    print(f"top {top_n}: {metric}")
    # todo how to increase the score? we can change search constructor with different params and check this metric
