from pathlib import Path
from typing import Any, Dict, Iterator, List, Tuple

import pandas as pd
from preprocess.mappers.utils import TokenParser

parser = TokenParser()
DATASET_TO_ELASTIC_MAPPING = {
    "code": "function_body",
    "code_tokens": "identifiers",
    "docstring": "docstring",
    "url": "location",
    "func_name": "function_name"
}


def dataset_to_elastic(path_to_dataset_folder: str) -> Iterator[Dict[str, Any]]:
    """
    This method gets path to CodeSearchNet dataset folder and returns an Iterator of entities that ready to be
    stored in elastic index with train_index schema
    Args:
        path_to_dataset_folder: path to CodeSearchNet dataset
    Returns: iterator of prepared entities
    """
    python_files = sorted(Path(path_to_dataset_folder).glob("**/*.gz"))

    for file in python_files:
        print(f"extract data from: {file}")
        data = pd.read_json(file,
                            orient="records",
                            compression="gzip",
                            lines=True)

        values = data.values.tolist()
        for value in values:
            yield prepare_entity_to_elastic(data.columns.tolist(), value)


def prepare_entity_to_elastic(columns: List[str], entity: List[str]) -> Dict[str, Any]:
    """
    This method get columns and values and transform it to one elastic entity
    Args:
        columns: ==keys of entity
        entity: ==values of entity
    Returns: One dictionary-like entity
    """
    result = {}

    for column, value in zip(columns, entity):
        if column in DATASET_TO_ELASTIC_MAPPING:
            elastic_field = DATASET_TO_ELASTIC_MAPPING[column]
            result[elastic_field] = value

    result["split_identifiers"] = []
    for identifier in result["identifiers"]:
        result["split_identifiers"].extend(list(parser.split(identifier)))

    # we should remove docstring from function body
    result["function_body"] = result.get("function_body", "").replace(result["docstring"], "")

    return result


def make_dataset_for_evaluation(path_to_dataset_folder: str) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """
    This method marks up dataset for evaluation
    Args:
        path_to_dataset_folder: path to CodeSearchNet dataset

    Returns: train and test dataset, prepared from CodeSearchNet. This is a list of pairs - docstring (to make a
    query from it) and url - to definitely know corresponding function
    """
    # works for ~ 1 min, 200 MB in RAM
    train_dataset = []
    test_dataset = []
    python_files = sorted(Path(path_to_dataset_folder).glob("**/*.gz"))

    for file in python_files:
        data = pd.read_json(file,
                            orient="records",
                            compression="gzip",
                            lines=True)[["docstring", "url"]]
        for index, row in data.iterrows():
            if "test" in str(file):
                test_dataset.append({"query": row["docstring"], "location": row["url"]})
            else:
                train_dataset.append({"query": row["docstring"], "location": row["url"]})

    return train_dataset, test_dataset
