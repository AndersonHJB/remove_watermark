from flask import Flask, request, send_file, render_template
import cv2
import numpy as np
import os

app = Flask(__name__)

# Directory to save processed images temporarily
TEMP_DIR = "temp/"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


# Function to remove watermark by covering it with a white background
def remove_watermark(image_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path)

    # Define the watermark region (adjust coordinates according to watermark position)
    height, width, _ = img.shape
    watermark_region = (width - 200, height - 50, width, height)  # Adjust as needed

    # Fill the watermark area with white color (255, 255, 255 for white in RGB)
    cv2.rectangle(img, (watermark_region[0], watermark_region[1]),
                  (watermark_region[2], watermark_region[3]),
                  (255, 255, 255), -1)

    # Save the processed image
    output_path = os.path.join(TEMP_DIR, "processed_image.png")
    cv2.imwrite(output_path, img)

    return output_path


# Route for the web interface
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle image upload and watermark removal
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No image file provided", 400

    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400

    # Save uploaded image temporarily
    input_path = os.path.join(TEMP_DIR, "input_image.png")
    file.save(input_path)

    # Remove watermark
    processed_image_path = remove_watermark(input_path)

    # Serve the processed image as download
    return send_file(processed_image_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
