from flask import Flask, request, send_file, render_template, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from encryptor import encrypt_file, decrypt_file

app = Flask(__name__)
app.secret_key = 'supersecret'
UPLOAD_FOLDER = 'uploads'
DECRYPTED_FOLDER = 'decrypted'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DECRYPTED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    files = [f.replace('.enc', '') for f in files if f.endswith('.enc')]
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        enc_path = os.path.join(UPLOAD_FOLDER, filename + '.enc')
        with open(enc_path, 'wb') as out_file:
            encrypt_file(file.stream, out_file)
        flash('File uploaded and encrypted!')
    else:
        flash('Invalid file type.')
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    enc_path = os.path.join(UPLOAD_FOLDER, filename + '.enc')
    dec_path = os.path.join(DECRYPTED_FOLDER, filename)
    with open(enc_path, 'rb') as in_file, open(dec_path, 'wb') as out_file:
        decrypt_file(in_file, out_file)
    return send_file(dec_path, as_attachment=True)

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), debug=True)