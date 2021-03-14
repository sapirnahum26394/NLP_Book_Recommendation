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
from Normalize_marc_file import normalizeMarc
from Topic_Vector_Reduction import Vector_reduction
from Find_similar import Find_similar_topics
from Elastic_search import elasticsearch
from Expend_synonym_index import expend_synonym_index
from Find_books import find_books
from Rate_books import rate_books
import time
from flask import Flask
app=Flask(__name__)
rb = rate_books()
# import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet


"""
===================================================================================================
Main
===================================================================================================
"""
if __name__ == '__main__':
    # b1=["god","bible","book","holy","religion","christian"]
    # b2=["god","christ","idol","jesus"]
    # b3=["god","music","apollo","Egyptian","Greek","Roman"]
    # score=0
    # for key in b3:
    #     for word in b2:
    #         x = wordnet.synsets(word)
    #         y = wordnet.synsets(key)
    #         if not x or not y:
    #             continue
    #         s = x[0].wup_similarity(y[0])
    #         score+=s
    #         print(key, ", ", word, " = ", s)
    # size=len(b1)+len(b2)
    # print("Score: ",score/size)


    # XML_file = "files/bib_records.xml"
    #
    # # Normalize marc(xml) file and create a record list containing mms_id and list of topics for each record
    # data = normalizeMarc(XML_file)
    # record_list = data.records_list
    # # print(record_list)
    #
    # # Elastic search - uploading the record list to local elastic search
    # es = elasticsearch()
    # books = es.get_all_books_ids()
    # fb = find_books()
    # for id in books:
    #     # print(id)
    #     res = fb.find_books_by_book_id(id)
    #     rated_books = rb.get_books_by_rate(id,res)
    #     es.update_similar_books(id,rated_books)
    # es.upload_dictionary(record_list, "create")
    #
    # time.sleep(3)
    #
    # # expend every topic in the record list with wordnet and create new index in elasticsearch
    # expend_synonym_index(record_list)
    #
    # # reducing the records list topics and uploading to elastic search
    # reduce = Vector_reduction()
    # for i in range(len(record_list)):
    #     record_list[i][1] = reduce.normalize_words_vector_wordnet(record_list[i][1])
    # es.upload_dictionary(record_list, "update")
    #
    #
    #
    # fb = find_books()
    # res = fb.find_books_by_book_id(991001088454304574)
    # rated = rb.get_books_by_rate(991001088454304574,res)
    import routes
