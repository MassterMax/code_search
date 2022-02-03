from typing import Dict, List


class SearchConstructor:
    @classmethod
    def make_query(cls, data: Dict):
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
                                "docstring^3",
                                "identifiers",
                                "function_name"
                            ],
                            "fuzziness": "AUTO",
                            "prefix_length": 2
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
    def add_filters(cls, filters: List, data: Dict):
        for el in data["filters"]:
            FILTER_MAPPING[el](filters, data["filters"][el])


INF = 1000000000
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
