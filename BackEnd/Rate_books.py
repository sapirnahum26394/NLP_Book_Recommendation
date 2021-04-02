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
from Find_similar import Find_similar_topics
from Elastic_search import elasticsearch
import spacy
from scipy import spatial
import collections
from gensim.models import Word2Vec
from nltk.corpus import wordnet
class rate_books():
    """
    ===================================================================================================
    Functions
    ===================================================================================================
    """

    def get_books_by_rate(self,original,list,books_names):
        new_list_names = {}
        new_list_ids = {}
        for book in list:
            rate = self.get_rate(original,book)
            new_list_names[books_names[book]] = rate
            new_list_ids[book] = rate
        sorted_dict_names = dict(sorted(new_list_names.items(), key=lambda item: item[1],reverse = True))
        sorted_dict_ids = dict(sorted(new_list_ids.items(), key=lambda item: item[1],reverse = True))
        return sorted_dict_names,sorted_dict_ids

    def get_rate(self,book1,book2):
        es = elasticsearch()
        topics_list1 = es.get_book_topics(book1)
        topics_list2 = es.get_book_topics(book2)
        score = 0
        threshold = 0.80     # if needed
        combineList= len(topics_list1) + len(topics_list2)
        for key in topics_list1:
            for word in topics_list2:
                x = wordnet.synsets(key)
                y = wordnet.synsets(word)
                if not x or not y:
                    continue
                s = x[0].wup_similarity(y[0])
                if s is not None:
                    score += s
                # print(key,", ",word," = ",s)
        return score/combineList







#     def rate2words(self,word1,word2):
#         # load the language model
#         nlp = spacy.load('en_core_web_md')
#
#         # convert the strings to spaCy Token objects
#         token1 = nlp(word1)[0]
#         token2 = nlp(word2)[0]
#         # compute word similarity
#         score = token1.similarity(token2)
#
#         print(word1,", ",word2," = ",score)
#         return score
#
#
#     def get_rate(self,book1,book2):
#         es = elasticsearch()
#         topics_list1 = es.get_book_topics(book1)
#         topics_list2 = es.get_book_topics(book2)
#         score = 0
#         threshold = 0.80     # if needed
#         combineList= list(set(topics_list1) | set(topics_list2))
#         for key in topics_list1:
#             for word in topics_list2:
# #               res = self.cosdis(self.word2vec(word), self.word2vec(key))
#                 res = self.rate2words(key,word)
#                 if res > threshold:
#                     score +=  res
#
#         return score/len(combineList)
#

#
#
#     def word2vec(self,word):
#         from collections import Counter
#         from math import sqrt
#
#         # count the characters in word
#         cw = Counter(word)
#         # precomputes a set of the different characters
#         sw = set(cw)
#         # precomputes the "length" of the word vector
#         lw = sqrt(sum(c*c for c in cw.values()))
#
#         # return a tuple
#         return cw, sw, lw
#
#     def cosdis(self,v1, v2):
#         # which characters are common to the two words?
#         common = v1[1].intersection(v2[1])
#         # by definition of cosine distance we have
#         return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]
#
#
