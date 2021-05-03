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


@app.route('/ingredients')
def ilist():
	ilist = [ { "ingredient" : "apple"}, 
			  { "ingredient" : "sugar"},
			  { "ingredient" : "milk"},
			  { "ingredient" : "flour"},
			]
	return Response(json.dumps(ilist),mimetype='application/json')

@app.route('/recipelist', methods=['GET'])
def rlist():
	rlist = [ { "recipe" : "recipe one", "id":1},
			  { "recipe" : "recipe two", "id":2},
			  { "recipe" : "recipe three", "id":3},
			  { "recipe" : "recipe four", "id":4},
			  { "recipe" : "recipe five", "id":5},
			]
	return Response(json.dumps(rlist),mimetype='application/json')


@app.route('/recipeinfo', methods=['GET'])
def rinfo():
	rinfo = { "recipe" : "recipe one", "id":1, "veg": False, "serving":1, "ingredients":[ { "ingredient" : "apple","amount" : "1 kg"}, 
																						    { "ingredient" : "sugar","amount" : "2 kg"},
																						    { "ingredient" : "milk","amount" : "3 kg"},
																						    { "ingredient" : "flour","amount" : "4 kg"}],
																						    "image":"r one image_url", "link":"r one link_url", "inst":"r_one cooking instruction"}
	return Response(json.dumps(rinfo),mimetype='application/json')

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=8080)
    