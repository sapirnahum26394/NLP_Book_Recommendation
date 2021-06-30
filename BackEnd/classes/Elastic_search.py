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
from elasticsearch_dsl import Search, connections
import calendar
import time

connections.add_connection('default', Elasticsearch)


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

    def upload_dictionary(self, dictionary, mode):
        if mode == "create":
            self.client.indices.create(index="books", ignore=[400, 404])
            for i in range(len(dictionary)):
                res = self.client.exists(index="books", id=dictionary[i][0])
                if res:
                    self.delete_record("books", record_id=dictionary[i][0])
                self.client.index(index="books", id=dictionary[i][0],
                                  body={"title": dictionary[i][1], "original_topics": dictionary[i][2],
                                        "normalized_topics": dictionary[i][3],
                                        "reduced_topics": dictionary[i][4],
                                        "description": dictionary[i][5], "isbn": dictionary[i][6], "synonym": []})

    def delete_record(self, index, record_id):
        self.client.delete(index=index, id=record_id, ignore=[400, 404])

    def delete_index(self, index):
        self.client.indices.delete(index=index, ignore=[400, 404])

    def find_books(self, token):
        books_id = []
        res = self.client.search(index="books", body={"query": {"match": {"reduced_topics": token}}}, size=1000)
        if res['hits']['total']['value'] == 0:
            return -1
        else:
            for hit in res['hits']['hits']:
                books_id.append(hit['_id'])
        return books_id

    def find_token_index(self, token):
        try:
            res = self.client.search(index="synonyms", body={"query": {"match": {"words": token}}}, size=1000)
            if res['hits']['total']['value'] == 0:
                return -1
            else:
                return res['hits']['hits'][0]['_id']

        except:
            return -1

    def add_new_synonyms_list(self, synonyms_list):
        self.client.indices.create(index="synonyms", ignore=400)
        return (self.client.index(index="synonyms", body={"words": synonyms_list}))['_id']

    def update_similar_books(self, mms_id, list):
        res = self.client.get(index="books", id=mms_id)
        self.client.update(index="books", id=mms_id, body={"doc": {"similar_books": list}})

    def update_record_with_indexes(self, mms_id, record_indexes):
        res = self.client.get(index="books", id=mms_id)
        self.client.update(index="books", id=mms_id, body={"doc": {"synonym": record_indexes}})

    def get_book_synonym(self, mms_id):
        res = self.client.get(index="books", id=mms_id)
        return res['_source']['synonym']

    def get_all_synonym(self):
        res = self.client.search(index="synonyms", size=1000)
        return res['hits']['hits']

    def get_book_synonym_lists(self, mms_id):
        res = self.get_book_synonym(mms_id)
        lists = []
        for hit in res:
            lists.append(self.client.get(index="synonyms", id=hit)['_source']['words'])
        return lists

    def get_books_by_common_synonym(self, synonym, lamda):
        count = {}
        for i in synonym:
            res = self.client.search(index="books", body={"query": {"match": {"synonym": i}}}, size=20)
            for hit in res['hits']['hits']:
                if hit['_id'] in count:
                    count[hit['_id']][1] += 1
                else:
                    count[hit['_id']] = [hit['_source']['title'], 1]

        temp = count.copy()
        for j in count:
            if count[j][1] < lamda:
                del temp[j]

        return temp

    def get_synonym_index_by_token(self, token):
        synonyms = []
        res = self.client.search(index="synonyms", body={"query": {"match": {"words": token}}}, size=1000)
        for hit in res['hits']['hits']:
            synonyms.append(hit['_id'])
        return synonyms

    def get_synonym_by_id(self, syn_id):
        res = self.client.get(index="synonyms", id=syn_id)
        return res['_source']['words']

    def get_book_by_isbn(self, isbn):
        res = self.client.search(index="books", body={"query": {"match": {"isbn": isbn}}}, size=1)
        return res['hits']['hits'][0]['_id']

    def get_book_reduced_topics(self, mms_id):
        res = self.client.get(index="books", id=mms_id)
        return res['_source']['reduced_topics']

    def get_book_original_topics(self, mms_id):
        res = self.client.get(index="books", id=mms_id)
        return res['_source']['original_topics']

    def get_book_normalized_topics(self, mms_id):
        res = self.client.get(index="books", id=mms_id)
        return res['_source']['normalized_topics']

    def get_all_books_ids(self):
        books = []
        res = self.client.search(index='books', size=10000)
        for hit in res['hits']['hits']:
            books.append(hit['_id'])
        return books

    def get_book_title(self, mms_id):
        res = self.client.get(index="books", id=mms_id)
        return res['_source']['title']

    def get_book_description(self, mms_id):
        res = self.client.get(index="books", id=mms_id)
        return res['_source']['description']

    def get_book_isbn(self, mms_id):
        res = self.client.get(index="books", id=mms_id)
        return res['_source']['isbn']

    def get_books_by_tokens(self, tokens):
        books = []
        for token in tokens:
            res = self.client.search(index="books", body={"query": {"match": {"reduced_topics": token}}}, size=10)
            for book in res['hits']['hits']:
                temp = {}
                temp['mms_id'] = book['_id']
                temp['title'] = book['_source']['title']
                temp['isbn'] = book['_source']['isbn']

                books.append(temp)
        return books

    def get_random_books(self):
        gmt = time.gmtime()
        res = self.client.search(index='books', doc_type='_doc', size=30,
                                 body={"query": {
                                     "function_score": {
                                         "functions": [{
                                             "random_score": {
                                                 "seed": calendar.timegm(gmt)
                                             }
                                         }]
                                     }
                                 }})
        rnd_books = []
        for book in res['hits']['hits']:
            temp = {}
            temp['mms_id'] = book['_id']
            temp['title'] = book['_source']['title']
            temp['isbn'] = book['_source']['isbn']
            rnd_books.append(temp)

        return rnd_books
