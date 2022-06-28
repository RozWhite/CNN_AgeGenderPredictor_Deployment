from __future__ import division, print_function
# coding=utf-8
#import sys
import os
import numpy as np
#from PIL import Image
# Keras
#from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)


MODEL_PATH = 'models/model2.h5'

# Load your trained model
model = load_model(MODEL_PATH)



def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(128, 128), grayscale=True)
    x = np.array(img)
    x=x.reshape(1, 128, 128, 1)
    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        #Y_true
        temp = f.filename.split('_')
        age = int(temp[0])
        gender = int(temp[1])
        
        # map labels for gender
        gender_dict = {0:'Male', 1:'Female'}
        
        # Make prediction
        preds = model_predict(file_path, model)
        pred_gender = gender_dict[round(preds[0][0][0])]
        pred_age = round(preds[1][0][0])
        pred_age=int(str(pred_age)[:2])
               
        result= "\n"+"Original Gender: "+gender_dict[gender]+ ", Predicted Gender: "+pred_gender + ", Original Age: "+ str(age)+", Predicted Age: " +str(pred_age)
        return result
    
    return None

if __name__ == '__main__':
    app.run(debug=True)
      