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
import requests
# import 2
# import 3



class Find_similar_topics():
    """
    ===================================================================================================
    Init
    ===================================================================================================
    """
    def __init__(self,vertor,dir):
        self.vector=vertor
        self.model=open(dir+"word2vec.model")
        self.expaned_vector_with_conceptNet()

    """
    ===================================================================================================
    Functions
    ===================================================================================================
    """
    def expaned_vector_with_conceptNet(self):
        temp=self.vector.copy()
        for word in self.vector:
            obj = requests.get('http://api.conceptnet.io/query?node =/c/en/' + word + '?rel=/r/Synonym&limit=20').json()
            words = [edge['end']['label'] for edge in obj['edges']]
            words = list(dict.fromkeys(words))
            print(word)
            print(words)

            temp.append(words)
        print(temp)

