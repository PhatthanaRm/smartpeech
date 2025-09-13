# OCR Web Application

A web application built with FastHTML and Google Gemini AI for optical character recognition (OCR) from uploaded images and PDF files.

## Features

- Upload and process images (JPG, PNG) and PDF files
- Extract text using Google Gemini AI
- Modern, responsive web interface
- Docker support for easy deployment

## Requirements

- Python 3.11+
- Google Gemini API key

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Update the API key in `app.py`:
   ```python
   genai.configure(api_key="YOUR_API_KEY_HERE")
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open your browser and go to `http://localhost:5000`

3. Upload an image or PDF file to extract text

## Docker

Build and run with Docker:

```bash
# Build the image
docker build -t ocr-app .

# Run the container
docker run -p 5000:5000 ocr-app
```

## API Endpoints

- `GET /` - Home page with file upload form
- `POST /upload` - Handle file upload and OCR processing

## Dependencies

- FastHTML: Web framework
- Google Generative AI: OCR processing
- Pillow: Image processing
- PyMuPDF: PDF processing
