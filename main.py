
from flask import Flask, request, render_template
import os
import zipfile

appFlask = Flask(__name__)

@appFlask.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        folder_input = request.files['folder_input']
        if folder_input:
            zip_path = os.path.join("static", folder_input.filename)
            folder_path = os.path.join("static", folder_input.filename.split(".")[0])

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            folder_input.save(zip_path)

            image_files = []

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(folder_path)

            for filename in os.listdir(folder_path):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                    image_files.append(os.path.join(folder_path, filename).replace('\\', '/'))

            # Debug: Print the contents of image_files
            print(image_files)

            if image_files:
                return render_template('result.html', image_files=image_files)
            else:
                return render_template('result.html', image_files=None)

    return render_template('index.html')


if __name__ == '__main__':
    appFlask.run(debug=True, port=5000)
