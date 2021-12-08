import json
import os

from elasticsearch import Elasticsearch
from elasticsearch import exceptions as EcExceptions
import src.views.common as common

METHOD_NAME = "delete"

RESULT_TEMPLATE = "Index {} is deleted successfully"


def impl(request, response):

    # Check request is correct.
    if not common.check_request(METHOD_NAME, request):
        common.make_error(response, "Wrong request parameter")
        return

    index_name = request["index_name"]
    # Delete index.
    try:
        es = Elasticsearch()
        res = es.indices.delete(index=index_name, ignore=[400, 404])
        print(res)
        response["template"] = RESULT_TEMPLATE
        response["index_name"] = index_name
    except EcExceptions.ConnectionError as err:
        common.make_error(response, f"Failed to connect es: {err}")
    return response
