from flask import Flask, request, send_file, render_template
from PIL import Image, ImageFilter
import io
import os

app = Flask(__name__)

# Directory to save processed images temporarily
TEMP_DIR = "temp/"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


# Function to remove the watermark from the image
def remove_watermark(image_path):
    img = Image.open(image_path)

    # Define the region to crop (adjust these coordinates as per the watermark location)
    width, height = img.size
    watermark_region = (width - 200, height - 50, width, height)  # Example: bottom-right region

    # Apply blur filter to the watermark area
    cropped = img.crop(watermark_region)
    blurred = cropped.filter(ImageFilter.GaussianBlur(10))  # Adjust blur radius as needed

    img.paste(blurred, watermark_region)

    # Save processed image temporarily
    output_path = os.path.join(TEMP_DIR, "processed_image.png")
    img.save(output_path)

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

    img_bytes = file.read()
    img = Image.open(io.BytesIO(img_bytes))

    # Save uploaded image temporarily
    input_path = os.path.join(TEMP_DIR, "input_image.png")
    img.save(input_path)

    # Remove watermark
    processed_image_path = remove_watermark(input_path)

    # Serve the processed image as download
    return send_file(processed_image_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
