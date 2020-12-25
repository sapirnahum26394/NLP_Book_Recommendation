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
    def __init__(self):
        self.es = Elasticsearch()
        # ignore 400 cause by IndexAlreadyExistsException when creating an index
        self.es.indices.create(index='test-index', ignore=400)

        self.es.index(index="my-index", id=42, body={"any": "data", "timestamp": datetime.now()})
        print(self.es.get(index="my-index", id=42)['_source'])
    """
    ===================================================================================================
    Functions
    ===================================================================================================
    """
    def exeptions(self):


        # ignore 404 and 400
        self.es.indices.delete(index='test-index', ignore=[400, 404])



