from typing import Any, Dict, List


# def make_responses():
#     queries: List[str],

def calculate_metric(responses: List[Dict[str, Any]], correct_answers: List[str]) -> float:
    """

    Args:
        responses: Responses from elasticsearch, fitted with v1.transform_output(...)
        correct_answers: List of correct functionality in format ["location1#start_line1", ...], for example
        ["https://github.com/MassterMax/code_search/blob/main/codesearch/es/es_explain.py#L14", ...]

    Returns:
        float number - if top

    """
    pass
