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


def map_n(dataset: List[Dict[str, str]], client: ElasticSearchClient, index_name: str, map_n: int = 10):
    scores = []

    for item in dataset:
        query = item["query"]
        location = item["location"]

        result = client.search_doc(index_name, {"query": query, "from": 0, "size": top_n})
        score = 0

        for i, entity in enumerate(result):
            if entity["location"] == location:
                score = 1 / (1 + i)
                break
        scores.append(score)

    return sum(scores) / len(scores)
