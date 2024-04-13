import os
from flask import Flask, request, jsonify, send_file, send_from_directory, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'rabin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Rabin@123'
app.config['MYSQL_DATABASE_DB'] = 'file_storage_db'
app.config['MYSQL_DATABASE_HOST'] = '10.0.1.10'
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql = MySQL(app, connection_options={
    'unix socket': None, #Disable Unix socket
    'host': app.config['MYSQL_DATABASE_HOST'],
    'port': app.config['MYSQL_DATABASE_PORT'],
})

# Route for handling file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO files (name) VALUES (%s)', (file.filename,))
    file_id = cursor.lastrowid

    file.save(f'uploads/{file_id}.dat')
    conn.commit()
    conn.close()

    return jsonify({'message': 'File uploaded successfully'}), 201

# Route for getting list of files
@app.route('/files')
def get_files():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM files')
    files = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(files), 200

# Route for downloading a file by ID
@app.route('/download/<int:file_id>')
def download_file(file_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM files WHERE id = %s', (file_id,))
    file_name = cursor.fetchone()[0]
    conn.close()
    return send_file(f'uploads/{file_id}.dat', as_attachment=True, attachment_filename=file_name)

# Route for handling root endpoint
@app.route('/')
def index():
    return render_template('index.html')

# Route for serving favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)