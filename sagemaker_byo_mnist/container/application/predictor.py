# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

from __future__ import print_function

import numpy as np
import re, io, base64
from PIL import Image
from flask import request

import os
import json
import pickle
from io import StringIO
import sys
import signal
import traceback
import flask
import pandas as pd
from application import app
from src.models import predict_model

model_path = os.path.join('output', 'models')

# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.

class ScoringService(object):
    model = None                # Where we keep the model when it's loaded

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model == None:
            with open(os.path.join(model_path, 'application-model.pkl'), 'r') as inp:
                cls.model = pickle.load(inp)
        return cls.model

    @classmethod
    def predict(cls, input):
        """For the input, do the predictions and return them.

        Args:
            input (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        clf = cls.get_model()
        return clf.predict(clf)

# The flask app for serving predictions
# app = flask.Flask(__name__)

@app.route('/index', methods=['GET', 'POST'])
def index():

    # image_data = re.sub('^data:image/.+;base64,', '', request.form.items()[1])
    # print('request.form[img]')
    # print(image_data)
    imgData = request.get_data()
    imgData1 = imgData.decode("utf-8")
    img_str = re.search(r'base64,(.*)',imgData1).group(1)
  
    image_bytes = io.BytesIO(base64.b64decode(img_str))
    im = Image.open(image_bytes)
    print('im1')
    print(im)

    # Resize image to 28x28
    im = im.resize((28,28))
    print('im2')
    print(im)

    arr = np.array(im)[:,:,0:1]
    print('arr')
    print(arr)


    # nparr = np.fromstring(imgData.decode('base64'), np.uint8)
    # print('nparr')
    # print(nparr)

    # im = Image.open(io.BytesIO(base64.b64decode(imgData)))
   
    

    # # Resize image to 28x28
    # im = im.resize((28,28))
    # print("im2")
    # print(im)

    # arr = np.array(im)[:,:,0:1]
    # print("arr")
    # print(arr)

    res = {"result": 0,
       "data": [], 
       "error": ''}

    res["result"] = 1
    res["data"] = [0.1, 0.2, 0.1, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0]

    return res

@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = ScoringService.get_model() is not None  # You can insert a health check here

    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():

    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None

    # Convert from CSV to pandas
    if flask.request.content_type == 'text/csv':
        data = flask.request.data.decode('utf-8')
        s = StringIO(data)
        # data = pd.read_csv(s, header=None)
    else:
        return flask.Response(response='This predictor only supports CSV data', status=415, mimetype='text/plain')


    # # print('Invoked with {} records'.format(data.shape[0]))

    # # Do the prediction
    # # predictions = ScoringService.predict(data)

    os.chdir('/opt/program')
    predictions = predict_model.main(s)

    # Convert from numpy back to CSV
    out = StringIO()
    pd.DataFrame({'results':predictions}).to_csv(out, header=False, index=False)
    result = out.getvalue()

    return flask.Response(response=result, status=200, mimetype='text/csv')

if __name__ == '__main__':
	# run!
	app.run()