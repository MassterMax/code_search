import json
import os
import time
from pprint import pprint
from typing import Iterator, Tuple, Dict, Type

from cytoolz import groupby
# To extract class identifiers simply use another prebuilt extractor
# from preprocess.mappers.files import extract_class_trees
from preprocess.extractors.tree_sitter import TreeEntity
from preprocess.mappers.files import extract_function_trees
from preprocess.sources import GitSource, FolderSource
# To extract class identifiers simply use another prebuilt extractor
# from preprocess.mappers.files import extract_class_identifiers_from_file
from preprocess.utils import ProgrammingLanguages

from codesearch.preproc.languages import CppRules, PythonRules, LanguageRules

# list of all supported languages
LANGUAGES: Dict[str, Type[LanguageRules]] = {PythonRules.name: PythonRules, CppRules.name: CppRules}


def extract_data(repositories_path: str, output_directory: str, git_location: bool = True):
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

    all_functions = {'extracted': []}

    function_trees_identifiers = (
        # FolderSource(repositories_path)
        GitSource(repositories_path)
            # Construct files sequence
            .files_chain
            # Extract function trees
            .flat_map(extract_function_trees)
            # Iterate over elements, by default iteration happens over batches
            .elements()
    )

    # Do further processing with function trees
    # For example: output types of entities grouped by depth
    for tree_identifier in function_trees_identifiers:
        code_file = tree_identifier.file
        lang: ProgrammingLanguages = tree_identifier.file.language
        data = {'start_line': tree_identifier.start_line,
                'location': f'{tree_identifier.file.repo}/{tree_identifier.file.file}',
                'language': lang.value,
                'identifiers': []}

        if git_location:
            repo = tree_identifier.file.repo.replace('-', '/', 1)
            file = tree_identifier.file.file
            data['location'] = f'https://github.com/{repo}/blob/main/{file}'

        assert lang.value in LANGUAGES, f"language not supported: {lang.value}"

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
                    docstring = docstring.replace("  ", "")
                    docstring = docstring.replace("\n", " ")
                    docstring = docstring.replace("\r", "")
                    docstring = docstring.replace('"', '')
                    docstring = docstring.replace("  ", " ")
                    docstring = docstring.replace("  ", " ")
                    docstring = docstring.strip()
                data['docstring'] = docstring

        all_functions['extracted'].append(data)

    with open(f'{output_directory}/result.json', 'w') as fp:
        json.dump(all_functions, fp)


if __name__ == '__main__':
    directory = os.getcwd()
    path = f"{directory}/repositories.txt"
    # path = "/mnt/c/Users/maxma/Documents/tmp"
    extract_data(path, directory, False)
