from typing import Any, Dict, List


def calculate_metric(responses: List[List[Dict[str, Any]]], correct_answers: List[str], top_n: int) -> float:
    """

    Args:
        responses: list of responses from elasticsearch, fitted with v1.transform_output(...)
        correct_answers: List of correct functionality in format ["location1#start_line1", ...], for example
        ["https://github.com/MassterMax/code_search/blob/main/codesearch/es/es_explain.py#L14", ...]
        top_n: for each query answer is correct if ground_truth appears in top_n most relevant results

    Returns:
        float number - average top_n metric of each result

    """
    score = 0.0
    for j, result in enumerate(responses):
        for i, entity in enumerate(result):
            if i == top_n:
                break
            if entity['url'] == correct_answers[j]:
                score += 1
    return score / len(correct_answers)
