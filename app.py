import os
import cv2
import uuid
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

IMAGE_DIR = 'path/to/image/directory'
LABELS = [
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
    "Throw in"
]

OUTPUT_DIR = 'path/to/output/directory'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Save the label for the current image:
        image_id = request.form['image_id']
        label = request.form['label']
        with open('labels.csv', 'a') as f:
            f.write(f'{image_id},{label}\n')
        # Save the labeled image to the output directory:
        output_dir = os.path.join(OUTPUT_DIR, label)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'{image_id}.jpg')
        image_data = request.form['image_data']
        with open(output_path, 'wb') as f:
            f.write(image_data)
        return redirect(url_for('index'))
    else:
        # Find the next unlabelled image:
        labelled_images = set()
        with open('labels.csv', 'r') as f:
            for line in f:
                labelled_images.add(line.strip().split(',')[0])
        for filename in os.listdir(IMAGE_DIR):
            if filename.endswith('.jpg') and filename not in labelled_images:
                image_id = str(uuid.uuid4())
                image_path = os.path.join(IMAGE_DIR, filename)
                image = cv2.imread(image_path)
                # Convert the image to base64 for display in the web UI:
                _, buffer = cv2.imencode('.jpg', image)
                image_data = buffer.tobytes()
                return render_template('index.html', image_id=image_id, image_data=image_data, labels=LABELS)
        # If there are no unlabelled images, display a message:
        return 'No more unlabelled images'

def load_skills():
    skill_imgs = []

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


load_skills()