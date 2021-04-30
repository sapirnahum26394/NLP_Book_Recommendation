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
    def find_books_by_book_id(self,mms_id,lamda = 1):
        synonym = self.es.get_book_synonym(mms_id)
        if len(synonym)<lamda:
            lamda = len(synonym)
        synonym = self.es.get_books_by_common_synonym(synonym,lamda)
        del synonym[str(mms_id)]
        books = []
        for book in synonym:
            books.append(book)
        books_names = {}
        for book in synonym:
            books_names[book] = synonym[book][0]
        return books,books_names


    def find_books_by_token(self,token,lamda = 2):
        synonym = self.es.get_synonym_index_by_token(token)
        return self.es.get_books_by_common_synonym(synonym,lamda)
