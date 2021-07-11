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

from flask import Flask
app = Flask(__name__)



"""
===================================================================================================
Main
===================================================================================================
"""
if __name__ == '__main__':
    """
    Start flask app and impost routes functions
    """
    import BackEnd.classes.routes as routes
