import os
from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'user': 'rabin',
    'password': 'Rabin@123',
    'host': '10.0.1.10',  # Update to MySQL server IP or hostname
    'database': 'file_storage_db',
    'port': 3306,  # Update to MySQL server port
    'auth_plugin': 'mysql_native_password'  # Use the default authentication plugin
}

# Route for rendering index.html template
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
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert file information into the 'files' table
        cursor.execute('INSERT INTO files (name) VALUES (%s)', (file.filename,))
        file_id = cursor.lastrowid

        # Save the file to the uploads directory with the file_id as filename
        file_path = os.path.join('/app/uploads', str(file_id))
        file.save(file_path)
        # Insert file information into the 'files' table
        # You'll need to modify this part to interact with your MySQL database
        # Use the file information to insert into your MySQL database
        # Commit changes and close the connection
        connection.commit()
        connection.close()

        return jsonify({'message': 'File uploaded successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for getting list of files
@app.route('/files')
def get_files():
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Retrieve file information from the 'files' table
        cursor.execute('SELECT id, name FROM files')
        files = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]

        # Close the connection
        connection.close()

        return jsonify(files), 200
    except Exception as e:
        # If there's an error fetching files (e.g., table doesn't exist or query fails), return an empty list
        print(f"Error fetching files: {str(e)}")
        return jsonify([]), 200  # Return an empty list instead of raising an error

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)