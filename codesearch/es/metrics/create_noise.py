from collections import Counter
import re
from typing import Dict, List

import numpy as np
from nltk.corpus import wordnet


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
