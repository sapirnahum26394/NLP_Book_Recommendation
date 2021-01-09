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
    def upload_dictionary(self,dictionary,mode):
        if mode == "create":
            self.client.indices.create(index="books", ignore=400)
            for i in range(len(dictionary)):
                self.client.index(index="books", id=dictionary[i][0], body={"topics": dictionary[i][1], "synonym": []})
        elif mode == "update":
            for i in range(len(dictionary)):
                self.client.update(index="books", id=dictionary[i][0], body={"doc": {"topics": dictionary[i][1]}})

    def delete_index(self,index):
        self.client.indices.delete(index=index, ignore=[400, 404])

    def find_books(self, token):
        books_id=[]
        res = self.client.search(index="books",body={"query": {"match": {"topics": token}}}, size=1000)
        if res['hits']['total']['value'] == 0:
            return -1
        else:
            for hit in res['hits']['hits']:
                books_id.append(hit['_id'])
        return books_id

    def find_token_index(self, token):
        try:
            res = self.client.search(index="synonyms",body={"query": {"match": {"words":token}}},size=1000)
            if res['hits']['total']['value'] == 0:
                return -1
            else:
                return res['hits']['hits'][0]['_id']

        except:
            return -1

    def add_new_synonyms_list(self, synonyms_list):
        self.client.indices.create(index="synonyms", ignore=400)
        return (self.client.index(index="synonyms", body={"words":synonyms_list}))['_id']

    def update_record_with_indexes(self,mms_id,record_indexes):
        res = self.client.get(index="books",id=mms_id)
        self.client.update(index="books", id=mms_id, body={"doc": {"synonym": record_indexes}})

    def get_book_synonym(self,mms_id):
        res = self.client.get(index="books", id=mms_id)
        return res['_source']['synonym']

    def get_books_by_common_synonym(self,synonym,lamda):
        count = {}
        for i in synonym:
            res = self.client.search(index="books",body={"query": {"match": {"synonym":i}}},size=1000)
            for hit in res['hits']['hits']:
                if hit['_id'] in count:
                    count[hit['_id']] += 1
                else:
                    count[hit['_id']] = 1

        temp = count.copy()
        for j in count:
            if count[j] < lamda:
                del temp[j]

        return temp

    def get_synonym_index_by_token(self,token):
        synonyms = []
        res = self.client.search(index="synonyms", body={"query": {"match": {"words": token}}}, size=1000)
        for hit in res['hits']['hits']:
            synonyms.append(hit['_id'])
        return synonyms
