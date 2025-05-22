from flask import Flask, request, jsonify, send_from_directory
import os
from gpa_calculator import extract_registered_courses, extract_summary_values
import pdfplumber

app = Flask(__name__, static_folder='docs')

@app.route('/')
def index():
    return send_from_directory('docs', 'index.html')

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file uploaded'}), 400
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400
    
    try:
        # Save the uploaded file temporarily
        temp_path = 'temp_transcript.pdf'
        file.save(temp_path)
        
        # Process the PDF
        with pdfplumber.open(temp_path) as pdf:
            document = ""
            for page in pdf.pages:
                document += page.extract_text() + "\n"
        
        # Extract courses
        courses = extract_registered_courses(document)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({'courses': courses})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 