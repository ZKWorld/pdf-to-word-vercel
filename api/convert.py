# api/convert.py

import json
import base64
from PyPDF2 import PdfReader
from docx import Document
from io import BytesIO

# CORS headers ke saath response banane ka function
def get_response(data, status_code=200, is_options=False):
    # Har domain se aane waali request ko allow karna
    headers = {
        'Access-Control-Allow-Origin': '*', 
        # Yeh headers zaroori hain POST aur OPTIONS requests ke liye
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    
    if is_options:
        # OPTIONS request ka jawab (no content)
        return '', 204, headers
        
    headers['Content-Type'] = 'application/json'
    return json.dumps(data), status_code, headers

def handler(request):
    
    # 1. Agar request OPTIONS hai (CORS pre-flight), to seedha allow kar do
    if request.method == 'OPTIONS':
        return get_response(None, is_options=True)
        
    # 2. Asli POST request
    if request.method == 'POST':
        try:
            data = request.json
            if not data or 'pdf_base64' not in data:
                return get_response({"error": "No PDF data found"}, 400)
            
            # --- Conversion Logic ---
            pdf_data = base64.b64decode(data['pdf_base64'])
            pdf_file = BytesIO(pdf_data)
            
            pdf_reader = PdfReader(pdf_file)
            document = Document()
            
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    document.add_paragraph(text)
            
            docx_file = BytesIO()
            document.save(docx_file)
            docx_file.seek(0)
            docx_base64 = base64.b64encode(docx_file.read()).decode('utf-8')
            # --- Conversion Logic End ---

            return get_response({
                "status": "success",
                "docx_base64": docx_base64,
                "filename": "converted_document.docx"
            }, 200)

        except Exception as e:
            return get_response({"error": f"Conversion failed: {str(e)}"}, 500)
    
    # Method not allowed
    return get_response({"error": "Method not allowed"}, 405)