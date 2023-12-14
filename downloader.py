from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os
import time

app = Flask(__name__)

DOWNLOADS_DIR = 'downloads'

if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

def sanitize_filename(title):
    """Substituir caracteres inválidos no nome do arquivo."""
    return ''.join(char if char.isalnum() or char in (' ', '-') else '_' for char in title)

def download_media(url, is_audio):
    try:
        yt = YouTube(url)
        title = yt.title
        sanitized_title = sanitize_filename(title)
        timestamp = int(time.time())

        if is_audio:
            media = yt.streams.filter(only_audio=True).first()
            extension = 'mp3'
        else:
            media = yt.streams.get_highest_resolution()
            extension = 'mp4'

        file_path = os.path.join(DOWNLOADS_DIR, f'{sanitized_title}_{timestamp}.{extension}')

        if not os.path.exists(file_path):
            media.download(DOWNLOADS_DIR, f'temp_{extension}')
            os.rename(os.path.join(DOWNLOADS_DIR, f'temp_{extension}'), file_path)

        return file_path, title

    except Exception as e:
        raise RuntimeError(f"Erro ao baixar o {( 'áudio' if is_audio else 'vídeo')} : {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']

        if 'audio' in request.form:
            audio_path, title = download_media(url, is_audio=True)
            return send_file(audio_path, as_attachment=True, download_name=f"{title}.mp3")
        elif 'video' in request.form:
            video_path, title = download_media(url, is_audio=False)
            return send_file(video_path, as_attachment=True, download_name=f"{title}.mp4")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
