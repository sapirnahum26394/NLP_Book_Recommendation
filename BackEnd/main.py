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
from classes.Normalize_marc_file import normalizeMarc
from classes.Elastic_search import elasticsearch
from classes.Expend_synonym_index import expend_synonym_index
from flask import Flask
app = Flask(__name__)
es=elasticsearch()


"""
===================================================================================================
Main
===================================================================================================
"""
if __name__ == '__main__':
    """
    Start flask app and impost routes functions
    """

    data = normalizeMarc("files/marc_files/bib_records.xml")
    record_list = data.records_list
    es.upload_dictionary(record_list, "create")
    expend_synonym_index(record_list)
    import BackEnd.classes.routes as routes
