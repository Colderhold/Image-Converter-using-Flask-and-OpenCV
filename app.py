from flask import Flask, render_template, request, flash, send_file
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

def processImage(temp_filename, operation):
    print(f'The operation is {operation} and filename is {temp_filename}')

    # Load the image directly from the temporary file
    img = cv2.imread(temp_filename)

    if img is None:
        # Handle the case where the image could not be loaded
        print('Error: Image not loaded.')
        return 'error'

    base_filename, _ = os.path.splitext(os.path.basename(temp_filename))

    if operation == 'cgray':
        imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif operation == 'cwebp':
        imgProcessed = img  # No need to process for webp
    elif operation == 'cjpg':
        imgProcessed = img  # No need to process for jpg
    elif operation == 'cjpeg':
        imgProcessed = img  # No need to process for jpeg
    elif operation == 'cpng':
        imgProcessed = img  # No need to process for png
    else:
        print('Error: Operation not recognized.')
        return 'error'

    # Create a temporary file to store the processed image with the original filename and the new extension
    _, temp_output_filename = tempfile.mkstemp(suffix=f'.{operation}')
    cv2.imwrite(temp_output_filename, imgProcessed)

    return temp_output_filename

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
            temp_output_filename = processImage(temp_file.name, operation)

        # Send the processed image directly to the client
        return send_file(temp_output_filename, as_attachment=True, mimetype='image/png')

    return render_template('index.html', flash_messages=flash.get_messages())