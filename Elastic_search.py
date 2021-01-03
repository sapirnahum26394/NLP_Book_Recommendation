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
from elasticsearch_dsl import Search

class elasticsearch():
    """
    ===================================================================================================
    Init
    ===================================================================================================
    """
    def __init__(self):
        self.client = Elasticsearch()
        self.s = Search(using=self.client)

    """
    ===================================================================================================
    Functions
    ===================================================================================================
    """
    def upload_dictionary(self,dictionary,index):
        print("Number of books: {}".format(len(dictionary)))
        if index=="books":
            val1="book_id"
            val2="topics"
        for i in range(len(dictionary)):
            self.client.indices.create(index=index, ignore=400)
            self.client.index(index=index, id=i, body={val1: dictionary[i][0], val2: dictionary[i][1]})
            # print(self.client.get(index=index, id=i)['_source'])

    def delete_index(self,index):
        self.client.indices.delete(index=index, ignore=[400, 404])


    def find_token(self,token):
        books_id=[]
        res = self.client.search(index="books",body={"query": {"match": {"topics":token}}},size=1000)
        print("Got %d Hits:" % res['hits']['total']['value'])
        if res['hits']['total']['value'] == 0:
            return -1
        else:
            for hit in res['hits']['hits']:
                books_id.append(hit['_source']['book_id'])
        return books_id
