"""
Final Project
Software engineering department

Authors:
Sapir Nahum
Shmuel Eliasyan
"""
import math
import numpy as np

"""
===================================================================================================
Imports
===================================================================================================
"""
from BackEnd.classes.Elastic_search import elasticsearch
from BackEnd.classes.Number_batch import number_batch
class rate_books():
    """
    ===================================================================================================
    Functions
    ===================================================================================================
    """

    def __init__(self):
        self.nb = number_batch()
        self.es = elasticsearch()

    def get_books_by_rate(self,original,list,books_names):
        new_list_names = {}
        new_list_ids = {}
        for book in list:
            rate = self.cosine_similarity(original,book)
            if rate > 0.2:
                rate = self.get_rate(original,book)
                new_list_names[book] = books_names[book]
                new_list_ids[book] = rate
        sorted_dict_names = dict(sorted(new_list_names.items(), key=lambda item: item[1], reverse = True))
        sorted_dict_ids = dict(sorted(new_list_ids.items(), key=lambda item: item[1], reverse = True))
        return sorted_dict_names,sorted_dict_ids

    def get_rate(self,book1,book2):
        topics_list1 = self.es.get_book_reduced_topics(book1)
        topics_list2 = self.es.get_book_reduced_topics(book2)
        score = {}
        count = len(topics_list2)+len(topics_list1)
        # threshold = 0.50     # if needed
        for key in topics_list1:
            for word in topics_list2:
                if word not in score:
                    score[word]=0

                s = float(self.nb.similarity_score(key,word))
                if s > score[word]:
                    score[word] = s
        for word in score:
            if score[word] > 0.3:
                count -= 1
        return sum(score.values())/count

    def get_wights(self,mms_id):
        wights = {}
        topics_list = self.es.get_book_normalized_topics(mms_id)
        synonym = self.es.get_book_synonym_lists(mms_id)
        syn_ids = self.es.get_book_synonym(mms_id)
        for (syn, syn_id) in zip(synonym, syn_ids):
            for token in topics_list:
                if token in syn:
                    if syn_id in wights:
                        wights[syn_id] += 1 / len(synonym)
                    else:
                        wights[syn_id] = 1 / len(synonym)
        return wights

    def create_vector(self,book_synonyms,topics):
        synonyms = self.es.get_all_synonym()
        syn_vector = {}
        for i in synonyms:
            syn_vector[i['_id']] = 0

        for s in book_synonyms:
            list_of_syn = self.es.get_synonym_by_id(s)
            for t in topics:
                if t in list_of_syn:
                    syn_vector[s] += 1
        return np.array(list(syn_vector.values()))

    def cosine_similarity(self, book1, book2):

        synonyms1 = self.es.get_book_synonym(book1)
        topics1 = self.es.get_book_normalized_topics(book1)
        synonyms2 = self.es.get_book_synonym(book2)
        topics2 = self.es.get_book_normalized_topics(book2)

        syn_vector1 = self.create_vector(synonyms1,topics1)
        syn_vector2 = self.create_vector(synonyms2,topics2)

        sum = np.dot(syn_vector1, syn_vector2)/(math.sqrt(len(synonyms1))*math.sqrt(len(synonyms2)))

        return sum