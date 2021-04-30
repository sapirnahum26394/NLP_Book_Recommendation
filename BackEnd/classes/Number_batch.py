"""
Final Project
Software engineering department

Authors:
Sapir Nahum
Shmuel Eliasyan
"""
from gensim.models import KeyedVectors
import wordfreq
import re
"""
===================================================================================================
Imports
===================================================================================================
"""


class number_batch():
    """
    ===================================================================================================
    Init
    ===================================================================================================
    """

    def __init__(self):
        self.number_batch_path = "../files/number_batch/numberbatch-en.txt"
        self.number_batch_model = ""
        self.load_model()
        # English-specific stopword handling
        self.STOPWORDS = ['the', 'a', 'an']
        self.DROP_FIRST = ['to']
        self.DOUBLE_DIGIT_RE = re.compile(r'[0-9][0-9]')
        self.DIGIT_RE = re.compile(r'[0-9]')


    """
    ===================================================================================================
    Functions
    ===================================================================================================
    """

    def load_model(self):
        try:
            self.number_batch_model = KeyedVectors.load("files/number_batch/numberbatch.model")
        except:
            print("model file not exist, creating a new model file")
            self.number_batch_model = KeyedVectors.load_word2vec_format(
                self.number_batch_path,
                binary=False,
                unicode_errors='ignore'
            )
            self.number_batch_model.save("files/number_batch/numberbatch.model")

    def find_similar_words(self,term,number_of_words):
        try:
            list = self.number_batch_model.most_similar(term, topn=number_of_words)
            newList=[]
            for (word,score) in list:
                newList.append(word)
            return newList
        except:
            print("Error with model in 'find_similar_words'")


    def similarity_score(self,term1,term2):
        try:
            return self.number_batch_model.similarity(term1, term2)
        except:
            return 0