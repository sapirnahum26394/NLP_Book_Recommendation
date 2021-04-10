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
from Rate_books import rate_books
from Number_batch import number_batch
from flask import Flask
app=Flask(__name__)
rb = rate_books()
# import nltk
# nltk.download('wordnet')


def main():
    # upload this file to elastic search data base
    XML_file = "files/marc_files/bib_records.xml"

    # Normalize marc(xml) file and create a record list containing mms_id and list of topics for each record
    data = normalizeMarc(XML_file)
    record_list = data.records_list
    # print(data.dictionary)
    nb = number_batch()
    # vectors = nb.getVectorsFromWords(data.dictionary)
    # print(vectors)

    # Elastic search - uploading the record list to local elastic search
    es = elasticsearch()
    es.upload_dictionary(record_list,'create')

    # expend every topic in the record list with wordnet and create new index in elasticsearch
    expend_synonym_index(record_list)



"""
===================================================================================================
Main
===================================================================================================
"""
if __name__ == '__main__':

    main()
    #
    # fb = find_books()
    # res,books_names = fb.find_books_by_book_id(991000001799704574)
    # rated, ids = rb.get_books_by_rate(991000001799704574, res, books_names)
    # cr = create_report()
    # cr.create_excel(ids, str(991000001799704574))
    # # import routes
