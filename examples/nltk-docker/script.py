#!/usr/bin/env python

import nltk
from nltk.corpus import brown, gutenberg, reuters, inaugural

import random
import sys


def main(corpus):
    lookup = {
        "brown": brown,
        "gutenberg": gutenberg,
        "reuters": reuters,
        "inaugural": inaugural,
    }
    if corpus not in lookup:
        sys.exit(f"Cannot find {corpus} in lookup. Choose from {list(lookup.keys())}")

    # Get the corpus, choose a random file
    corpus = lookup[corpus]
    fileid = random.choice(corpus.fileids())

    # Randomly select a sentence
    sentence = random.choice(list(corpus.sents(fileid)))
    print(" ".join(sentence))


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        corpus = "brown"
    else:
        corpus = sys.argv[1]
    main(corpus)
