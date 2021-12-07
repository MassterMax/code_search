import json
import os
import re
from subprocess import PIPE, run
import shutil
from pathlib import Path

#
# Пока что просто набор методов!
#

IGNORE_RULES = {"__init__", "__len__"}


def call_buckwheat():
    os.system(f'python3 -m {path_to_buckwheat} -i /repositories.txt -o /buckwheat_output --files')


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

    with open(f"buckwheat_output/docword0.txt") as fin:
        lines = fin.read().splitlines()
        d = {}
        for line in lines:
            if ';' not in line:
                url = line
                d[url] = {}
            else:
                names = re.split("[,;]", line)
                path = names[0]  # is a path
                d[url][path] = []
                for el in names[1:]:
                    if el not in IGNORE_RULES:
                        d[url][path].append(el)

                if len(d[url][path]) == 0:
                    del d[url][path]

                if len(d[url]) == 0:
                    del d[url]

    with open('result.json', 'w') as fp:
        json.dump(d, fp)


def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout


if __name__ == "__main__":
    current_dir = os.getcwd()
    path_to_buckwheat = f'{Path(current_dir).parents[1]}/buckwheat'

    os.chdir(path_to_buckwheat)

    val = os.popen('pwd').read().strip()
    assert val == path_to_buckwheat, f'{val}!={path_to_buckwheat}'

    shutil.rmtree(f'{current_dir}/buckwheat_output')
    val = os.popen(
        f'python3 -m identifiers_extractor.run -i {current_dir}/repositories.txt -o {current_dir}/buckwheat_output --files').read()

    print(val)

    os.chdir(current_dir)
    val = os.popen('pwd').read().strip()
    assert val == current_dir, f'{val}!={current_dir}'

    convert_to_json()
