# 🌟 Gemini Image Generator

Generate high-quality AI images using Google's Gemini API via a sleek web interface.

---

## 📸 Features

- Gemini-powered image generation (`imagen-3.0-generate-002`)
- Signed URL-based image access via Google Cloud Storage
- Clean Bootstrap 5 UI
- Rate-limited API using Flask-Limiter (default: `10 requests/min/IP`)
- Environment-based secret management

---

## 🧾 Requirements

- Python 3.8+
- A valid [Gemini API Key](https://makersuite.google.com/app/apikey)
- A Google Cloud Storage Bucket
- Google Service Account Credentials JSON

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

- git clone https://github.com/yourusername/gemini-image-generator.git
- cd gemini-image-generator

### 2. Create .env File

- GEMENI_API_KEY=your_gemini_api_key
- GOOGLE_APPLICATION_CREDENTIALS=google-cred/google_credentials.json

### 3. Install Dependencies

- pip install -r requirements.txt

### 4. Run the App Locally

- python app.py
