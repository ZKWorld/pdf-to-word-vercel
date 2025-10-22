# api/convert.py (Aapka updated code)

import json
import base64
from PyPDF2 import PdfReader
from docx import Document
from io import BytesIO

# Nayi Utility Function (Headers set karne ke liye)
def get_response(data, status_code=200):
    # Yeh headers CORS ko allow karte hain
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*', # <-- Har domain ko allow karo
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    return json.dumps(data), status_code, headers

# Aapka main handler function
def handler(request):
    
    # 1. CORS Pre-flight (OPTIONS request) handle karna zaroori hai
    if request.method == 'OPTIONS':
        # Agar browser pehle OPTIONS request bhejta hai, to seedha headers wapas kar do
        return get_response({"status": "CORS pre-flight success"}, 204)
        
    # 2. Asli POST request
    if request.method == 'POST':
        try:
            # ... (Baaki code jaisa pehle tha) ...
            data = request.json
            if not data or 'pdf_base64' not in data:
                return get_response({"error": "No PDF data found"}, 400)
            
            # ... (Conversion Logic - PDF padhna aur DOCX banana) ...
            
            # 5. Result wapis Android App ko bhejna
            # Ab yahan 'get_response' function use hoga
            return get_response({
                "status": "success",
                "docx_base64": docx_base64,
                "filename": "converted_document.docx"
            }, 200)

        except Exception as e:
            return get_response({"error": f"Conversion failed: {e}"}, 500)
    
    # Agar na OPTIONS na POST ho
    return get_response({"error": "Method not allowed"}, 405)