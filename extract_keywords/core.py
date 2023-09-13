# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['read_in_text', 'is_word_in_range', 'remove_singular_words', 'extract_keywords']

# %% ../nbs/00_core.ipynb 3
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer
from functools import partial

# %% ../nbs/00_core.ipynb 4
def read_in_text(file_path:str): # path of text file
    "Read in the text file"
    with open(file_path, 'r') as f: return f.read()

# %% ../nbs/00_core.ipynb 5
def is_word_in_range(word:str, # input word
                     min_len:int, # Min length of word
                     max_len:int): # Max length of word
    "returns True if word is in range (min_len, max_len) both inclusive"
    if (len(word) <= max_len) and (len(word) >= min_len): return True
    else: return False

# %% ../nbs/00_core.ipynb 12
def remove_singular_words(word_list:list): # List of words
    "Removes singular words when they have a corresponding plural word in a list of words."
    plural_words = set()
    singular_words = []
    
    for word in word_list:
        # Check if the word is in plural form by adding 's'
        plural_form = word + 's'
        
        if plural_form in word_list:
            # If the plural form is in the list, add it to the set of plural words
            plural_words.add(plural_form)
        else:
            # If the word is not in plural form, add it to the list of singular words
            singular_words.append(word)
    
    return singular_words

# %% ../nbs/00_core.ipynb 15
def extract_keywords(text:str, # input text
                     n:int, # number of keywords
                     min_len:int, # minimum length of word
                     max_len:int): # maximum length of word
    "Extract n keywords from text in range (min_len, max_len) both inclusive"
    kw_extractor = KeyBERT('valurank/MiniLM-L6-Keyword-Extraction')
    keywords = kw_extractor.extract_keywords(text, vectorizer=KeyphraseCountVectorizer(), stop_words=None, top_n=n*2)
    keywords = [i for i,j in keywords] #removing confidence score
    keywords = remove_singular_words(keywords)
    keywords = [word for word in keywords if is_word_in_range(word, min_len=4, max_len=16)]
    return keywords[:n]
