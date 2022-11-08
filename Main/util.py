from tokenizer import selectTokenizer
import spacy
from ngram import *


def cleanToken(token):
    punk = ".\",'()\n"
    for i in token:
        if i in punk:
            token.remove(i)

    return token


def cat(token):
    return (" ".join(token))


