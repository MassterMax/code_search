import json
import os

from elasticsearch import Elasticsearch

from views import common

METHOD_NAME = "init"

RESULT_TEMPLATE = "Index {} is created successfully"


def impl(request):
    response = {}

    # Check request is correct.
    if not common.check_request(METHOD_NAME, request):
        common.make_error(response, "Wrong request parameter")
        return

    # Look for index schema.
    index_name = request["index_name"]
    dir_path = os.path.dirname(__file__)
    index_schema_path = f"{dir_path}/index_schemas/{index_name}.json"

    schema = common.try_open_file(index_schema_path)
    if schema is None:
        common.make_error(response, f"Failed to open file {index_schema_path}")
        return

        # Create new empty index.
    es = Elasticsearch()
    res = es.indices.create(index=index_name, ignore=400, body=json.loads(schema.read()))
    print(res)
    response["template"] = RESULT_TEMPLATE
    response["index_name"] = index_name

    return response
