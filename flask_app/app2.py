import numpy as np
from flask import Flask, request, jsonify, render_template
import os
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pylab as plt
from werkzeug.utils import secure_filename

def create_preproc_image(filename):
    preproc = _Preprocessor()
    img = preproc.read_from_jpegfile(filename)
    return preproc.preprocess(img)


class _Preprocessor:
    def __init__(self):
        # nothing to initialize
        pass

    def read_from_tfr(self, proto):
        feature_description = {
            'image': tf.io.VarLenFeature(tf.float32),
            'shape': tf.io.VarLenFeature(tf.int64),
            'label': tf.io.FixedLenFeature([], tf.string, default_value=''),
            'label_int': tf.io.FixedLenFeature([], tf.int64, default_value=0),
        }
        rec = tf.io.parse_single_example(
            proto, feature_description
        )
        shape = tf.sparse.to_dense(rec['shape'])
        img = tf.reshape(tf.sparse.to_dense(rec['image']), shape)
        label_int = rec['label_int']
        return img, label_int

    def read_from_jpegfile(self, filename):
        # same code as in 05_create_dataset/jpeg_to_tfrecord.py
        img = tf.io.read_file(filename)
        img = tf.image.decode_jpeg(img, channels=IMG_CHANNELS)
        img = tf.image.convert_image_dtype(img, tf.float32)
        return img

    def preprocess(self, img):
        return tf.image.resize_with_pad(img, IMG_HEIGHT, IMG_WIDTH)


serving_model = tf.keras.models.load_model("clothes_model")

sar=["T-Shirt", "Longsleeve", "Pants", "Shoes", "Shirt", "Dress", "Outwear", "Shorts", "Hat", "Skirt"]
IMG_HEIGHT = 224
IMG_WIDTH = 224
IMG_CHANNELS = 3

#PEOPLE_FOLDER = os.path.join('static', 'images')

# Create flask app
flask_app = Flask(__name__)
#flask_app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@flask_app.route("/")
def Home():
    return render_template("index2.html")

@flask_app.route("/about")
def about_page():
	return "Please subscribe  Artificial Intelligence Hub..!!!"


#@flask_app.route("/predict", methods = ["POST"])
def predict():
    filename=request.files["file"]
    filename_path = "images/" + filename.filename
    img=create_preproc_image(filename_path)

    batch_image = tf.reshape(img, [1, IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS])
    batch_pred = serving_model.predict(batch_image)
    pred = batch_pred[0]
    pred_label_index = tf.math.argmax(pred).numpy()
    pred_label = sar[pred_label_index]
    prob = pred[pred_label_index]
    prob_round=round(prob*100)

    return pred_label, prob_round
#    return render_template("index2.html", prediction_text = "Drabužių kategorija yra  {} su tikimybe {}%".format(pred_label, prob_round),
#                           img_path=img_path)

@flask_app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		imag = request.files['file']

		img_path = "images/" + imag.filename
		imag.save(img_path)

		p = predict()

	return render_template("index2.html", prediction = p, img_path = img_path)


@flask_app.route("/test")
def test_ok():
    return {"result": "ok"}

if __name__ == "__main__":
    flask_app.run(debug=True)