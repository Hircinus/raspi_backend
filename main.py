from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

import os

appFlask = Flask(__name__)

@appFlask.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Create a list to hold the image file paths
        image_files = []
        # Get the uploaded images
        uploaded_files = request.files.getlist("folder_input")

        # Path where images will be saved
        folder_path = os.path.join("static", "images")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Iterate through the uploaded files
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                # Save the file and add it to the image_files list
                filename = secure_filename(file.filename)
                file_path = os.path.join(folder_path, filename)
                file.save(file_path)
                image_files.append(file_path.replace('\\', '/'))

        # Debug: Print the contents of image_files
        print(image_files)

        if image_files:
            return render_template('result.html', image_files=image_files)
        else:
            return render_template('result.html', image_files=None)

    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif', 'bmp'}

if __name__ == '__main__':
    appFlask.run(debug=True, port=5000)
