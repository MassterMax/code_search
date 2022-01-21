import sys
import click
from codesearch.es.client import ElasticSearchClient


@click.group()
def cs():
    pass


@cs.command()
@click.argument("index_name")
def init(index_name: str):
    print(ES.init(index_name))


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


if __name__ == '__main__':
    ES = ElasticSearchClient()
    cs()
