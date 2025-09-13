from fasthtml import *
import google.generativeai as genai
import os
import base64
import io
from PIL import Image
import fitz  # PyMuPDF for PDF handling
import tempfile

# Configure Google GenAI
genai.configure(api_key="AIzaSyB-xxx-k")

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Create FastHTML app
app = FastHTML()

@app.get("/")
def home():
    """Home page with file upload form"""
    return html(
        head(
            title("OCR Web Application"),
            meta(charset="utf-8"),
            meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            style("""
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #333;
                    text-align: center;
                    margin-bottom: 30px;
                }
                .upload-area {
                    border: 2px dashed #ccc;
                    border-radius: 10px;
                    padding: 40px;
                    text-align: center;
                    margin: 20px 0;
                    background-color: #fafafa;
                }
                .upload-area:hover {
                    border-color: #007bff;
                    background-color: #f0f8ff;
                }
                input[type="file"] {
                    margin: 10px 0;
                    padding: 10px;
                    width: 100%;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
                button {
                    background-color: #007bff;
                    color: white;
                    padding: 12px 30px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    width: 100%;
                }
                button:hover {
                    background-color: #0056b3;
                }
                .result {
                    margin-top: 30px;
                    padding: 20px;
                    background-color: #f8f9fa;
                    border-radius: 5px;
                    border-left: 4px solid #007bff;
                }
                .error {
                    background-color: #f8d7da;
                    border-left-color: #dc3545;
                    color: #721c24;
                }
                .loading {
                    text-align: center;
                    color: #666;
                }
            """)
        ),
        body(
            div(
                h1("OCR Web Application"),
                p("Upload an image or PDF file to extract text using Google Gemini AI"),
                form(
                    div(
                        label("Select file:"),
                        input(type="file", name="file", accept=".jpg,.jpeg,.png,.pdf", required=True),
                        cls="upload-area"
                    ),
                    button("Extract Text", type="submit"),
                    method="post",
                    action="/upload",
                    enctype="multipart/form-data"
                ),
                cls="container"
            )
        )
    )

@app.post("/upload")
def upload_file(request):
    """Handle file upload and OCR processing"""
    try:
        # Get uploaded file
        file = request.files.get("file")
        if not file:
            return html(
                div("No file uploaded", cls="error"),
                h1("OCR Web Application"),
                p("Upload an image or PDF file to extract text using Google Gemini AI"),
                form(
                    div(
                        label("Select file:"),
                        input(type="file", name="file", accept=".jpg,.jpeg,.png,.pdf", required=True),
                        cls="upload-area"
                    ),
                    button("Extract Text", type="submit"),
                    method="post",
                    action="/upload",
                    enctype="multipart/form-data"
                ),
                cls="container"
            )
        
        # Read file content
        file_content = file.read()
        file_extension = file.filename.split('.')[-1].lower()
        
        # Process based on file type
        if file_extension in ['jpg', 'jpeg', 'png']:
            # Process image
            image = Image.open(io.BytesIO(file_content))
            # Convert to base64 for Gemini
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Call Gemini API
            response = model.generate_content([
                "Extract all text from this image. Return only the extracted text without any additional formatting or explanations.",
                {
                    "mime_type": "image/png",
                    "data": img_base64
                }
            ])
            
            extracted_text = response.text
            
        elif file_extension == 'pdf':
            # Process PDF
            pdf_document = fitz.open(stream=file_content, filetype="pdf")
            all_text = []
            
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                # Convert PDF page to image
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                
                # Convert to base64
                img_base64 = base64.b64encode(img_data).decode()
                
                # Call Gemini API for each page
                response = model.generate_content([
                    "Extract all text from this image. Return only the extracted text without any additional formatting or explanations.",
                    {
                        "mime_type": "image/png",
                        "data": img_base64
                    }
                ])
                
                all_text.append(f"Page {page_num + 1}:\n{response.text}\n")
            
            pdf_document.close()
            extracted_text = "\n".join(all_text)
            
        else:
            return html(
                div("Unsupported file type. Please upload JPG, PNG, or PDF files.", cls="error"),
                h1("OCR Web Application"),
                p("Upload an image or PDF file to extract text using Google Gemini AI"),
                form(
                    div(
                        label("Select file:"),
                        input(type="file", name="file", accept=".jpg,.jpeg,.png,.pdf", required=True),
                        cls="upload-area"
                    ),
                    button("Extract Text", type="submit"),
                    method="post",
                    action="/upload",
                    enctype="multipart/form-data"
                ),
                cls="container"
            )
        
        # Display results
        return html(
            head(
                title("OCR Results"),
                meta(charset="utf-8"),
                meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                style("""
                    body {
                        font-family: Arial, sans-serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #f5f5f5;
                    }
                    .container {
                        background: white;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }
                    h1 {
                        color: #333;
                        text-align: center;
                        margin-bottom: 30px;
                    }
                    .result {
                        margin-top: 30px;
                        padding: 20px;
                        background-color: #f8f9fa;
                        border-radius: 5px;
                        border-left: 4px solid #007bff;
                        white-space: pre-wrap;
                        font-family: monospace;
                    }
                    .back-button {
                        background-color: #6c757d;
                        color: white;
                        padding: 10px 20px;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        text-decoration: none;
                        display: inline-block;
                        margin-top: 20px;
                    }
                    .back-button:hover {
                        background-color: #545b62;
                    }
                """)
            ),
            body(
                div(
                    h1("OCR Results"),
                    div(
                        h3("Extracted Text:"),
                        div(extracted_text, cls="result")
                    ),
                    a("Upload Another File", href="/", cls="back-button"),
                    cls="container"
                )
            )
        )
        
    except Exception as e:
        return html(
            div(f"Error processing file: {str(e)}", cls="error"),
            h1("OCR Web Application"),
            p("Upload an image or PDF file to extract text using Google Gemini AI"),
            form(
                div(
                    label("Select file:"),
                    input(type="file", name="file", accept=".jpg,.jpeg,.png,.pdf", required=True),
                    cls="upload-area"
                ),
                button("Extract Text", type="submit"),
                method="post",
                action="/upload",
                enctype="multipart/form-data"
            ),
            cls="container"
        )

if __name__ == "__main__":
    # Run on port 5000 as specified in FastHTML documentation
    app.run(port=5000, debug=True)
