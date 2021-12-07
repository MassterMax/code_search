import json

from views.search.vs import v1

from elasticsearch import Elasticsearch

from views import common

METHOD_NAME = "search"

RESULT_TEMPLATE = "Searching in {} went successfully"

def impl(request, response):
    # Check request is correct.
    if (not common.check_request(METHOD_NAME, request)):
        common.make_error(response, "Wrong request parameter")
        return
    
    # Look for index schema.
    index_name = request["index_name"]
    search_request = v1.transform(request["search_code_request"])
    # Send search request to elastic
    es = Elasticsearch()
    res = es.search(index=index_name, body=json.loads(search_request))
    print(res)
    response["template"] = RESULT_TEMPLATE
    response["index_name"] = index_name

