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
from Elastic_search import elasticsearch
from Find_similar import Find_similar_topics


class Index_Records_And_Expand_Elastic():
    """
    ===================================================================================================
    Init
    ===================================================================================================
    """
    def __init__(self,records_list):
        self.index_records_and_expand_elastic(records_list)

    """
    ===================================================================================================
    Functions
    ===================================================================================================
    """
    def find_indexed_records(self,records_list):
        for record in records_list:
            words_indexes = []
            for word in record[1]:
                token_index = elasticsearch.find_token_index(word)
                if token_index is -1:
                    synonyms = Find_similar_topics.get_synonyms_list(word)
                    token_index = elasticsearch.add_new_synonyms_list(synonyms)
                words_indexes.append(token_index)
            elasticsearch.add_new_record_with_indexes(record[0],words_indexes)

