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
import pandas as pd


class create_report():
    """
    ===================================================================================================
    Init
    ===================================================================================================
    """
    def __init__(self):
        self.es = elasticsearch()

    """
    ===================================================================================================
    Functions
    ===================================================================================================
    """
    def create_excel(self,sorted_dict,book_id):
        ids=[]
        scores=[]
        names=[]
        topics=[]
        synon = []
        ids.append(book_id)
        scores.append("-")
        names.append(self.es.get_book_title(book_id))
        topics.append(self.es.get_book_topics(book_id))
        synon.append(self.es.get_book_synonym(book_id))
        for book in sorted_dict:
            ids.append(book)
            scores.append(sorted_dict[book])
            names.append(self.es.get_book_title(book))
            topics.append(self.es.get_book_topics(book))
            synon.append(self.es.get_book_synonym_lists(book))
        df = pd.DataFrame({'Book ID':ids,
                           'Title':names,
                           'Score':scores,
                           'topics':topics,
                           'synonyms':synon})
        writer = pd.ExcelWriter("files/report.xlsx", engine='xlsxwriter')
        df.to_excel(writer, sheet_name=book_id, startrow=0, header=False)

        workbook = writer.book
        worksheet = writer.sheets[book_id]

        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1})

        # Write the column headers with the defined format.
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num+1, value, header_format)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()