from flask import Flask, request, jsonify, send_file
from flask_mysql import MySQL

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'rabin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Rabin@123'
app.config['MYSQL_DATABASE_DB'] = 'file_storage_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL(app)

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

@app.route('/files')
def get_files():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM files')
    files = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(files), 200

@app.route('/download/<int:file_id>')
def download_file(file_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM files WHERE id = %s', (file_id,))
    file_name = cursor.fetchone()[0]
    conn.close()
    return send_file(f'uploads/{file_id}.dat', as_attachment=True, attachment_filename=file_name)

if __name__ == '__main__':
    app.run(debug=True)