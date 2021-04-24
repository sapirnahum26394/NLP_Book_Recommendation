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
from Number_batch import number_batch
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
            rate = self.get_rate(original,book)
            new_list_names[books_names[book]] = rate
            new_list_ids[book] = rate
        sorted_dict_names = dict(sorted(new_list_names.items(), key=lambda item: item[1],reverse = True))
        sorted_dict_ids = dict(sorted(new_list_ids.items(), key=lambda item: item[1],reverse = True))
        return sorted_dict_names,sorted_dict_ids

    def get_rate(self,book1,book2):
        topics_list1 = self.es.get_book_topics(book1)
        topics_list2 = self.es.get_book_topics(book2)
        score = {}
        print(topics_list1)
        print(topics_list2)
        count = 0
        # threshold = 0.50     # if needed
        for key in topics_list1:
            for word in topics_list2:
                score[word] = 0
                try:
                    s = self.nb.similarity_score(key,word)
                except:
                    s = 0
                # print(key,word+" = "+str(s))
                if s is not None and s > score[word]:
                    score[word] = s
        print(score)
        print(sum(score.values())/len(score))
        return sum(score.values())/len(score)
