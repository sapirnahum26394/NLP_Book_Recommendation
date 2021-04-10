"""
Final Project
Software engineering department

Authors:
Sapir Nahum
Shmuel Eliasyan
"""
from BackEnd.Topic_Vector_Reduction import Vector_reduction

"""
===================================================================================================
Imports
===================================================================================================
"""
import xml.etree.ElementTree as ET
from gensim.models import Word2Vec
import shutil
import os
import re
# import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

class normalizeMarc():
    """
    ===================================================================================================
    Init
    ===================================================================================================
    """
    def __init__(self,file):

        self.dictionary = []
        self.records_list = self.parse_xml(file)

    """
    ===================================================================================================
    Functions
    ===================================================================================================
    """
    def parse_xml(self,xml_name):
        # xml should be in shape of a collection with some records
        xml_tree = ET.parse(xml_name)
        xml_root = xml_tree.getroot()
        fields_and_ids = []
        for record in xml_root:
            mms_id = ''
            fields = []
            fields_and_id = []
            for field in record.findall('controlfield'):
                if(field.get('tag') == '001'):
                    mms_id = field.text
                    break

            for field in record.findall('datafield'):
                if(field.get('tag') == '650'):
                    for subfield in field.findall('subfield'):
                        if subfield.get('code')=='a':
                            fields.append(subfield.text)
                elif(field.get('tag') == '245'):
                    for subfield in field.findall('subfield'):
                        if subfield.get('code')=='a':
                                title = subfield.text
                                if title[-1].isalpha() == False:
                                    title = title[:-1]


            if(fields):
                fields_and_id.append(mms_id)
                fields_and_id.append(title)
                fields_and_id.append(fields)
                fields_and_id.append(self.reduceListOfTopics(self.normalize_650_fields(fields)))
                fields_and_ids.append(fields_and_id)
        return fields_and_ids


    def reduceListOfTopics(self,list):
        reduce = Vector_reduction()
        newList = reduce.normalize_words_vector_wordnet(list)
        return newList

    def normalize_650_fields(self,list):
        final_words_array = []
        for i in range(len(list)):
            list[i] = re.sub(r'\[[0-9]*\]', '',list[i])
            cell_value = self.normalize_single_array_cell(list[i])
            index_i_words_array = cell_value.split()
            for word in index_i_words_array:
                if word not in final_words_array:
                    if word not in stop_words:
                        final_words_array.append(word)
        self.dictionary=self.dictionary+final_words_array
        return final_words_array


    def normalize_single_array_cell(self,cell_value):
        cell_value = cell_value.lower()
        cell_value = re.sub(r'\d', ' ', cell_value)
        cell_value = re.sub(r'\s+', ' ', cell_value)
        cell_value = re.sub(r"", '', cell_value)
        cell_value = re.sub(r'\-', ' ', cell_value)
        cell_value = re.sub(r'\(', '',cell_value)
        cell_value = re.sub(r'\)', '', cell_value)
        cell_value = re.sub(r'\,', '', cell_value)
        cell_value = re.sub("'s", '', cell_value)
        cell_value = re.sub("'", '', cell_value)
        cell_value = re.sub("&", '', cell_value)
        return cell_value
