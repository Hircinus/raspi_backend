from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os

appFlask = Flask(__name__)
appFlask.config['UPLOAD_FOLDER'] = 'uploads/'  # This is where I defined the folder

# To catch if the folder does not exist
os.makedirs(appFlask.config['UPLOAD_FOLDER'], exist_ok=True)


@appFlask.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve files from the 'folder_input' field
        files = request.files.getlist("folder_input")
        image_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(appFlask.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_files.append(file_path)

        if image_files:
            # No need to send the full paths to the template
            return render_template('result.html', image_files=image_files)
        else:
            return render_template('result.html', image_files=None)

    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif', 'bmp'}


@appFlask.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(appFlask.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    appFlask.run(debug=True, port=5000)
