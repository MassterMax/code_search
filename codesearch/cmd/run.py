import sys
import click
sys.path.insert(0, './codesearch/es/')
from es_connector import ESConnector


@click.group()
def cs():
    pass

@cs.command()
@click.argument("index_name")
def init(index_name: str):
    print(es_obj.init(index_name))

@cs.command()
@click.argument("index_name")
def delete(index_name: str):
    print(es_obj.delete(index_name))

@cs.command()
@click.argument("index_name")
def put(index_name: str):
    print(es_obj.load_data(index_name))

@cs.command()
@click.argument("index_name")
@click.argument("search_request")
def search(index_name: str, search_request: str):
    print(es_obj.search(index_name, search_request))

if __name__ == '__main__':
    es_obj = ESConnector()
    cs()
