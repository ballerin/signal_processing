import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','db'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print (request.form['text'])
        if 'file' not in request.files:
            flash('No file part')
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        try:
            if len(file.filename)<2:
                try:
                    flash('No selected file')
                    return "No selected file"
                except:
                    return "Unable to flash"
        except:
            return "Unable to work with empty file"
        
        try:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return 'Everything is working'
        except:
            return "unable to work with full file"
    return "Not a POST request"

@app.route('/data_taken', methods=['GET', 'POST'])
def data_taken():
    field = request.form['field']
    result = "NOT RIPE YET"
    return render_template('data_taken.html', field=field, result=result)

@app.route('/take_data/<int:field>', methods=['GET', 'POST'])
def take_data(field):
    return render_template('take_data.html', field=field)

@app.route('/', methods=['GET', 'POST'])
def show_html():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')