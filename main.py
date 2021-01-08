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
import time

# import nltk
# nltk.download('wordnet')


"""
===================================================================================================
Main
===================================================================================================
"""
if __name__ == '__main__':
    XML_file = "bib records.xml"
    model_dir = "model/"

    # Normalize marc(xml) file and create a record list containing mms_id and list of topics for each record
    data = normalizeMarc(XML_file, model_dir)
    record_list = data.records_list

    # Elastic search - uploading the record list to local elastic search
    es = elasticsearch()
    es.upload_dictionary(record_list, "create")

    time.sleep(3)

    # expend every topic in the record list with wordnet and create new index in elasticsearch
    expend_synonym_index(record_list)

    # reducing the records list topics and uploading to elastic search
    reduce = Vector_reduction()
    for i in range(len(record_list)):
        record_list[i][1] = reduce.normalize_words_vector_wordnet(record_list[i][1])
    print(record_list)
    es.upload_dictionary(record_list, "update")