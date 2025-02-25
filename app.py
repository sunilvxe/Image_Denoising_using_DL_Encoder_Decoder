from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os
from PIL import Image

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained denoising autoencoder model
model = load_model('denoising_autoencoder.h5')

# Get model's input shape and parameters
input_shape = model.input_shape[1:]  # Get (height, width, channels)
target_height, target_width, target_channels = input_shape

# Define folders for uploaded and processed images
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Set allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    # Read image in appropriate color mode
    if target_channels == 3:
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
    else:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Resize to model's expected input size
    img = cv2.resize(img, (target_width, target_height))
    
    # Normalize pixel values
    img = img.astype('float32') / 255.0
    
    # Add batch dimension and ensure channel dimension exists
    if len(img.shape) == 2:
        img = np.expand_dims(img, axis=-1)
    img = np.expand_dims(img, axis=0)
    
    return img

def postprocess_image(prediction, save_path):
    # Remove batch dimension
    img = prediction[0]
    
    # Rescale to 0-255 range
    img = (img * 255).astype(np.uint8)
    
    # Handle channel dimension for saving
    if img.shape[-1] == 1:
        img = img.squeeze(axis=-1)  # Remove channel dimension for grayscale
        mode = 'L'
    else:
        mode = 'RGB'
    
    # Save with appropriate color mode
    Image.fromarray(img, mode=mode).save(save_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)
        
        if not allowed_file(file.filename):
            return "Invalid file type. Allowed formats: png, jpg, jpeg, bmp, gif."
        
        # Save uploaded file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        # Process image
        try:
            img = preprocess_image(filepath)
            prediction = model.predict(img)
            processed_filename = f'processed_{file.filename}'
            processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
            postprocess_image(prediction, processed_path)
            return redirect(url_for('result', filename=processed_filename))
        except Exception as e:
            return f"Error processing image: {str(e)}"
    
    return render_template('index.html')

@app.route('/result/<filename>')
def result(filename):
    processed_image_url = url_for('static', filename=f'processed/{filename}')
    return render_template('result.html', image_url=processed_image_url)

if __name__ == '__main__':
    app.run(debug=True)