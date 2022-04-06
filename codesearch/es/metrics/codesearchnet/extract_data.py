from pathlib import Path
from typing import Any, Dict, Iterator, List

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


def make_dataset_for_evaluation(path_to_dataset_folder: str):
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
