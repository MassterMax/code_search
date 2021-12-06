import os
import subprocess
from subprocess import PIPE, run

from prompt_toolkit import prompt

PATH_TO_BUCKWHEAT = "/mnt/c/Users/maxma/Documents/GitHub/buckwheat"
IGNORE_RULES = ["__init__", "__len__"]


def call_buckwheat():
    os.system(f'python3 -m {PATH_TO_BUCKWHEAT} -i /repositories.txt -o /buckwheat_output --files')


def convert_to_json():
    # Expect files in buckwheat format:
    # REPOSITORY1
    # file1;method1,method2
    # file2;method1
    # REPOSITORY2
    # file1;method1,method2,method3
    #
    # Output:
    # {
    #  //doc1
    # }
    # {...}

    with open(f"/buckwheat_output/docword0.txt") as fin:
        lines = fin.read().splitlines()
        for line in lines:
            if ';' not in line:
                print(f'repository: {line}')
            else:
                line = line.replace(';', ',', 1)
                names = line.split(sep=',')
                print(f'\tfile: {names[0]}')
                for el in line[1:]:
                    print(f'\t\t'
                          f'function: {el}')


def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout


if __name__ == "__main__":
    current_dir = os.getcwd()
    os.chdir(PATH_TO_BUCKWHEAT)

    val = os.popen('pwd').read().strip()
    assert val == PATH_TO_BUCKWHEAT, f'{val}!={PATH_TO_BUCKWHEAT}'

    val = os.popen(f'python3 -m identifiers_extractor.run -i {current_dir}/repositories.txt -o {current_dir}/buckwheat_output --files').read()

    print(val)
    os.chdir(current_dir)
