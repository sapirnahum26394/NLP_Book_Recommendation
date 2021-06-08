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
    def find_books_by_book_id(self,mms_id):
        synonym = self.es.get_book_synonym(mms_id)
        lamda = len(synonym)
        books = []
        books_names = {}
        while lamda > 0 and len(books) < 10:
            synonyms = self.es.get_books_by_common_synonym(synonym,lamda)
            if str(mms_id) in synonyms:
                del synonyms[str(mms_id)]
            for book in synonyms:
                if len(books) < 10:
                    books.append(book)
            for book in synonyms:
                if len(books_names) < 10:
                    books_names[book] = synonyms[book][0]
            lamda -= 1
        return books, books_names


    def find_books_by_token(self,token,lamda = 2):
        synonym = self.es.get_synonym_index_by_token(token)
        return self.es.get_books_by_common_synonym(synonym,lamda)
