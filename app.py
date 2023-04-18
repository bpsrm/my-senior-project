import os
import bcrypt
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory, session
import cv2
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import mysql.connector
import numpy as np
import base64
import pytesseract
import random
import string

app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'snp65_project'
}

@app.route('/uploads/<filename>')
def serve_file(filename):
    uploads_dir = os.path.join(os.path.dirname(app.instance_path), './uploads/')
    return send_from_directory(directory=uploads_dir, path=filename)

@app.route('/uploads/ <filename>')
def getImage(filename):
    uploads_dir = os.path.join(os.path.dirname(app.instance_path), './uploads/')
    return send_from_directory(directory=uploads_dir, path=filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/detect')
def detect():
    return render_template('detect.html')

# @app.route('/detect-text', methods=['POST'])
# def detect_text():
#     data = request.json
#     image_data = data['imageData'].split(',')[1].encode('utf-8')

#     img = cv2.imdecode(np.frombuffer(base64.b64decode(image_data), np.uint8), cv2.IMREAD_COLOR)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     text = pytesseract.image_to_string(gray)
#     # text = pytesseract.image_to_string(gray, lang=['eng', 'tha'])
#     if text:
#         retval, buffer = cv2.imencode('.png', img)
#         img_base64 = base64.b64encode(buffer).decode('utf-8')
#         return jsonify({'status': 'success', 'text': text, 'imageData': img_base64})
#     else:
#         return jsonify({'status': 'error', 'message': 'Text cannot be read'})
@app.route('/detect-text', methods=['POST'])
def detect_text():
    data = request.json
    image_data = data['imageData'].split(',')[1].encode('utf-8')

    img = cv2.imdecode(np.frombuffer(base64.b64decode(image_data), np.uint8), cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray, lang='eng+tha')
    if text:
        retval, buffer = cv2.imencode('.png', img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        return jsonify({'status': 'success', 'text': text, 'imageData': img_base64})
    else:
        return jsonify({'status': 'error', 'message': 'Text cannot be read'})


@app.route('/pdf_convert')
def create():
    return render_template('pdf-convert.html')

@app.route('/convert', methods=['POST'])
def convert():
    uploaded_file = request.files['pdf_file']

    if uploaded_file.filename != '':
        path_file = os.path.join(os.getcwd(), 'uploads', uploaded_file.filename)

        uploaded_file.save(path_file)
        text = extract_text(path_file)
        filename = os.path.basename(path_file)
        data = [
            text,
            filename,
        ]
        return render_template('convert.html', info=data)

    return render_template('create.html')

def extract_text(pdf_file):
    with open(pdf_file, 'rb') as f:
        pdf_reader = PdfReader(f)
        num_pages = len(pdf_reader.pages)
        text = ""
        for i in range(num_pages):
            page = pdf_reader.pages[i]
            text += page.extract_text()
        return text

@app.route('/pdf_data')
def pdfData():
    return render_template('pdf-information.html')


@app.route('/save', methods=['POST'])
def save():

    data = request.get_json()
    topic = data['topic']
    detail = data['des']
    text = data['text']
    file_path = data['file_path']
    user = data['user']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    sql = 'INSERT INTO library_pdf (topic, detail, text_content, file_upload, user_created) VALUES (%s, %s, %s, %s, %s)'
    val = (topic, detail, text, file_path, user)
    cursor.execute(sql, val)
    conn.commit()

    cursor.close()
    conn.close()

    success = {"message": "success"}
    
    return jsonify(success)

@app.route('/library')
def library():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    sql = 'SELECT * FROM library_pdf'
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('library.html',data=result)

@app.route('/search')
def search():
    query = request.args.get('query')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM library_pdf WHERE topic LIKE %s", ('%' + query + '%',))
    results = cursor.fetchall()
    
    conn.close()
    return jsonify(results)

@app.route('/show/<int:id>')
def show(id):
    data = retrieve_data(id)
    return render_template('show-pdf.html', row=data)

def retrieve_data(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT * FROM library_pdf WHERE id = %s", (id,))
        row = cur.fetchone()
    except Exception as e:
        print(f"Error retrieving data from database: {e}")
        row = None
    finally:
        if conn:
            conn.close()
    return row

@app.route('/edit/<int:id>')
def edit(id):
    data = retrieve_data(id)
    return render_template('edit-library.html', data=data)

@app.route('/update-data', methods=['POST'])
def update_data():
    try:
        data = request.get_json()
        topic = data['topic']
        detail = data['detail']
        id = data['id']
        text = data['text']

        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("UPDATE library_pdf SET topic = %s, detail = %s, text_content = %s WHERE id = %s", (topic, detail, text, id,))
        conn.commit()

        return jsonify({'success': True, 'message': 'Data updated successfully!'})
    except Exception as e:
        print(f"Error updating data to database: {e}")
        return jsonify({'success': False, 'message': 'Error updating data!'})
    finally:
        if conn:
            conn.close()

@app.route('/delete-data/<int:id>', methods=['DELETE'])
def delete_data(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("DELETE FROM library_pdf WHERE id = %s", (id,))
        conn.commit()
        message = "Data deleted successfully"
    except Exception as e:
        print(f"Error deleting data from database: {e}")
        message = "Error deleting data"
    finally:
        if conn:
            conn.close()
    return message


if __name__ == '__main__':
    app.run(debug=True)
# if __name__ == '__main__':
#     app.run(debug=False)
