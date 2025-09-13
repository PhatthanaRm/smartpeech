# SmartSpeech OCR Web Application

A web application built with Python FastHTML and Google GenAI for OCR (Optical Character Recognition) functionality. Upload images or PDF files to extract text using AI.

## Features

- 🖼️ **Image OCR**: Upload images (JPEG, PNG, etc.) to extract text
- 📄 **PDF Processing**: Upload PDF files to extract text
- 🎨 **Modern UI**: Beautiful, responsive web interface with drag-and-drop support
- 🚀 **Fast Processing**: Powered by Google GenAI for accurate text extraction
- 🐳 **Docker Support**: Easy deployment with Docker

## Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)

## Installation

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd smartpeech
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t smartpeech-ocr .
```

2. Run the container:
```bash
docker run -p 5000:5000 smartpeech-ocr
```

The application will be available at `http://localhost:5000`

## Usage

1. Open your web browser and navigate to `http://localhost:5000`
2. Drag and drop image or PDF files onto the upload area, or click "Choose Files"
3. Click "Process Files" to extract text using AI
4. View the extracted text in the results area

## Supported File Types

- **Images**: JPEG, PNG, GIF, BMP, WebP
- **PDFs**: Standard PDF files (text-based and scanned)

## API Endpoints

- `GET /` - Main web interface
- `POST /process` - Process uploaded files for OCR

## Configuration

The Google GenAI API key is configured in the application. Make sure you have a valid API key for the Google GenAI service.

## Dependencies

- `fasthtml` - Fast web framework
- `google-genai` - Google GenAI client library
- `Pillow` - Image processing
- `PyPDF2` - PDF processing
- `python-multipart` - File upload handling

## License

This project is open source and available under the MIT License.
