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
def put(index_name: str):
    print(ES.load_data(index_name))


@cs.command()
@click.argument("index_name")
@click.argument("search_request")
def search(index_name: str, search_request: str):
    print(ES.search(index_name, search_request))


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
