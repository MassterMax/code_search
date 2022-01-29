import os

from pprint import pprint
from preprocess.sources import GitSource, FolderSource
from preprocess.mappers.files import extract_function_identifiers_from_file
from preprocess.filters.entities import children_count_gt

from typing import Iterator, Tuple

from cytoolz import groupby

from preprocess.sources import ZipSource
from preprocess.mappers.files import extract_function_trees
# To extract class identifiers simply use another prebuilt extractor
# from preprocess.mappers.files import extract_class_trees
from preprocess.extractors.tree_sitter import TreeEntity


# To extract class identifiers simply use another prebuilt extractor
# from preprocess.mappers.files import extract_class_identifiers_from_file
from preprocess.utils import ProgrammingLanguages


def v2():
    directory = os.getcwd()

    function_identifiers = (
        # GitSource(f"{directory}/repositories.txt")
        FolderSource("/mnt/c/Users/maxma/Documents/GitHub/sandbox-course-work/")
            # Get the sequence of files
            .files_chain
            # Extract functions from files and flatten them
            .flat_map(extract_function_identifiers_from_file)
            # To extract identifiers from classes use
            # .flat_map(extract_class_identifiers_from_file)
            # Extract functions/classes with 10 or more identifiers
            .filter(children_count_gt(10))
            # Iterate over elements, by default iteration happens over batches
            .elements()
    )

    # Do further processing with function identifiers
    for identifier in function_identifiers:
        print(f"Function file: {identifier.file.repo}/{identifier.file.file}")
        print(f"Function identifiers: {' '.join([c.body for c in identifier.children])}")
        # print(f"Function identifier: {identifier}")
        print(f"Function first line: {identifier.start_line}")
        print(f"Function type: {identifier.type}")
        print(f"Function script: {identifier.file.file}")
        print(f"Function language: {identifier.file.language}")
        # print(f"Function entity name: {identifier.entity_name()}")
        print()


# todo что будет на другом языке?
def v1():
    def traverse_tree(entity: TreeEntity, level: int = 0) -> Iterator[Tuple[int, TreeEntity]]:
        """Yield tree structure with depth level"""
        yield level, entity
        for child in entity.children:
            yield from traverse_tree(child, level + 1)

    directory = os.getcwd()
    function_trees_identifiers = (
        GitSource(f"{directory}/repositories.txt")
        #FolderSource("/mnt/c/Users/maxma/Documents/GitHub/sandbox-course-work/")
            # Construct files sequence
            .files_chain
            # Extract function trees
            .flat_map(extract_function_trees)
            # Iterate over elements, by default iteration happens over batches
            .elements()
    )

    def get_str(ident):
        return code_file.code_bytes[ident[1].start_byte: ident[1].end_byte].decode()

    def get_function_name(_identifiers):
        for i in _identifiers:
            if i[1].type == 'identifier':
                return get_str(i)

    def get_parameters(_identifiers):
        arr = []
        for i in _identifiers:
            if i[1].type in {'identifier', 'typed_parameter'}:
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

    # Do further processing with function trees
    # For example: output types of entities grouped by depth
    for tree_identifier in function_trees_identifiers:
        code_file = tree_identifier.file
        lang: ProgrammingLanguages = tree_identifier.file.language
        data = {'start_line': tree_identifier.start_line,
                'location': f'{tree_identifier.file.repo}/{tree_identifier.file.file}',
                'language': lang.value,
                'identifiers': []}

        # Group nodes by level for nice output
        tree_nodes_by_depth = groupby(lambda i: i[0], traverse_tree(tree_identifier))
        print(f"Identifier: {tree_identifier.file.repo}/{tree_identifier.file.file}#L{tree_identifier.start_line}")
        # print("Structure:")
        for level, identifiers in sorted(tree_nodes_by_depth.items()):
            # print(f"L{level}: {'; '.join([i[1].type + ' ' + get_str(i) for i in identifiers])}")
            data['identifiers'].extend(get_identifiers(identifiers))
            if level == 1:
                data['function_name'] = get_function_name(identifiers)
            if level == 2:
                data['parameters'] = get_parameters(identifiers)
            if level == 3:
                docstring: str = get_docstring(identifiers)
                # todo comment this - because solution is not optimal
                if docstring:
                    docstring = docstring.replace("  ", "")
                    docstring = docstring.replace("\n", " ")
                    docstring = docstring.replace("\r", "")
                    docstring = docstring.replace('"', '')
                    docstring = docstring.replace("  ", " ")
                    docstring = docstring.replace("  ", " ")
                    docstring = docstring.strip()
                data['docstring'] = docstring

        pprint(data)
        print("\n" * 3)
        # return


if __name__ == '__main__':
    v1()

# self.file.code_bytes[self.start_byte : self.end_byte].decode()
# Node.start_byte Node.end_byte -> name
