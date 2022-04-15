from typing import Any, Dict, List


class SearchConstructor:
    @classmethod
    def make_query(cls, data: Dict) -> Dict[str, Any]:
        """
        Make elastic query from given request
        Args:
            data: request like example_request.json
        Returns: elastic query
        """
        query = cls.main_body(data["query"])
        query['from'] = data.get('from', 0)
        query['size'] = data.get('size', 5)
        filters = query['query']['bool']['filter']['bool']['must']
        cls.add_filters(filters, data)
        return query

    @classmethod
    def main_body(cls, query: str) -> Dict:
        return {
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": query,
                            "fields": [
                                # exact occurrence
                                "identifiers^1",
                                "split_identifiers^2",
                                "function_body^2",
                                # meaning
                                "docstring^12",
                                "location^3",
                                "function_name^5",
                            ],
                            "type": "most_fields",
                            "fuzziness": "AUTO",
                            "prefix_length": 3
                        }
                    },
                    "filter": {
                        "bool": {
                            "must": [

                            ]
                        }
                    }
                }
            }
        }

    @classmethod
    def add_filters(cls, filters: List, data: Dict) -> None:
        """
        Add filters to query body
        Args:
            filters: filters part of elastic query
            (inside filter-bool-must)
            data: filter parameters
        """
        for el in data["filters"]:
            FILTER_MAPPING[el](filters, data["filters"][el])


INF = 10000000
FILTER_MAPPING = {
    "language": lambda filters, value: filters.append({
        "terms": {
            "language": value
        }
    }),
    "stargazers_count": lambda filters, value: filters.append({
        "range": {
            "stargazers_count": {
                "gte": value.get("from", -1),
                "lte": value.get("to", INF)
            }
        }
    })
}
