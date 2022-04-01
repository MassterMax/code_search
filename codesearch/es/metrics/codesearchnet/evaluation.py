from typing import Dict, List

from codesearch.es.client import ElasticSearchClient


def top_n(dataset: List[Dict[str, str]], client: ElasticSearchClient, index_name: str, top_n: int = 10):
    score = 0.0

    for item in dataset:
        query = item["query"]
        location = item["location"]

        result = client.search_doc(index_name, {"query": query, "from": 0, "size": top_n})

        for entity in result:
            if entity["location"] == location:
                score += 1
                break

    return score / len(dataset)


def make_search_query(query: str,
                      identifiers_weight: int = 1,
                      split_identifiers_weight: int = 1,
                      function_body_weight: int = 1,
                      docstring_weight: int = 1,
                      location_weight: int = 1,
                      function_name_weight: int = 1,
                      ) -> Dict:
    return {
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
                            "prefix_length": 2
                        }
                    }
                }
            }
        }
