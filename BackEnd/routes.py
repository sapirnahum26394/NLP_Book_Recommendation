from classes.Find_books import find_books
from Find_similar import Find_similar_topics
from Topic_Vector_Reduction import Vector_reduction
from classes.Normalize_marc_file import normalizeMarc
from classes.Elastic_search import elasticsearch
from classes.Expend_synonym_index import expend_synonym_index
from Rate_books import rate_books
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from classes.Create_report import create_report

UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = set(['xml'])

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
rb = rate_books()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    data = normalizeMarc(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    record_list = data.records_list

    es = elasticsearch()
    es.upload_dictionary(record_list, "create")
    expend_synonym_index(record_list)
    reduce = Vector_reduction()
    for i in range(len(record_list)):
        record_list[i][1] = reduce.normalize_words_vector_wordnet(record_list[i][1])
    es.upload_dictionary(record_list, "update")
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route("/mms_id")
def mms_id():
    # try:
    id = request.args.get('id', default="*", type=int)
    fb = find_books()
    res,books_names = fb.find_books_by_book_id(id)
    rated,ids = rb.get_books_by_rate(id,res,books_names)
    cr=create_report()
    cr.create_excel(ids,str(id))
    # except:
    #     return "Error"
    return rated


@app.route("/reduce")
def reduce():
    try:
        list = request.args.get('list', default="*", type=str)
        list = list.split(",")
        reduce = Vector_reduction()
        list = reduce.normalize_words_vector_wordnet(list)
    except:
        return "Error"
    return str(list)


@app.route("/expand")
def expand():
    try:
        token = request.args.get('token', default="*", type=str)
        fs = Find_similar_topics()
        list = fs.get_synonyms_list(token)
    except:
        return "Error"
    return str(list)




@app.errorhandler(404)
def not_found(e):
    return "{}"



app.run(port=8080)