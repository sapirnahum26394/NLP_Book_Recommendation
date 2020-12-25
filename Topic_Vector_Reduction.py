"""
Final Project
Software engineering department

Authors:
Sapir Nahum
Shmuel Eliasyan
"""

"""
===================================================================================================
Imports
===================================================================================================
"""
import nltk
from nltk.corpus import wordnet
import requests


class Vector_reduction():
    """
    ===================================================================================================
    Init
    ===================================================================================================
    """
    def __init__(self,vector):
        self.conceptNet = self.normalize_words_vector_conceptnet(vector)
        self.wordNet = self.normalize_words_vector_wordnet(vector)
        self.conceptNetAndWordNet = self.normalize_words_vector_conceptnet(vector)
        self.conceptNetAndWordNet = self.normalize_words_vector_wordnet(self.conceptNetAndWordNet)


    """
    ===================================================================================================
    Functions
    ===================================================================================================
    """

    def normalize_words_vector_wordnet(self,words_vector):
        nltk.download('wordnet')
        expanded_words_vector = []
        words_vector_copy = words_vector.copy();
        for word in words_vector_copy:
            if word in expanded_words_vector:
                words_vector.remove(word)
                continue
            syn_sets = wordnet.synsets(word)
            for syn_set in syn_sets:
                for name in syn_set._lemma_names:
                    if name not in expanded_words_vector:
                        expanded_words_vector.append(name)
        return words_vector


    def normalize_words_vector_conceptnet(self,words_vector):
        words_vector_copy = words_vector.copy();
        for first_word_index in range(0, len(words_vector_copy)):
            for second_word_index in range(first_word_index + 1, len(words_vector_copy)):
                url = self.parse_conceptnet_url(words_vector_copy[first_word_index], words_vector_copy[second_word_index]);
                synonyms_json_obj = requests.get(url).json();
                if len(synonyms_json_obj['edges']):
                    words_vector.remove(words_vector_copy[first_word_index])
                    break;
        return words_vector


    def parse_conceptnet_url(self,first_word, second_word):
        return "http://api.conceptnet.io/query?node=/c/en/" + first_word + \
               "&other=/c/en/" + second_word + "&rel=/r/Synonym&limit=1";
