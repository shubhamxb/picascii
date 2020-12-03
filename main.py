from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
import img2img, img2txt
import os
import importlib

importlib.import_module("img2img")
app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static\img\input"


@app.route('/')
def index():
    return render_template('input.html')


@app.route('/convert', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('input.html',
                                   error="Select an image first.")
        file = request.files['file']
        if file.filename == '':
            return render_template('input.html',
                                   error="Select an image first.")
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            if checkifimage("static/img/input/" + filename):
                if request.form.get('type') == 'img':
                    img2img.main(str("static/img/input/" + filename),
                                str("static/img/output/ASCII_" + filename),
                                str(request.form.get('mode')),
                                str(request.form.get('background')),
                                int(request.form.get('num_cols')),
                                int(request.form.get('scale')))
                    outputfilename = "/static/img/output/ASCII_" + filename
                    return render_template('result.html',
                                            type = 'img',
                                        output_file=outputfilename)
                else:
                    fname = os.path.splitext(filename)[0] + '.txt'
                    img2txt.main(str("static/img/input/" + filename),
                                str("static/img/output/ASCII_" + fname),
                                str(request.form.get('mode')),
                                int(request.form.get('num_cols')),
                                int(request.form.get('scale')))
                    outputfilename = "/static/img/output/ASCII_" + fname
                    return render_template('result.html',
                                            type = 'txt',
                                        output_file=outputfilename)

            else:
                return render_template('input.html',
                                   error="Unsupported file format.")    
                        
def checkifimage(path_to_image):
    try:
        Image.open(path_to_image)
    except IOError:
        return False
    return True

                    


if __name__ == '__main__':
    app.run(debug=True)
