import json
import os
from ssl import create_default_context
from typing import Dict

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

from codesearch.es.search_constructor import SearchConstructor
from codesearch.es.vs import v1

class ElasticSearchClient:
    def __init__(self):
        """
        Access elasticsearch by https://localhost::9200
        """
        load_dotenv()
        context = create_default_context(cafile=os.environ['PATH_TO_ES_CERTIFICATE'])
        self.instance = Elasticsearch(
            ['localhost', 'es01'],
            http_auth=('elastic', os.environ['ELASTIC_PASSWORD']),
            scheme="https",
            port=9200,
            ssl_context=context
        )

    def create(self, index_name: str):
        """
        Create index with schema, defined in index_schemas folder
        Args:
            index_name: name of elastic index

        Returns: result as Dict
        """
        dir_path = os.path.dirname(__file__)
        index_schema_path = f"{dir_path}/index_schemas/{index_name}.json"

        try:
            with open(index_schema_path, "r", encoding='utf-8') as schema:
                res = self.instance.indices.create(index=index_name,
                                                   ignore=400,
                                                   body=json.loads(schema.read()))
            return res
        except IOError as e:
            return {'status': 'error', 'errors': e}

    def load_data(self, index_name: str, data: Dict):
        try:
            for entity in data:
                self.instance.index(index=index_name, document=entity)
        except Exception as e:
            return {'status': 'error', 'errors': e}

        return {'status': 'ok'}

    def search(self, index_name: str, search_request: str):
        search_request = v1.transform_input(search_request)
        if search_request is None:
            return {'status': 'error', 'errors': 'Failed to build search input'}
        res = self.instance.search(index=index_name, body=search_request)
        return v1.transform_output(res)

    def search_doc(self, index_name: str, data: Dict):
        """
        Search data in index with request like in example_request
        Args:
            index_name: index to search
            data: provided request

        Returns: result from elastic
        """
        search_request = SearchConstructor.make_query(data)
        res = self.instance.search(index=index_name, body=search_request)
        return v1.transform_output(res)

    def delete(self, index_name: str):
        """
        Delete elastic index
        Args:
            index_name: name of index

        Returns: Dictionary-like result
        """
        try:
            self.instance.indices.delete(index=index_name)
        except Exception as e:
            return {'status': 'error', 'errors': e}

        return {'status': 'ok'}


if __name__ == '__main__':
    pass
