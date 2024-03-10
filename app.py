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

def processImage(orig_filename, temp_filename, operation):
    print(f'The operation is {operation} and filename is {temp_filename}')

    # Load the image directly from the temporary file
    img = cv2.imread(temp_filename)

    if img is None:
        # Handle the case where the image could not be loaded
        return 'error'

    newfilename = os.path.join(app.config['UPLOAD_FOLDER'], f"static/{os.path.basename(orig_filename)}")

    if operation == 'cgray':
        imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(newfilename, imgProcessed)
        print(f"The new filename is: {newfilename}")

    elif operation == 'cwebp':
        newfilename = os.path.join(app.config['UPLOAD_FOLDER'], f"static/{os.path.basename(orig_filename).split('.')[0]}.webp")
        cv2.imwrite(newfilename, img)
        print(f"The new filename is: {newfilename}")

    elif operation == 'cjpg':
        newfilename = os.path.join(app.config['UPLOAD_FOLDER'], f"static/{os.path.basename(orig_filename).split('.')[0]}.jpg")
        cv2.imwrite(newfilename, img)
        print(f"The new filename is: {newfilename}")

    elif operation == 'cjpeg':
        newfilename = os.path.join(app.config['UPLOAD_FOLDER'], f"static/{os.path.basename(orig_filename).split('.')[0]}.jpeg")
        cv2.imwrite(newfilename, img)
        print(f"The new filename is: {newfilename}")

    elif operation == 'cpng':
        newfilename = os.path.join(app.config['UPLOAD_FOLDER'], f"static/{os.path.basename(orig_filename).split('.')[0]}.png")
        cv2.imwrite(newfilename, img)
        print(f"The new filename is: {newfilename}")

    else:
        # Handle the case where operation is not recognized
        return 'error'

    if os.path.exists(newfilename):
        print(os.getcwd())
        print("Image saved successfully.")
    else:
        print(os.getcwd())
        print("Error: Image not saved.")

    return newfilename


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
            processImage(file.filename, temp_file.name, operation)
            
            # Clean up the temporary file
            os.remove(temp_file.name)
        
        flash(f"Your image has been converted and is available <a href='/static/{os.path.basename(file.filename)}' target='_blank'> here</a>")
        return render_template('index.html')
    
    return render_template('index.html', flash_messages=flash.get_messages())