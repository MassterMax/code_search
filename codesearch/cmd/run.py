import click

from codesearch.es.client import ElasticSearchClient
from codesearch.preproc.extract import extract_data


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
def put(index_name: str):
    print(ES.load_data(index_name))


@cs.command()
@click.argument("index_name")
@click.argument("search_request")
def search(index_name: str, search_request: str):
    print(ES.search(index_name, search_request))


@cs.command()
@click.argument("repositories_path")
@click.argument("output_directory")
@click.argument("git_location")
def extract(repositories_path: str, output_directory: str, git_location: bool = True):
    extract_data(repositories_path, output_directory, git_location)


if __name__ == '__main__':
    ES = ElasticSearchClient()
    cs()
