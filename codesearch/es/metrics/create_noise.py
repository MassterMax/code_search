import nltk

nltk.download('omw-1.4')
nltk.download('wordnet')
from nltk.corpus import wordnet


def generate_synonyms(word: str):
    synonyms = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
    return synonyms


w = "make"
s = generate_synonyms(w)
for el in s:
    print(el)
