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
import xml.etree.ElementTree as ET
from gensim.models import Word2Vec
import shutil
import os
import re



class Create_model():
    """
    ===================================================================================================
    Init
    ===================================================================================================
    """
    def __init__(self,file,dir):

        if os.path.exists(dir) == True:
            shutil.rmtree(dir)
        try:
            os.mkdir(dir)
        except:
            print("Error creating the directory")

        #self.dictionary=[]
        self.records_list = self.parse_xml(file)
        self.normalize_650_fields(self.records_list)
        #self.create_word2vec_model(dir)

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
                        fields.append(subfield.text)

            if(fields):
                fields_and_id.append(mms_id)
                fields_and_id.append(fields)
                fields_and_ids.append(fields_and_id)
        return fields_and_ids

    def normalize_650_fields(self,records_list):
        for record in records_list:
            final_words_array = []

            for i, subfield in enumerate(record[1]):
                record[1][i] = re.sub(r'\[[0-9]*\]', '', subfield)
                cell_value = self.normalize_single_array_cell(record[1][i])
                index_i_words_array = cell_value.split()
                for word in index_i_words_array:
                    if word not in final_words_array:
                        final_words_array.append(word)

            record[1] = final_words_array


    def normalize_single_array_cell(self,cell_value):
        cell_value = cell_value.lower()
        cell_value = re.sub(r'\d', ' ', cell_value)
        cell_value = re.sub(r'\s+', ' ', cell_value)
        cell_value = re.sub(r'\.', '',cell_value)
        cell_value = re.sub(r'\-', ' ', cell_value)
        return cell_value

    def create_word2vec_model(self,dir):
        model = Word2Vec(sentences=self.dictionary, window=5, min_count=1, workers=4)
        model.save(dir+"word2vec.model")