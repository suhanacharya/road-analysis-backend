from pydub import AudioSegment
import os

def split_audio(audio_path, split_duration):
    AUDIO_FILE = os.path.basename(audio_path)
    
    file_name, extention = AUDIO_FILE.split('.')

    # create folder to store the audio files
    if not os.path.exists(f"./data/prod/audio/segments/{file_name}"):
        os.makedirs(f"./data/prod/audio/segments/{file_name}")

    if not os.path.exists(f"./data/prod/spectrogram/segments/{file_name}"):
        os.makedirs(f"./data/prod/spectrogram/segments/{file_name}")

    AUDIO_FILE_PATH = audio_path

    sound = AudioSegment.from_file(AUDIO_FILE_PATH)

    for i in range(0, len(sound), split_duration * 1000):
        segment = sound[i:i+split_duration*1000]
        segment_duration = str((i/(1000))) + '-' + str((i+split_duration*1000)/(1000))
        segment.export(f"./data/prod/audio/segments/{file_name}/{file_name}_{segment_duration}.mp3" , format="mp3")
