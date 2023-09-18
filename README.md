# Image Labeling App

This is a Flask web application that allows you to label images using a pre-trained Keras model. The app displays an unlabelled image from the static/unlabelled folder and asks you to label it manually or semi-automatically using the pre-trained model. If you choose to label the image using the model, it will ask you to confirm whether the label is correct.

Once you've labelled an image, it will be moved to a folder inside the labelled folder with the same name as the label.

### Prerequisites

Before running the application, you need to install the following dependencies:

    Python 3.x
    Flask
    Keras
    TensorFlow

You can install the dependencies by running the following command:

    pip install flask keras tensorflow

### Running the Application

To run the application, navigate to the project directory and run the following command:

    flask run

This will start the Flask application and you can access it by going to http://localhost:5000 in your web browser.

### Usage

Open the application in your web browser by going to http://localhost:5000.
An unlabelled image from the static/unlabelled folder will be displayed.

If you choose to label the image manually, the multiple labels will be presented and you only need to click the corresponding button.

If you choose to label the image using the pre-trained model, confirm whether the label is correct by clicking the "Yes" or "No" button.

The labelled image will be moved to a folder inside the labelled folder with the same name as the label.

### Configuration

The configuration for the application is stored in the config.py file. You can modify the following settings:

    MODEL_FILE: The path to the pre-trained Keras model file.
    IS_AUTOMATIC: Whether to automatically label images using the model.

### License

This project is licensed under the MIT License - see the LICENSE file for details.