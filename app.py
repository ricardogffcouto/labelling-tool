import os
import uuid

import cv2
import shutil
from flask import Flask, render_template, request, redirect, url_for
from keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np


app = Flask(__name__)

# load the Keras model
model = load_model('model/skills.h5')

IMAGE_DIR = 'static/unlabelled'
SKILL_LABELS = [
    "Rainbow",
    "Nutmeg",
    "Cannon Kick",
    "Slide Tackle",
    "Long Pass",
    "Layoff Pass",
    "Olympic Kick",
    "Reaction",
    "Interception",
    "Strong Goalkeeper",
    "Playing out",
    "Head Play",
    "Throw in",
    "None"
]
SKILL_LEVEL_LABELS = [
    "0",
    "1",
    "2",
    "3",
]

NUMBER_LABELS = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]

LABELS = NUMBER_LABELS

labels = sorted(LABELS)

# KEYMAP = [
#     "q", "w", "e", "r", "t", "a", "s", "d", "f", "g", "z", "x", "c", "v"
# ]

OUTPUT_DIR = 'labelled'

def predict(img):
    img = load_img(img, target_size=(224, 224))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img/255

    pred = model.predict(img)
    return labels[np.argmax(pred)]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Save the label for the current image:
        image_id = request.form['image_id']
        image_path = request.form['image_path']
        label = request.form['prediction']
        output_dir = os.path.join(OUTPUT_DIR, label)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'{image_id}')
        shutil.move(image_path, output_path)
        return redirect(url_for('index'))
    else:
        for filename in os.listdir(IMAGE_DIR):
            if filename.endswith('.png'):
                image_path = os.path.join(IMAGE_DIR, filename)
                prediction = predict(image_path)
                prediction_path = os.path.join('static', f'{prediction}.png')
                return render_template('index.html', image_path=image_path, prediction_path=prediction_path, prediction=prediction)
        # If there are no unlabelled images, display a message:
        return 'No more unlabelled images'


@app.route('/label', methods=['GET', 'POST'])
def label():
    if request.method == 'POST':
        # Save the label for the current image:
        image_id = request.form['image_id']
        image_path = request.form['image_path']
        label = request.form['label']
        output_dir = os.path.join(OUTPUT_DIR, label)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'{image_id}')
        shutil.move(image_path, output_path)
        return redirect(url_for('label'))
    else:
        for filename in os.listdir(IMAGE_DIR):
            if filename.endswith('.png'):
                image_path = os.path.join(IMAGE_DIR, filename)
                return render_template('label.html', image_id=filename, image_path=image_path, labels=LABELS, keymap=["0", "1", "2", "3"])
        # If there are no unlabelled images, display a message:
        return 'No more unlabelled images'

def create_skills():
    skill_h = 42
    starting_y1 = 9
    starting_y2 = 3

    img1 = cv2.imread("skills/1.png")
    img2 = cv2.imread("skills/2.png")

    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    for i in range(7):
        new_img = img1[starting_y1 + skill_h * i:starting_y1 + skill_h * (i+1), 0:w1]
        cv2.imwrite(f"skills/{LABELS[i]}.png", new_img)

    for i in range(6):
        new_img = img2[starting_y2 + skill_h * i:starting_y2 + skill_h * (i+1), 0:w2]
        cv2.imwrite(f"skills/{LABELS[i + 7]}.png", new_img)

def create_numbers():
    folder_path = "static/unlabelled"
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    for file in files:
        img = cv2.imread(f"{folder_path}/{file}")
        h, w = img.shape[:2]
        new_img = img[8:h-8, 0:int(w/2)+4]
        cv2.imwrite(f"{folder_path}/{uuid.uuid4()}.png", new_img)

def get_skill_levels():
    import os
    import glob

    SKILL_LEVEL = {
        "X1": 38,
        "X2": 54,
        "Y1": 24,
        "Y2": 40,
    }

    # Set the path to the folder containing subfolders with images
    folder_path = "labelled/skills"

    # Get all subdirectories inside the folder
    subdirs = [os.path.join(folder_path, d) for d in os.listdir(folder_path) if
               os.path.isdir(os.path.join(folder_path, d))]

    # Get all image files inside each subdirectory
    image_files = []
    for subdir in subdirs:
        image_files.extend(
            glob.glob(os.path.join(subdir, "*.png")))

    for file in image_files:
        img = cv2.imread(file)

        skill_level = img[
          SKILL_LEVEL["Y1"]:SKILL_LEVEL["Y2"], SKILL_LEVEL["X1"]:SKILL_LEVEL["X2"]
        ]

        cv2.imwrite(f"static/unlabelled/{uuid.uuid4()}.png", skill_level)

if __name__ == '__main__':
    app.run(debug=True)