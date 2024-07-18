from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd
import psycopg2
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database connection details
DB_NAME = "fads12"
DB_USER = "postgres"
DB_PASS = "Fani@123"
DB_HOST = "localhost"
DB_PORT = "5432"

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# Upload CSV route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Read CSV and insert into database
        df = pd.read_csv(filepath)
        conn = get_db_connection()
        cursor = conn.cursor()
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO public.combinedpapers (
                    paperid, title, authors, contactinformation, journal, 
                    publicationdate, abstract, description, openaccess, url,
                    tags, keywords, insectspecies, commonname, iabrelevance, 
                    geneticsdata, microbiologydata, feedtrialsdata, thermaldata
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(row))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "File uploaded successfully"}), 200

# Search route
@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT url 
        FROM public.combinedpapers 
        WHERE title ILIKE %s OR abstract ILIKE %s
    """
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"urls": [result[0] for result in results]}), 200

# Serve React build files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
