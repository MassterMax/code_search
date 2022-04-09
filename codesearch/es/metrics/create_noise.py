from collections import Counter
import re
from typing import Dict, List

import nltk
import numpy as np

from codesearch.es.metrics.utils import timer

nltk.download('omw-1.4')
nltk.download('wordnet')
from nltk.corpus import wordnet


@timer
def generate_synonyms(word: str):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.name() != word:
                synonyms.add(lemma.name())
    return list(synonyms)


def get_most_common_synonyms(texts: List[str], n_top_common: int = 100, max_count: int = 10):
    most_words = Counter()
    for text in texts:
        for word in re.findall(r'\w+', text):
            most_words[word.lower()] += 1

    most_synonyms = {}
    for word, frequency in most_words.most_common():
        synonyms = generate_synonyms(word)[:max_count]
        if len(synonyms) > 0:
            most_synonyms[word] = synonyms
        if len(most_synonyms) == n_top_common:
            break

    return most_synonyms


def corrupt_text(text: str, synonyms: Dict[str, List[str]], probability: float, corrupt_if_unique: bool = True):
    for word in re.findall(r"\w+", text):
        if np.random.binomial(1, probability):
            if word in synonyms:
                text = text.replace(word, np.random.choice(synonyms[word]))
            elif corrupt_if_unique:
                pos = np.random.randint(0, len(word))
                text = text.replace(word, word[:pos] + "#" + word[pos + 1:])
    return text


# todo remove after debug
if __name__ == '__main__':
    text_list = [
        """ repo_name: name of GitHub repo like "scikit-learn/scikit-learn"
        max_user_stars: only max_user_stars starred repo from each user counts
        n_top_repos: returns this number of most popular repos""",

        """ A method that does following:
    1. get all GitHub repo stargazers (list)
    2. for each stargazer get all of his starred repos
    3. for""",

        """A method that calculates how much time until GitHub api limit breaks
    Args:
        github: GitHub instance
    Returns: estimated time to api reset in seconds
        """
    ]

    data = get_most_common_synonyms(text_list, 20)
    new_text = corrupt_text(text_list[0], data, 0.15)
    print(text_list[0])
    print(new_text)
