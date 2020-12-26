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
from elasticsearch import Elasticsearch
from datetime import datetime


class elasticsearch():
    """
    ===================================================================================================
    Init
    ===================================================================================================
    """
    def __init__(self,dictionary):
        self.es = Elasticsearch()
        # ignore 400 cause by IndexAlreadyExistsException when creating an index
        for i in range(len(dictionary)):
            self.es.indices.create(index=i, ignore=400)
            self.es.index(index=i, id=i, body={"book_id": dictionary[i][0], "topics": dictionary[i][1]})
            print(self.es.get(index=i, id=i)['_source'])
    """
    ===================================================================================================
    Functions
    ===================================================================================================
    """
    def exeptions(self):


        # ignore 404 and 400
        self.es.indices.delete(index='test-index', ignore=[400, 404])



