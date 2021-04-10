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
from BackEnd.Find_similar import Find_similar_topics


class expend_synonym_index():
    """
    ===================================================================================================
    Init
    ===================================================================================================
    """
    def __init__(self,records_list):
        self.find_indexed_records(records_list)

    """
    ===================================================================================================
    Functions
    ===================================================================================================
    """
    def find_indexed_records(self,records_list):
        elastic = elasticsearch()
        similar = Find_similar_topics()
        for record in records_list:
            words_indexes = []
            for word in record[1]:
                token_index = elastic.find_token_index(word)
                if token_index == -1:
                    synonyms = similar.get_synonyms_list(word)
                    token_index = elastic.add_new_synonyms_list(synonyms)
                words_indexes.append(token_index)
            elastic.update_record_with_indexes(record[0],words_indexes)

