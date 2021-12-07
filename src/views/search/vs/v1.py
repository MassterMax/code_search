def transform(user_request):
    if user_request == "__all":
        return {
            "query": {
                "match_all": {}
            }
        }
    return {
        "query": {
            "match": {
                "function_name": {
                    "query": user_request,
                    "fuzziness": 10
                }
            }
        }
    }
