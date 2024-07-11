from flask import Flask, request, redirect, url_for, render_template_string
import pandas as pd
import os

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template_string('''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="{{ url_for('upload_file') }}" method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
    ''')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Process the CSV file
        process_csv(filepath)
        return 'File successfully uploaded and processed'

def process_csv(filepath):
    # Read the CSV file
    df = pd.read_csv(filepath)
    df['TEST'] = 0
    # Perform any processing on the DataFrame
    #print(df.head())  # Example: print the first few rows

if __name__ == '__main__':
    app.run(debug=True)
