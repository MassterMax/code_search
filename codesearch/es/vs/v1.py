from typing import Any, Dict

import codesearch.constants as consts
from codesearch.es.es_explain import SearchResponseAnalyzer

resp_analyzer = SearchResponseAnalyzer()


def transform_input(user_request, mode=consts.REALISE_SEARCH_MODE):
    result = dict()
    if user_request == "__all":
        result = {
            "query": {
                "match_all": {}
            }
        }
    else:
        result = {
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": user_request,
                            "fields": [
                                # exact occurrence
                                "identifiers^2",
                                "split_identifiers^2",
                                "function_body^2",
                                # meaning
                                "docstring",
                                "location"
                                "function_name",
                            ],
                            "type": "most_fields",
                            "fuzziness": "AUTO",
                            "prefix_length": 2
                        }
                    }
                }
            }
        }
    if mode == consts.EXPLAIN_SEARCH_MODE:
        result["explain"] = True
    if mode == consts.TIMINGS_SEARCH_MODE:
        result["profile"] = True
    return result


def transform_output(search_result, user_request: str, mode=consts.REALISE_SEARCH_MODE):
    if mode == consts.EXPLAIN_SEARCH_MODE:
        resp_analyzer.explain_score(search_result, user_request)
    if mode == consts.TIMINGS_SEARCH_MODE:
        resp_analyzer.explain_time(search_result, user_request)
    return [{'url': f"{el['_source']['location']}#L{el['_source']['start_line'] + 1}",
             'lng': el['_source']['language'],
             'func': el['_source']['function_name'],
             'body': el['_source']['function_body'],
             'score': el['_score'],
             'doc_id': el['_id'],
             } for el in search_result['hits']['hits']]


def transform_output_light(search_result: Dict[str, Any], keep_keys=None):
    if keep_keys is None:
        keep_keys = ["location", "language", "function_name", "function_body"]
    return [{key: el['_source'][key] for key in keep_keys} for el in search_result['hits']['hits']]
