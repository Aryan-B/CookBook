import os
from flask import Flask,jsonify,Response,json, request
from flask_cors import CORS, cross_origin
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename
import cv2, torch
import numpy as np
import glob
import image
from torch import nn
# from .utils import load_state_dict_from_url
import torchvision.models as models
import pickle

filelist = glob.glob('./upload')

UPLOAD_FOLDER = './upload'

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

with open('classes.txt') as f:
    label = list(map(lambda x:x.strip(), f.readlines()))
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(DEVICE)
model = torch.load('model.pht').to(DEVICE)


@app.route('/recognise', methods=['POST'])
def recognise():
    data=dict(request.files)
    for key in data:
        path = os.path.join(app.config['UPLOAD_FOLDER'], data[key].filename)
        print(data[key])
        data[key].save(path)
        
        
        
    x = np.array([np.array(image.open(fname)) for fname in filelist])
    for image in x:
        try:
            img = cv2.imdecode(np.fromfile(image, np.uint8), cv2.IMREAD_COLOR)
            img = cv2.resize(img, (224, 224))
            img = np.transpose(img, axes=[2, 0, 1]) / 255.0
            img = np.expand_dims(img, axis=0)
            img = torch.from_numpy(img).to(DEVICE).float()
            pred = np.argmax(model(img).cpu().detach().numpy()[0])
            print('Image Path:{}, Pred Class:{}'.format("heh",label[pred]))
        except:
            print('Error, Try Again!')
    return jsonify({'name':'Success'})


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
    