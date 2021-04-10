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
from BackEnd.classes.Elastic_search import elasticsearch
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
        score = {}
        # threshold = 0.50     # if needed
        for key in topics_list1:
            score[key] = 0
            for word in topics_list2:
                x = wordnet.synsets(key)
                y = wordnet.synsets(word)
                if not x or not y:
                    continue
                s = x[0].wup_similarity(y[0])
                if s is not None and s > score[key]:
                    score[key] = s

        return sum(score.values())/len(score.values())
