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
            rate = self.get_rate(original,book)
            new_list_names[books_names[book]] = rate
            new_list_ids[book] = rate
        sorted_dict_names = dict(sorted(new_list_names.items(), key=lambda item: item[1],reverse = True))
        sorted_dict_ids = dict(sorted(new_list_ids.items(), key=lambda item: item[1],reverse = True))
        return sorted_dict_names,sorted_dict_ids

    def get_rate(self,book1,book2):
        topics_list1 = self.es.get_book_reduced_topics(book1)
        topics_list2 = self.es.get_book_reduced_topics(book2)
        score = {}

        count = 0
        # threshold = 0.50     # if needed
        for key in topics_list1:
            for word in topics_list2:
                if word not in score:
                    score[word]=0

                s = float(self.nb.similarity_score(key,word))
                # print(key,word+" = "+str(s)+" "+str(score[word]))
                if s > score[word]:
                    score[word] = s
        return int((sum(score.values())/len(score))*100)
