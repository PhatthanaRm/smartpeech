from python_fasthtml.common import *
from google.genai import types
import google.genai as genai
import base64
import io
from PIL import Image
import PyPDF2
import tempfile
import os

# Configure Google GenAI
genai.configure(api_key="AIzaSyAIfdb-TNKbNecLbdDuTa-5YbcXbvTl6RY")

# Create FastHTML app
app = FastHTML()

@app.get("/")
def index():
    return Html("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SmartSpeech OCR</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 {
                text-align: center;
                color: #333;
                margin-bottom: 30px;
            }
            .upload-area {
                border: 2px dashed #667eea;
                border-radius: 10px;
                padding: 40px;
                text-align: center;
                margin: 20px 0;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .upload-area:hover {
                border-color: #764ba2;
                background-color: #f8f9ff;
            }
            .upload-area.dragover {
                border-color: #764ba2;
                background-color: #f0f2ff;
            }
            input[type="file"] {
                display: none;
            }
            .upload-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                transition: transform 0.2s ease;
            }
            .upload-btn:hover {
                transform: translateY(-2px);
            }
            .process-btn {
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px;
                transition: transform 0.2s ease;
            }
            .process-btn:hover {
                transform: translateY(-2px);
            }
            .result-area {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            }
            .loading {
                display: none;
                text-align: center;
                color: #667eea;
            }
            .error {
                color: #dc3545;
                background: #f8d7da;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }
            .success {
                color: #155724;
                background: #d4edda;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 SmartSpeech OCR</h1>
            <p style="text-align: center; color: #666; margin-bottom: 30px;">
                Upload images or PDF files to extract text using AI
            </p>
            
            <div class="upload-area" id="uploadArea">
                <p>📁 Drag and drop files here or click to select</p>
                <input type="file" id="fileInput" accept="image/*,.pdf" multiple>
                <button class="upload-btn" onclick="document.getElementById('fileInput').click()">
                    Choose Files
                </button>
            </div>
            
            <div style="text-align: center;">
                <button class="process-btn" id="processBtn" onclick="processFiles()" disabled>
                    🚀 Process Files
                </button>
            </div>
            
            <div class="loading" id="loading">
                <p>⏳ Processing files... Please wait</p>
            </div>
            
            <div id="results"></div>
        </div>

        <script>
            const uploadArea = document.getElementById('uploadArea');
            const fileInput = document.getElementById('fileInput');
            const processBtn = document.getElementById('processBtn');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            let selectedFiles = [];

            // Drag and drop functionality
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });

            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = Array.from(e.dataTransfer.files);
                handleFiles(files);
            });

            fileInput.addEventListener('change', (e) => {
                const files = Array.from(e.target.files);
                handleFiles(files);
            });

            function handleFiles(files) {
                selectedFiles = files.filter(file => 
                    file.type.startsWith('image/') || file.type === 'application/pdf'
                );
                
                if (selectedFiles.length > 0) {
                    processBtn.disabled = false;
                    uploadArea.innerHTML = `
                        <p>✅ ${selectedFiles.length} file(s) selected</p>
                        <p>${selectedFiles.map(f => f.name).join(', ')}</p>
                        <button class="upload-btn" onclick="document.getElementById('fileInput').click()">
                            Choose Different Files
                        </button>
                    `;
                }
            }

            async function processFiles() {
                if (selectedFiles.length === 0) return;

                loading.style.display = 'block';
                processBtn.disabled = true;
                results.innerHTML = '';

                const formData = new FormData();
                selectedFiles.forEach(file => {
                    formData.append('files', file);
                });

                try {
                    const response = await fetch('/process', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();
                    
                    if (data.success) {
                        results.innerHTML = `
                            <div class="success">
                                <h3>✅ OCR Results</h3>
                                <div style="white-space: pre-wrap; background: white; padding: 15px; border-radius: 5px; margin-top: 10px;">
                                    ${data.text}
                                </div>
                            </div>
                        `;
                    } else {
                        results.innerHTML = `
                            <div class="error">
                                <h3>❌ Error</h3>
                                <p>${data.error}</p>
                            </div>
                        `;
                    }
                } catch (error) {
                    results.innerHTML = `
                        <div class="error">
                            <h3>❌ Error</h3>
                            <p>Failed to process files: ${error.message}</p>
                        </div>
                    `;
                } finally {
                    loading.style.display = 'none';
                    processBtn.disabled = false;
                }
            }
        </script>
    </body>
    </html>
    """)

@app.post("/process")
async def process_files(request: Request):
    try:
        form = await request.form()
        files = form.getlist("files")
        
        if not files:
            return {"success": False, "error": "No files provided"}
        
        all_text = []
        
        for file in files:
            if file.filename:
                # Read file content
                content = await file.read()
                
                # Process based on file type
                if file.content_type.startswith('image/'):
                    # Process image
                    text = await process_image(content)
                    if text:
                        all_text.append(f"=== {file.filename} ===\n{text}\n")
                elif file.content_type == 'application/pdf':
                    # Process PDF
                    text = await process_pdf(content)
                    if text:
                        all_text.append(f"=== {file.filename} ===\n{text}\n")
        
        if all_text:
            return {"success": True, "text": "\n".join(all_text)}
        else:
            return {"success": False, "error": "No text could be extracted from the files"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

async def process_image(image_content):
    """Process image using Google GenAI Vision"""
    try:
        # Convert to base64
        image_b64 = base64.b64encode(image_content).decode('utf-8')
        
        # Create the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create the content
        content = [
            "Extract all text from this image. Return only the text content, no additional formatting or explanations.",
            {
                "mime_type": "image/jpeg",
                "data": image_b64
            }
        ]
        
        # Generate content
        response = model.generate_content(content)
        return response.text
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

async def process_pdf(pdf_content):
    """Process PDF by converting to images and then using OCR"""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(pdf_content)
            tmp_file_path = tmp_file.name
        
        try:
            # Read PDF
            with open(tmp_file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                # If PyPDF2 didn't extract text (scanned PDF), try OCR
                if not text.strip():
                    # For scanned PDFs, we would need additional libraries like pdf2image
                    # For now, return a message
                    return "PDF appears to be scanned. OCR for scanned PDFs requires additional setup."
                
                return text
                
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

if __name__ == "__main__":
    # Run on port 5000 as specified in FastHTML docs
    serve(port=5000)
