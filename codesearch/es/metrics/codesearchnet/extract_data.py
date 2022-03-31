from pathlib import Path
from pprint import pprint

from preprocess.mappers.utils import TokenParser
import pandas as pd
from typing import Any, Dict, List

parser = TokenParser()
PATH_TO_DATASET = "/mnt/c/Users/maxma/Desktop/dataset/"  # todo remove
DATASET_TO_ELASTIC_MAPPING = {
    "code": "function_body",
    "code_tokens": "identifiers",
    "docstring": "docstring",
    "url": "location",
    "func_name": "function_name"
}


def dataset_to_elastic(path_to_dataset: str = PATH_TO_DATASET) -> List[Dict[str, Any]]:
    python_files = sorted(Path(path_to_dataset).glob("**/*.gz"))

    # todo now get first file, then get all files
    file = python_files[0]
    print(f"extract data from: {file}")

    data = pd.read_json(file,
                        orient='records',
                        compression='gzip',
                        lines=True)

    values = data.values.tolist()
    print(f"columns: {data.columns.tolist()}")

    return [prepare_entity_to_elastic(data.columns.tolist(), value) for value in values]


def prepare_entity_to_elastic(columns: List[str], entity: List[str]) -> Dict[str, Any]:
    result = {}

    for column, value in zip(columns, entity):
        if column in DATASET_TO_ELASTIC_MAPPING:
            elastic_field = DATASET_TO_ELASTIC_MAPPING[column]
            result[elastic_field] = value

    result["split_identifiers"] = []
    for identifier in result["identifiers"]:
        result["split_identifiers"].extend(list(parser.split(identifier)))

    return result


if __name__ == "__main__":
    prepared_values = dataset_to_elastic()
    pprint(prepared_values[:5])
