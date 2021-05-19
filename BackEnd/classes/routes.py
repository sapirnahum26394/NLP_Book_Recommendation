from BackEnd.classes.Find_books import find_books
from BackEnd.classes.Find_similar import Find_similar_topics
from BackEnd.classes.Topic_Vector_Reduction import Vector_reduction
from BackEnd.classes.Normalize_marc_file import normalizeMarc
from BackEnd.classes.Elastic_search import elasticsearch
from BackEnd.classes.Expend_synonym_index import expend_synonym_index
from BackEnd.classes.Rate_books import rate_books
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from BackEnd.classes.Create_report import create_report
import json
UPLOAD_FOLDER = 'files/marc_files/'
ALLOWED_EXTENSIONS = set(['xml','txt'])

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
rb = rate_books()
es = elasticsearch()
fb = find_books()
cr = create_report()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file',filename=filename))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    data = normalizeMarc(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    record_list = data.records_list
    es.upload_dictionary(record_list, "create")
    expend_synonym_index(record_list)
    return recordListToJson(record_list)


@app.route("/mms_id")
def mms_id():
    id = request.args.get('id', default="*", type=int)
    res,books_names = fb.find_books_by_book_id(id)
    rated,ids = rb.get_books_by_rate(id,res,books_names)
    cr.create_excel(ids, str(id))
    return mmsToJson(rated, id)


@app.route("/reduce", methods=['POST'])
def reduce():
    new_list = {}
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        f = open(app.config['UPLOAD_FOLDER']+file.filename, "r")
        list = f.read().split(",")
        temp_list = list.copy()
        reduce = Vector_reduction()
        reduce.normalize_words_vector_wordnet(list)
        new_list['original_list'] = temp_list
        new_list['reduced_list'] = list
        return json.dumps(new_list)
    return "file not allowed"


@app.route("/expand")
def expand():
    new_list = {}
    token = request.args.get('token', default="*", type=str)
    fs = Find_similar_topics()
    list = fs.get_synonyms_list(token)
    new_list['original_token'] = token
    new_list['expended_list'] = list
    return json.dumps(new_list)


@app.errorhandler(404)
def not_found(e):
    return "{}"

def recordListToJson(recordList):
    new_list=[]
    for i in range(len(recordList)):
        item={}
        item['mms_id']=recordList[i][0]
        item['title']=recordList[i][1]
        item['original_topics']=recordList[i][2]
        item['reduced_topics']=recordList[i][3]
        item['description']=recordList[i][4]
        item['isbn']=recordList[i][5]
        new_list.append(item)
    return json.dumps(new_list)


def mmsToJson(rated,id):
    if len(rated)>10:
        rated = rated[:10]
    new_list = {}
    new_list['mms_id'] = id
    new_list['title'] = es.get_book_title(id)
    new_list['description'] = es.get_book_description(id)
    new_list['original_topics'] = es.get_book_original_topics(id)
    new_list['reduced_topics'] = es.get_book_reduced_topics(id)
    new_list['similar_books'] = rated

    return json.dumps(new_list)

app.run(port=8080)