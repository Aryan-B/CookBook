import os
from flask import Flask,jsonify,Response,json, request
from flask_cors import CORS, cross_origin
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './upload'

import os, cv2, torch
import numpy as np

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/recognise', methods=['POST'])
def recognise():
    data=dict(request.files)
    print(data)

    with open('classes.txt') as f:
        label = list(map(lambda x:x.strip(), f.readlines()))

    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(DEVICE)

    model = torch.load('model.pht').to(DEVICE)
    dataresult = []
    for key in data:
        '''moving predict.py into it'''
        path = os.path.join(app.config['UPLOAD_FOLDER'], data[key].filename)
        print(data[key])
        data[key].save(path)
        #end
        try:
            img = cv2.imdecode(np.fromfile(path, np.uint8), cv2.IMREAD_COLOR)
            img = cv2.resize(img, (224, 224))
            img = np.transpose(img, axes=[2, 0, 1]) / 255.0
            img = np.expand_dims(img, axis=0)
            img = torch.from_numpy(img).to(DEVICE).float()
            pred = np.argmax(model(img).cpu().detach().numpy()[0])
            print('Image Path:{}, Pred Class:{}'.format(path, label[pred]))
            #Save the returned result
            dataresult.append('Image Path:{}, Pred Class:{}'.format(path, label[pred]))
        except:
            print('Error, Try Again!')

    #return json
    return jsonify({'result':'Success','data':dataresult})


@app.route('/')
def hw():
    #should change this part to our react one 
	return '<form action="/recognise" method=\'POST\' enctype="multipart/form-data"><div>pic <input type="file" name=\'file[0]\'></div><div>pic2 <input type="file" name=\'file[1]\'></div><input type="submit" value=sign></form>'


if __name__ == '__main__':
   app.run(host="0.0.0.0", port=8080)
    