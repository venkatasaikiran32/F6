import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set the upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the home page with the file upload form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was submitted
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # If the user did not select a file
        if file.filename == '':
            return 'No selected file'
        # If the file is valid, save it and redirect to the display page
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('display', filename=filename))
    return render_template('index.html')

# Route to display the uploaded file
@app.route('/display/<filename>')
def display(filename):
    return render_template('display.html', filename=filename)

# Serve the uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename))

if __name__ == '__main__':
    app.run(debug=True)
