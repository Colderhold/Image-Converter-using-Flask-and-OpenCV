from flask import Flask, render_template, request, flash, send_file
from werkzeug.utils import secure_filename
import os
import cv2
import tempfile

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(orig_filename, temp_filename, operation):
    print(f'The operation is {operation} and filename is {temp_filename}')

    # Load the image directly from the temporary file
    img = cv2.imread(temp_filename)

    if img is None:
        # Handle the case where the image could not be loaded
        return 'error'

    base_filename, file_extension = os.path.splitext(orig_filename)
    output_filename = f"static/{base_filename}"

    if operation == 'cgray':
        imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(f"{output_filename}.png", imgProcessed)
        return f"{output_filename}.png"

    elif operation == 'cwebp':
        cv2.imwrite(f"{output_filename}.webp", img)
        return f"{output_filename}.webp"

    elif operation == 'cjpg':
        cv2.imwrite(f"{output_filename}.jpg", img)
        return f"{output_filename}.jpg"

    elif operation == 'cjpeg':
        cv2.imwrite(f"{output_filename}.jpeg", img)
        return f"{output_filename}.jpeg"

    elif operation == 'cpng':
        cv2.imwrite(f"{output_filename}.png", img)
        return f"{output_filename}.png"

    else:
        # Handle the case where operation is not recognized
        return 'error'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/edit', methods=['POST'])
def edit():
    if request.method == 'POST':
        operation = request.form.get('operation')
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'error'
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return 'error no selected file'
        
        # Use a temporary directory for file storage
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)
            new_filename = processImage(file.filename, temp_file.name, operation)
            
            # Clean up the temporary file
            os.remove(temp_file.name)
        
        if new_filename == 'error':
            flash('Error processing image')
            return 'error'
        
        # Use the correct path for send_file
        return send_file(new_filename, as_attachment=True)
    
    return render_template('index.html', flash_messages=flash.get_messages())