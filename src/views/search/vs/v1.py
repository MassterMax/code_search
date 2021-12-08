def transform(user_request):
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
