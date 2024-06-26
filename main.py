import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr

def baixar_arquivo(url, nome_arquivo):
    # Verifica se o URL é uma URL válida ou um caminho de arquivo local
    if url.startswith('http://') or url.startswith('https://'):
        # Se for uma URL, baixa o arquivo usando requests
        import requests
        r = requests.get(url, stream=True)
        with open(nome_arquivo, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    else:
        # Se for um caminho de arquivo local, copia o arquivo
        import shutil
        shutil.copy(url, nome_arquivo)

def extrair_audio(video_path):
    # Extrai o áudio de um vídeo para um arquivo WAV
    video = VideoFileClip(video_path)
    audio_path = os.path.splitext(video_path)[0] + ".wav"
    audio = video.audio
    audio.write_audiofile(audio_path, codec='pcm_s16le')
    return audio_path

def converter_audio_para_texto(audio_path):
    # Converte áudio em texto usando reconhecimento de fala
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        texto = recognizer.recognize_google(audio, language='pt-BR')
        return texto
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio")
    except sr.RequestError as e:
        print(f"Erro ao fazer a requisição para o serviço de reconhecimento de fala: {e}")

# Entrada do usuário para o URL do vídeo ou áudio
url = input("Digite o URL do vídeo ou áudio ou o caminho do arquivo local: ")

# Nome do arquivo temporário
nome_arquivo = "temp_video.mp4"

# Baixar ou copiar o arquivo
baixar_arquivo(url, nome_arquivo)

# Extrair o áudio do vídeo
audio_path = extrair_audio(nome_arquivo)

# Converter áudio em texto
texto_convertido = converter_audio_para_texto(audio_path)
if texto_convertido:
    print("Texto reconhecido:")
    print(texto_convertido)

# Remover arquivo temporário após o uso
os.remove(nome_arquivo)

