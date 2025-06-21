from flask import Flask, request, jsonify, render_template
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.cloud import storage
from datetime import timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import uuid

load_dotenv()

app = Flask(__name__)
client = genai.Client(api_key=os.getenv("GEMENI_API_KEY"))

limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])  

# Setup GCS
storage_client = storage.Client()
BUCKET_NAME = "gemini_image_bucket_1"
bucket = storage_client.bucket(BUCKET_NAME)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-image', methods=['POST'])
@limiter.limit("5 per minute")
def generate_image():
    data = request.json
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    # Step 1: Generate image via Gemini
    try:
        response = client.models.generate_images(
            model='imagen-3.0-generate-002',
            prompt=prompt,
            config=types.GenerateImagesConfig(number_of_images=1)
        )
    except Exception as e:
        return jsonify({"error": f"Image generation failed: {str(e)}"}), 500

    generated_urls = []

    # Step 2: Upload to GCS
    for idx, generated_image in enumerate(response.generated_images, 1):
        image_bytes = generated_image.image.image_bytes
        filename = f"{uuid.uuid4().hex}.png"

        try:
            blob = bucket.blob(filename)
            blob.upload_from_string(image_bytes, content_type='image/png')

            # Generate signed URL for 1 hour
            signed_url = blob.generate_signed_url(expiration=timedelta(hours=1))
            generated_urls.append(signed_url)

        except Exception as e:
            # If GCS upload fails, return clear error (but generation worked)
            return jsonify({
                "error": f"Image {idx} generated but failed to upload to GCS: {str(e)}",
                "recovery": "Try again later or check your GCS permissions.",
                "fallback": "You can still access the image in memory if needed."
            }), 500

    return jsonify({"images": generated_urls})

if __name__ == '__main__':
    app.run(debug=True, port=5050)