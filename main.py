import os
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
import wave
import json

def extract_audio(video_path):
    video_clip = VideoFileClip(video_path)
    audio_path = video_path.replace('.mp4', '.wav')
    video_clip.audio.write_audiofile(audio_path, codec='pcm_s16le')
    return audio_path

def transcribe_audio(audio_path, model_path):
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    wf = wave.open(audio_path, "rb")
    transcription = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result).get("text", "")
            transcription += text + " "

    final_result = recognizer.FinalResult()
    text = json.loads(final_result).get("text", "")
    transcription += text

    wf.close()
    return transcription

if __name__ == "__main__":
    video_path = input("Por favor, insira o caminho do arquivo de vídeo local: ")
    model_path = input("Por favor, insira o caminho do diretório do modelo Vosk: ")

    if os.path.isfile(video_path) and video_path.endswith('.mp4'):
        audio_path = extract_audio(video_path)
        transcription = transcribe_audio(audio_path, model_path)
        
        print("Transcrição do áudio:\n")
        print(transcription)
        
        # Cleanup
        os.remove(audio_path)
    else:
        print("O caminho fornecido não é um arquivo de vídeo MP4 válido.")

