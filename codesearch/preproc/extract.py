import datetime
import json
from pathlib import Path
import shutil
from typing import Dict, Iterator, List, Tuple, Type

from cytoolz import groupby
from git import GitCommandError, Repo
import pandas as pd
from preprocess.extractors.tree_sitter import TreeEntity
from preprocess.mappers.files import extract_function_trees
from preprocess.mappers.utils import TokenParser
from preprocess.sources import FolderSource, GitSource
from preprocess.utils import ProgrammingLanguages
from tqdm import tqdm

from codesearch.preproc.languages import CppRules, LanguageRules, PythonRules

# list of all supported languages
LANGUAGES: Dict[str, Type[LanguageRules]] = {
    PythonRules.name: PythonRules,
    CppRules.name: CppRules
}

parser = TokenParser()


def extract_from_csv(csv_path: str, storage_path: str, output_directory: str, one_file_size: int = 1024):
    """
    A function to extract data from git repo with provided csv
    Args:
        csv_path: path to csv file
        storage_path: a directory where tmp folder with repos will be created
        output_directory: a directory where .json file will be stored
        one_file_size: maximum size of one produced .json file in megabytes

    Returns: nothing
    """

    exceptions = 0
    output_files_cnt = 0
    one_file_size = int(one_file_size)
    data_to_write = []

    df = pd.read_csv(csv_path, header=[0])
    temp_path = f'{storage_path}/tmp'
    Path(temp_path).mkdir()  # there will be an exception if folder already exists

    for index, row in tqdm(df.iterrows()):
        owner = row['owner']
        name = row['name']
        url = f'https://github.com/{owner}/{name}'
        repo_path = f'{temp_path}/{owner}_{name}'
        print(f"processing {url} at {datetime.datetime.now()}")

        try:
            repo = Repo.clone_from(url.replace("https://", "https://null:null@"), repo_path)

            data = extract_data(temp_path)
            for el in data:
                el['location'] = f'{url}/blob/{repo.commit()}/{el["location"]}'
                el['stargazers_count'] = row['stargazers_count']
                el['repo_id'] = row['repo_id']

            data_to_write.extend(data)
            current_dict_size = len(json.dumps(data_to_write))
            if current_dict_size > one_file_size * 1024 * 1024:
                with open(f'{output_directory}/{output_files_cnt}.json', 'w+') as fp:
                    json.dump(data_to_write, fp)
                output_files_cnt += 1
                data_to_write = []
        except GitCommandError as e:
            print(f"{url}: exception occurred - {e}")
            exceptions += 1

        shutil.rmtree(repo_path, True)

    # save residual data
    if len(json.dumps(data_to_write)) > 2:
        with open(f'{output_directory}/{output_files_cnt}.json', 'w+') as fp:
            json.dump(data_to_write, fp)

    shutil.rmtree(temp_path, True)
    print(f"the whole process ends with {exceptions} exception(s)")


def extract_data(repositories_path: str, from_git: bool = False) -> List[Dict]:
    """
    A method to extract function data from git/in-storage repo and return all entities in List
    Args:
        repositories_path: path to folder with git projects or path to file with git links
        from_git: False = given path is folder with projects, otherwise - it is a file with links

    Returns: list of all extracted function entities as
    """

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
                'identifiers': [],
                'split_identifiers': [],
                'function_body': get_str(tree_identifier)}

        if lang.value not in LANGUAGES:
            continue

        # Group nodes by level for nice output
        tree_nodes_by_depth = groupby(lambda i: i[0], traverse_tree(tree_identifier))

        for level, identifiers in sorted(tree_nodes_by_depth.items()):
            # get all identifiers
            current_identifiers = get_identifiers(identifiers)
            data['identifiers'].extend(current_identifiers)
            split_identifiers = []
            for el in current_identifiers:
                split_identifiers.extend(list(parser.split(el)))
            data['split_identifiers'].extend(split_identifiers)

            # get function name
            if level == LANGUAGES[lang.value].function_name_level:
                data['function_name'] = get_function_name(identifiers)

            # get function parameters
            if level == LANGUAGES[lang.value].parameter_level:
                data['arguments'] = get_parameters(identifiers, LANGUAGES[lang.value])

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
