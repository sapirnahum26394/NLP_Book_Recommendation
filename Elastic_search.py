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
from elasticsearch_dsl  import Search

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


    def find_books(self,token):
        books_id=[]
        res = self.client.search(index="books",body={"query": {"match": {"topics":token}}},size=1000)
        print("Got %d Hits:" % res['hits']['total']['value'])
        if res['hits']['total']['value'] == 0:
            return -1
        else:
            for hit in res['hits']['hits']:
                books_id.append(hit['_source']['book_id'])
        return books_id

    def find_token_index(token):
        print("need to add a body to the method")
        print("the method should search and return the index of the token from the elastic search")
        print("and if the token does not exist in the elastic search the method should return -1")
        return -1

    def add_new_synonyms_list(synonyms_list):
        print("need to add a body to the method")
        print("the method should create a new index in the elastic search (in the synonyms column), and add the synonyms list into it")
        print("the method should return the number(key?) of the new added index")
        return 1

    def add_new_record_with_indexes(mms_id,record_indexes):
        print("need to add a body to the method")
        print("the method should create a new index in the elastic search (in the records with indexes coulumn), and add the record with the relevant indexes list into it")