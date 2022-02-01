import json
import os
import shutil
import time
from pathlib import Path
from typing import Iterator, Tuple, Dict, Type, List
import datetime
import pandas as pd
from cytoolz import groupby
from git import Repo
from preprocess.extractors.tree_sitter import TreeEntity
from preprocess.mappers.files import extract_function_trees
from preprocess.sources import GitSource, FolderSource
from preprocess.utils import ProgrammingLanguages

from codesearch.preproc.languages import CppRules, PythonRules, LanguageRules

# list of all supported languages
LANGUAGES: Dict[str, Type[LanguageRules]] = {PythonRules.name: PythonRules, CppRules.name: CppRules}


def extract_from_csv(_csv_path: str, _storage_path: str, _output_directory: str, _one_file_size: int = 2 * 1024):
    """
    A function to extract data from git repo with provided csv
    Args:
        _csv_path: path to csv file
        _storage_path: a directory where tmp folder with repos will be created
        _output_directory: a directory where .json file will be stored
        _one_file_size: maximum size of one produced .json file in megabytes

    Returns:

    """

    t = time.time()
    start_datetime = datetime.datetime.now()
    total_size = 0
    exceptions = 0
    cnt = 0
    data_to_write = []

    df = pd.read_csv(_csv_path, header=[0])
    temp_path = f'{_storage_path}/tmp'
    Path(temp_path).mkdir()  # there will be an exception if folder already exists

    skip = 9980
    for index, row in df.iterrows():
        skip -= 1
        if skip > 0:
            continue

        owner = row['owner']
        name = row['name']
        url = f'https://github.com/{owner}/{name}'
        repo_path = f'{temp_path}/{owner}_{name}'
        print(f"processing: {url}")

        try:
            repo = Repo.clone_from(url, repo_path)
            total_size += os.path.getsize(repo_path)

            data = extract_data(temp_path)
            for el in data:
                el['location'] = f'{url}/blob/{repo.commit()}/{el["location"]}'
                el['stargazers_count'] = row['stargazers_count']
                el['repo_id'] = row['repo_id']

            data_to_write.extend(data)
            current_dict_size = len(json.dumps(data_to_write))
            if current_dict_size > _one_file_size * 1024 * 1024 or df.shape[0] - 1 == index:
                # data[DATA_KEY].append(extract_data(path)[DATA_KEY])
                with open(f'{_output_directory}/{cnt}.json', 'w') as fp:
                    json.dump(data_to_write, fp)
                cnt += 1
                data_to_write = []
            print('success!')
        except Exception as e:
            print(f"exception occurred: {e}")
            exceptions += 1

        shutil.rmtree(repo_path, True)

    shutil.rmtree(temp_path, True)
    print(f"started at: {start_datetime}, current time: {datetime.datetime.now()}")
    print(f"the whole process took {time.time() - t} seconds with {exceptions} exception(s)")
    print(f"download totally {total_size}b which is {total_size / 1024 / 1024}mb")


def extract_data(repositories_path: str, from_git: bool = False) -> List[Dict]:
    def traverse_tree(entity: TreeEntity, _level: int = 0) -> Iterator[Tuple[int, TreeEntity]]:
        """Yield tree structure with depth level"""
        yield _level, entity
        for child in entity.children:
            yield from traverse_tree(child, _level + 1)

    def get_str(ident):
        return code_file.code_bytes[ident[1].start_byte: ident[1].end_byte].decode()

    def get_function_name(_identifiers):
        for i in _identifiers:
            if i[1].type == 'identifier':
                return get_str(i)

    def get_parameters(_identifiers, language: Type[LanguageRules]):
        arr = []
        for i in _identifiers:
            if i[1].type in language.parameter_node:
                arr.append(get_str(i))
        return arr

    def get_docstring(_identifiers):
        for i in _identifiers:
            if i[1].type == 'string':
                return get_str(i)

    def get_identifiers(_identifiers):
        arr = []
        for i in _identifiers:
            if i[1].type == 'identifier':
                arr.append(get_str(i))
        return arr

    all_functions = []

    source = GitSource(repositories_path) if from_git else FolderSource(repositories_path)

    function_trees_identifiers = (
        source
            # Construct files sequence
            .files_chain
            # Extract function trees
            .flat_map(extract_function_trees)
            # Iterate over elements, by default iteration happens over batches
            .elements()
    )

    for tree_identifier in function_trees_identifiers:
        code_file = tree_identifier.file
        lang: ProgrammingLanguages = tree_identifier.file.language
        data = {'start_line': tree_identifier.start_line,
                'location': f'{tree_identifier.file.file}',
                'language': lang.value,
                'identifiers': []}

        if lang.value not in LANGUAGES:
            print(f"language is not supported yet: {lang.value} for file {data['location']}")
            continue

        # Group nodes by level for nice output
        tree_nodes_by_depth = groupby(lambda i: i[0], traverse_tree(tree_identifier))

        for level, identifiers in sorted(tree_nodes_by_depth.items()):
            # print(f"L{level}: {'; '.join([i[1].type + ' ' + get_str(i) for i in identifiers])}")  # todo debug string

            # get all identifiers
            data['identifiers'].extend(get_identifiers(identifiers))

            # get function name
            if level == LANGUAGES[lang.value].function_name_level:
                data['function_name'] = get_function_name(identifiers)

            # get function parameters
            if level == LANGUAGES[lang.value].parameter_level:
                data['parameters'] = get_parameters(identifiers, LANGUAGES[lang.value])

            # get docstring
            if level == 3:
                docstring: str = get_docstring(identifiers)
                # maybe another solution?
                if docstring:
                    docstring = " ".join(docstring.split())
                    docstring = docstring.replace('\"', '')
                data['docstring'] = docstring

        all_functions.append(data)

    return all_functions


if __name__ == '__main__':
    directory = os.getcwd()
    csv_path = f"{directory}/repositories.csv"
    storage_path = "/mnt/c/Users/maxma/Documents"

    extract_from_csv(csv_path, storage_path, directory, 1)
