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
from Create_Model import Create_model
from Topic_Vector_Reduction import Vector_reduction
from Find_similar import Find_similar_topics
from Elastic_search import elasticsearch
from nltk.corpus import wordnet

"""
===================================================================================================
Main
===================================================================================================
"""
if __name__ == '__main__':
    XML_file="bib records.xml"
    model_dir="model/"

    word_vector = ["kid","baby","boy","child","mom","mother","done"]
    model=Create_model(XML_file,model_dir)
    elastic=elasticsearch()
    # elastic.upload_dictionary(model.records_list,"books")
    print(elastic.find_token("fiction"))
    # vector = Vector_reduction(word_vector)
    # print(vector.conceptNet)
    # print(vector.wordNet)
    # print(vector.conceptNetAndWordNet)
    # new_vector = vector.conceptNet
    # Find_similar_topics(new_vector,model_dir)
    #
    # synset = wordnet.synsets("child")
    # print('Word and Type : ' + synset[0].name())
    # print('Synonym of Travel is: ' + str([i.name() for i in synset[0].lemmas()]))
    # print('The meaning of the word : ' + synset[0].definition())
    # print('Example of Travel : ' + str(synset[0].examples()))