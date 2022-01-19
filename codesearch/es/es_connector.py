import json
import os
from elasticsearch import Elasticsearch
from vs import v1
# todo получается, для смены типа поиска нужно менять прям код, а хотелось бы как в load_data - параметром


# todo заодно поменять es_connector на client
class ElasticSearchClient:
    def __init__(self):
        self.es = Elasticsearch()

    def init(self, index_name: str):
        dir_path = os.path.dirname(__file__)
        index_schema_path = f"{dir_path}/index_schemas/{index_name}.json"

        try:
            with open(index_schema_path, "r", encoding='utf-8') as schema:
                res = self.es.indices.create(index=index_name,
                                             ignore=400,
                                             body=json.loads(schema.read()))
            return res
        except IOError as e:
            return {'status': 'error', 'errors': e}

    def load_data(self, index_name: str):
        try:
            with open(f'{os.getcwd()}/codesearch/preproc/result.json', encoding='utf-8') as json_file:
                data = json.load(json_file)
                for url in data:
                    for path in data[url]:
                        for name in data[url][path]:
                            self.es.index(index=index_name, document=
                            {'url': url, 'file': path, 'function_name': name})
        except Exception as e:
            return {'status': 'error', 'errors': e}

        return {'status': 'ok'}

    def search(self, index_name: str, search_request: str):
        search_request = v1.transform_input(search_request)
        if search_request is None:
            return {'status': 'error', 'errors': 'Failed to build search input'}
        res = self.es.search(index=index_name, body=search_request)
        return v1.transform_output(res)

    def delete(self, index_name: str):
        try:
            self.es.indices.delete(index=index_name)
        except Exception as e:
            return {'status': 'error', 'errors': e}

        return {'status': 'ok'}


if __name__ == '__main__':
    pass
