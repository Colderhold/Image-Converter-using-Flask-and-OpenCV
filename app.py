from flask import Flask, render_template, request, flash
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

def processImage(temp_filename, orig_filename, operation):
    print(f'The operation is {operation} and filename is {orig_filename}')

    # Load the image directly from the temporary file
    img = cv2.imread(temp_filename)

    if img is None:
        # Handle the case where the image could not be loaded
        print('Error: Image not loaded.')
        return 'error'

    newfilename = f"static/{os.path.basename(orig_filename)}"
    print(f'The new filename is: {newfilename}')

    if operation == 'cgray':
        imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        newfilename = f"static/{os.path.basename(orig_filename)}"
        print(f'The new filename is: {newfilename}')
        if cv2.imwrite(newfilename, imgProcessed):
            return newfilename
        else:
            print('Error: Image not saved.')
            return 'error'

    elif operation == 'cwebp':
        newfilename = f"static/{os.path.basename(orig_filename).split('.')[0]}.webp"
        print(f'The new filename is: {newfilename}')
        if cv2.imwrite(newfilename, img):
            return newfilename
        else:
            print('Error: Image not saved.')
            return 'error'

    elif operation == 'cjpg':
        newfilename = f"static/{os.path.basename(orig_filename).split('.')[0]}.jpg"
        print(f'The new filename is: {newfilename}')
        if cv2.imwrite(newfilename, img):
            return newfilename
        else:
            print('Error: Image not saved.')
            return 'error'

    elif operation == 'cjpeg':
        newfilename = f"static/{os.path.basename(orig_filename).split('.')[0]}.jpeg"
        print(f'The new filename is: {newfilename}')
        if cv2.imwrite(newfilename, img):
            return newfilename
        else:
            print('Error: Image not saved.')
            return 'error'

    elif operation == 'cpng':
        newfilename = f"static/{os.path.basename(orig_filename).split('.')[0]}.png"
        print(f'The new filename is: {newfilename}')
        if cv2.imwrite(newfilename, img):
            return newfilename
        else:
            print('Error: Image not saved.')
            return 'error'

    else:
        # Handle the case where operation is not recognized
        print('Error: Operation not recognized.')
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
            new = processImage(temp_file.name, file.filename, operation)

            # Clean up the temporary file
            os.remove(temp_file.name)

        flash(f"Your image has been converted and is available <a href='/{new}'target='_blank'> here</a>")
        return render_template('index.html')

    return render_template('index.html', flash_messages=flash.get_messages())
