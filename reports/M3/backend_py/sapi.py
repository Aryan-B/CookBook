from __future__ import print_function
import time
import spoonacular
from spoonacular.rest import ApiException
from pprint import pprint

import os

from flask import Flask,jsonify,Response,json, request
from flask_cors import CORS, cross_origin
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename
import cv2, torch
import numpy as np
import glob
from torch import nn
import torchvision.models as models
import pickle
import json




configuration = spoonacular.Configuration()
configuration.api_key['apiKey'] = 'de1b34dcfe874d82885c269c47708c22'

api_instance = spoonacular.DefaultApi(spoonacular.ApiClient(configuration))
# username = "dsky" # str | The username.
# hash = "4b5v4398573406" # str | The private hash for the username.
# inline_object11 = spoonacular.InlineObject11(username,hash) # InlineObject11 | 

UPLOAD_FOLDER = './upload'

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# with open('classes.txt') as f:
#     label = list(map(lambda x:x.strip(), f.readlines()))
# DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(DEVICE)
# model = torch.load('model.pht').to(DEVICE)

@app.route('/recognise', methods=['POST'])
def recognise():
    data=dict(request.files)
    for key in data:
        path = os.path.join(app.config['UPLOAD_FOLDER'], data[key].filename)
        print(data[key])
    #     data[key].save(path)
        
        
        
    # x = np.array([np.array(image.open(fname)) for fname in filelist])
    # for image in x:
    #     try:
    #         # img = cv2.imdecode(np.fromfile(image, np.uint8), cv2.IMREAD_COLOR)
    #         # img = cv2.resize(img, (224, 224))
    #         # img = np.transpose(img, axes=[2, 0, 1]) / 255.0
    #         # img = np.expand_dims(img, axis=0)
    #         # img = torch.from_numpy(img).to(DEVICE).float()
    #         # pred = np.argmax(model(img).cpu().detach().numpy()[0])
    #         print(model_less.predict(image))
    #         # print('Image Path:{}, Pred Class:{}'.format("heh",label[pred]))
    #     except:
    #         print('Error, Try Again!')
    return jsonify({'name':'Success', 'type':'string'},{'name':'Success1', 'type':'string'})

@app.route('/ingredients',methods=['POST'])
def ingredients():
    datas = json.loads((request.data.decode("ascii")))
    # # print(type(datas))
    # print(request.data)
    query=[]
    for x in datas:
        # print(x)
        # print(type(x))
        query.append(x['name'])
    query_string=','.join(query)
    print(query_string)
    try:
        api_response = api_instance.search_recipes_by_ingredients(query_string)
        # pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->add_to_meal_plan: %s\n" % e)
    return Response(json.dumps(api_response),mimetype='application/json')
    # return jsonify({'name':'Success', 'type':'status'})
    
@app.route('/recipe')
def recipe():
    # datas = json.loads((request.data.decode("ascii")))
    # # # print(type(datas))
    # # print(request.data)
    # query=[]
    # for x in datas:
    #     # print(x)
    #     # print(type(x))
    #     query.append(x['id'])
    # query_string=','.join(query)
    # print(query_string)
    try:
        api_response = api_instance.get_recipe_information('479101')
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->add_to_meal_plan: %s\n" % e)
    return jsonify({'name':'Success', 'type':'string'},{'name':'Success1', 'type':'string'})

if __name__ == '__main__':
       app.run(host="0.0.0.0", port=8080)


