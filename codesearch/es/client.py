import json
import os
from pprint import pprint
from typing import Dict

from elasticsearch import Elasticsearch

from codesearch.es.search_constructor import SearchConstructor
from codesearch.es.vs import v1


class ElasticSearchClient:
    def __init__(self):
        self.instance = Elasticsearch()

    def create(self, index_name: str):
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
        search_request = SearchConstructor.make_query(data)
        res = self.instance.search(index=index_name, body=search_request)
        return v1.transform_output(res)

    def delete(self, index_name: str):
        try:
            self.instance.indices.delete(index=index_name)
        except Exception as e:
            return {'status': 'error', 'errors': e}

        return {'status': 'ok'}


if __name__ == '__main__':
    pass
