def transform_input(user_request):
    if user_request == "__all":
        return {
            "query": {
                "match_all": {}
            }
        }
    return {
        "query": {
            "simple_query_string": {
                "query": user_request,
                "fields": ["function_name"],
                "default_operator": "or",
                "fuzzy_prefix_length": 5
            }
        }
    }


def transform_output(search_result):
    return [el['_source'] for el in search_result['hits']['hits']]
