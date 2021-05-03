import os
from flask import Flask,jsonify,Response,json, request
from flask_cors import CORS, cross_origin
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './upload'

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/recognise', methods=['POST'])
def recognise():
    data=dict(request.files)
    for key in data:
        path = os.path.join(app.config['UPLOAD_FOLDER'], data[key].filename)
        print(data[key])
        data[key].save(path)
    return jsonify({'result':'Success'})


@app.route('/')
def hw():
	return "hello world"


if __name__ == '__main__':
   app.run(host="0.0.0.0", port=8080)
    