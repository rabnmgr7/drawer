import os
from flask import Flask, request, jsonify, send_file, send_from_directory, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'rabin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Rabin@123'
app.config['MYSQL_DATABASE_DB'] = 'file_storage_db'
app.config['MYSQL_DATABASE_HOST'] = '10.0.1.10'  # Update to MySQL server IP or hostname
app.config['MYSQL_DATABASE_PORT'] = 3306  # Update to MySQL server port
app.config['MYSQL_DATABASE_DEFAULT_AUTH'] = 'mysql_native_password'

# Initialize MySQL connection
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

# Route for handling file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute('INSERT INTO files (name) VALUES (%s)', (file.filename,))
        file_id = cursor.lastrowid

        file.save(f'uploads/{file_id}.dat')
        conn.commit()
        conn.close()

        return jsonify({'message': 'File uploaded successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for getting list of files
@app.route('/files')
def get_files():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM files')
        files = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
        conn.close()
        return jsonify(files), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
