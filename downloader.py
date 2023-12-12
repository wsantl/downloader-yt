from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube
import os
import time

app = Flask(__name__)

DOWNLOADS_DIR = 'downloads'

if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

def download_video(url):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()

        # Extrair o título do vídeo
        video_title = yt.title

        # Substituir caracteres inválidos no nome do arquivo
        video_title = ''.join(char if char.isalnum() or char in (' ', '-') else '_' for char in video_title)

        # Adicionar um timestamp para garantir unicidade
        timestamp = int(time.time())

        video_path = os.path.join(DOWNLOADS_DIR, f'{video_title}_{timestamp}.mp4')

        if not os.path.exists(video_path):
            video.download(DOWNLOADS_DIR, 'temp_video')
            os.rename(os.path.join(DOWNLOADS_DIR, 'temp_video'), video_path)

        return video_path, video_title

    except Exception as e:
        raise RuntimeError(f"Erro ao baixar o vídeo: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']

        if 'audio' in request.form:
            return redirect(url_for('download_audio', url=url))
        elif 'video' in request.form:
            return redirect(url_for('download_video', url=url))

    return render_template('index.html')

@app.route('/download_audio/<path:url>', methods=['GET', 'POST'])
def download_audio(url):
    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()

        # Extrair o título do vídeo
        video_title = yt.title

        # Substituir caracteres inválidos no nome do arquivo
        video_title = ''.join(char if char.isalnum() or char in (' ', '-') else '_' for char in video_title)

        # Adicionar um timestamp para garantir unicidade
        timestamp = int(time.time())

        audio_path = os.path.join(DOWNLOADS_DIR, f'{video_title}_{timestamp}.mp3')

        if not os.path.exists(audio_path):
            audio.download(DOWNLOADS_DIR, 'temp_audio')
            os.rename(os.path.join(DOWNLOADS_DIR, 'temp_audio'), audio_path)

        return audio_path, video_title

    except Exception as e:
        raise RuntimeError(f"Erro ao baixar o áudio: {str(e)}")

@app.route('/download_video/<path:url>', methods=['GET', 'POST'])
def download_video(url):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()

        # Extrair o título do vídeo
        video_title = yt.title

        # Substituir caracteres inválidos no nome do arquivo
        video_title = ''.join(char if char.isalnum() or char in (' ', '-') else '_' for char in video_title)

        # Adicionar um timestamp para garantir unicidade
        timestamp = int(time.time())

        video_path = os.path.join(DOWNLOADS_DIR, f'{video_title}_{timestamp}.mp4')

        if not os.path.exists(video_path):
            video.download(DOWNLOADS_DIR, 'temp_video')
            os.rename(os.path.join(DOWNLOADS_DIR, 'temp_video'), video_path)

        return video_path, video_title

    except Exception as e:
        raise RuntimeError(f"Erro ao baixar o vídeo: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True)
