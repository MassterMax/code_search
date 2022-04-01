from typing import Callable, Dict, List

from codesearch.es.client import ElasticSearchClient
from codesearch.es.vs.v1 import transform_output_light


def top_n(dataset: List[Dict[str, str]],
          search_query_func: Callable[[str], Dict],
          client: ElasticSearchClient,
          index_name: str,
          n: int = 10):
    score = 0.0
    for item in dataset:
        query = item["query"]        # feature
        location = item["location"]  # target

        result = client.instance.search(index=index_name, body=search_query_func(query))
        result = transform_output_light(result)

        for i, entity in enumerate(result):
            if i == n:
                break
            if entity["location"] == location:
                score += 1
                break

    return score / len(dataset)


def make_search_query_func(identifiers_weight: int = 1,
                           split_identifiers_weight: int = 1,
                           function_body_weight: int = 1,
                           docstring_weight: int = 1,
                           location_weight: int = 1,
                           function_name_weight: int = 1,
                           prefix_length: int = 2,
                           start: int = 0,
                           size: int = 5
                           ) -> Callable[[str], Dict]:
    return lambda query: {
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": [
                            # exact occurrence
                            f"identifiers^{identifiers_weight}",
                            f"split_identifiers^{split_identifiers_weight}",
                            f"function_body^{function_body_weight}",
                            # meaning
                            f"docstring^{docstring_weight}",
                            f"location^{location_weight}"
                            f"function_name^{function_name_weight}",
                        ],
                        "type": "most_fields",
                        "fuzziness": "AUTO",
                        "prefix_length": prefix_length
                    }
                }
            }
        },
        "from": start,
        "size": size
    }
