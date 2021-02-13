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
from Elastic_search import elasticsearch



class find_books():
    """
    ===================================================================================================
    Init
    ===================================================================================================
    """
    def __init__(self):
        self.es = elasticsearch()


    """
    ===================================================================================================
    Functions
    ===================================================================================================
    """
    def find_books_by_book_id(self,mms_id,lamda = 2):
        synonym = self.es.get_book_synonym(mms_id)
        synonym = self.es.get_books_by_common_synonym(synonym,lamda)
        print(synonym)
        del synonym[str(mms_id)]
        books={}
        for book in synonym:
            books[book] = synonym[book][0]
        return books


    def find_books_by_token(self,token,lamda = 1):
        synonym = self.es.get_synonym_index_by_token(token)
        return self.es.get_books_by_common_synonym(synonym,lamda)
