# importing libraries
import google.generativeai as genai
import os
import io
import json
from dotenv import load_dotenv
import PyPDF2
from PIL import Image
import fitz  # pip install PyMuPDF

load_dotenv()
import base64

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def get_gemini_response_keywords(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return json.loads(response.text[8:-4])
    
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Read PDF content
        pdf_bytes = uploaded_file.read()
        
        try:
            # Convert PDF to image using PyMuPDF
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            first_page = pdf_document[0]
            
            # Convert page to image with higher resolution
            pix = first_page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better quality
            img_data = pix.tobytes()
            
            # Convert to base64
            img_base64 = base64.b64encode(img_data).decode()
            
            pdf_parts = [
                {
                    "mime_type": "image/png",
                    "data": img_base64
                }
            ]
            
            pdf_document.close()
            return pdf_parts
            
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
    else:
        raise FileNotFoundError("No file uploaded")
