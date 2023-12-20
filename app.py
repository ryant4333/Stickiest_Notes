import os
import datetime
# from flask_cors import CORS, cross_origin
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from pydub import AudioSegment

app = Flask(__name__)
# CORS(app)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        print('Request for upload page received')
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        if 'audio' not in request.files:
            print('No audio file in request')
            return 'No audio file in request', 400

        file = request.files['audio']
        if file.filename == '':
            print('No selected file')
            return 'No selected file', 400

        # Save the file temporarily as .ogg
        print(file.filename)
        ogg_path = os.path.join('uploads', file.filename)
        file.save(ogg_path)
        print("File saved to " + ogg_path)

        

        # Convert .ogg to .wav
        # ogg_to_wav(ogg_path)
        # audio = AudioSegment.from_ogg(file)
        # print(type(audio))
        # wav_path = os.path.splitext(ogg_path)[0] + "_" + timestamp + '.wav'
        # audio.export(wav_path, format='wav')
        print('File uploaded successfully')
        return 'File uploaded successfully'
    except Exception as e:
        print('Error uploading file: ' + str(e))
        return 'Error uploading file', 500


def ogg_to_wav(path_to_ogg):
    audio = AudioSegment.from_ogg(path_to_ogg)
    audio.export(path_to_ogg, format='wav')

if __name__ == '__main__':
   app.run()
