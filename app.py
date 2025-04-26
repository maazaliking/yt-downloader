from flask import Flask, render_template, request, redirect, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        filename = str(uuid.uuid4()) + '.mp4'
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        ydl_opts = {
            'outtmpl': filepath,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(filepath, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)