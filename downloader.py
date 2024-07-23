from flask import Flask, render_template, request, send_file
from yt_dlp import YoutubeDL
import os
import time
import tempfile

app = Flask(__name__)

DOWNLOADS_DIR = 'downloads'

if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

def sanitize_filename(title):
    """Substituir caracteres inválidos no nome do arquivo."""
    return ''.join(char if char.isalnum() or char in (' ', '-') else '_' for char in title)

def download_media(url, is_audio):
    try:
        ydl_opts = {
            'format': 'bestaudio/best' if is_audio else 'best',
            'noplaylist': True,
            'outtmpl': f'{tempfile.gettempdir()}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if is_audio else []
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
            title = sanitize_filename(info_dict.get('title', 'unknown'))
            if is_audio:
                file_path = f"{file_path.rsplit('.', 1)[0]}.mp3"

        return file_path, title

    except Exception as e:
        raise RuntimeError(f"Erro ao baixar o {'áudio' if is_audio else 'vídeo'} : {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']

        if 'audio' in request.form:
            audio_path, title = download_media(url, is_audio=True)
            return send_file(audio_path, as_attachment=True, download_name=f"{title}.mp3", mimetype='audio/mpeg')
        elif 'video' in request.form:
            video_path, title = download_media(url, is_audio=False)
            return send_file(video_path, as_attachment=True, download_name=f"{title}.mp4", mimetype='video/mp4')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
