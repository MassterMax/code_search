from pprint import pprint

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

__DEBUG_FLAG__ = True

class print_colors:
    FUNCTION_NAME = '\033[94m'
    END = '\033[0m'

def pretty_print(searching_result):
    print(f"{print_colors.FUNCTION_NAME}Found:{print_colors.END}", len(searching_result), "matches")
    for match in searching_result:
        # match = url + file + function_name
        print(f"{print_colors.FUNCTION_NAME}Function:{print_colors.END}", match["function_name"])
        print(match["url"], "/blob/master", match["file"], sep = "")
        if __DEBUG_FLAG__:
            pprint(match)