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
import requests
from nltk.corpus import wordnet as wn


class Find_similar_topics():
    """
    ===================================================================================================
    Init
    ===================================================================================================
    """
    # def __init__(self):

    """
    ===================================================================================================
    Functions
    ===================================================================================================
    """
    # def expaned_vector_with_conceptNet(self):
    #     temp=self.vector.copy()
    #     for word in self.vector:
    #         obj = requests.get('http://api.conceptnet.io/query?node =/c/en/' + word + '?rel=/r/Synonym&limit=20').json()
    #         words = [edge['end']['label'] for edge in obj['edges']]
    #         words = list(dict.fromkeys(words))
    #         # print(word)
    #         # print(words)
    #         temp.append(words)
    #     # print(temp)

    def get_synonyms_list(self, word):
        synonyms = []
        for syn in wn.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
        return list(dict.fromkeys(synonyms))

