# todo - WIP
from pathlib import Path
from pprint import pprint

from preprocess.mappers.utils import TokenParser
import pandas as pd
from typing import Any, Dict, List

parser = TokenParser()
PATH_TO_DATASET = "/mnt/c/Users/maxma/Desktop/dataset/"

python_files = sorted(Path(PATH_TO_DATASET).glob("**/*.gz"))
columns_long_list = ['repo', 'path', 'url', 'code',
                     'code_tokens', 'docstring', 'docstring_tokens',
                     'language', 'partition']

f = python_files[0]
print(f)
# for el in python_files:
#     print(el)
#     print(type(el))

data = pd.read_json(f,
                    orient='records',
                    compression='gzip',
                    lines=True)

values = data.values.tolist()


DATASET_TO_ELASTIC_MAPPING = {
    "code": "function_body",
    "code_tokens": "identifiers",
    "docstring": "docstring",
    "url": "location",
    "func_name": "function_name"
}


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


print(data.columns.tolist())
pprint(values[0])
prepared = prepare_entity_to_elastic(data.columns.tolist(), values[0])
pprint(prepared)
