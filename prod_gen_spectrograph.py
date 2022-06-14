import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

def plot_spectrogram(Y, sr, hop_length, audio_name, seg_name, y_axis="linear"):
    plt.figure(figsize=(2, 1), dpi=200)
    plt.axis('off')

    librosa.display.specshow(Y, 
                            sr=sr, 
                            hop_length=hop_length, 
                            x_axis="time", 
                            y_axis=y_axis)
    print(f'./data/prod/spectrogram/segments/{audio_name}/{seg_name}.png created!')
    plt.savefig(f'./data/prod/spectrogram/segments/{audio_name}/{seg_name}.png', bbox_inches='tight', pad_inches=0)
    plt.close()

def gen_spec(file_path, file_name, file):
    
    audio_file = file_path
    
    scale, sr = librosa.load(audio_file)
    FRAME_SIZE = 1024
    HOP_SIZE = 32
    S_scale = librosa.stft(scale, n_fft=FRAME_SIZE, hop_length=HOP_SIZE)
    S_scale.shape
    type(S_scale[0][0])
    Y_scale = np.abs(S_scale) ** 2
    Y_scale.shape
    type(Y_scale[0][0])

    Y_log_scale = librosa.power_to_db(Y_scale)
    plot_spectrogram(Y_log_scale, sr, HOP_SIZE, file_name, file, y_axis="log")

def gen_spec_segments(file_path):
    print("Generating spectrograms...")
    file_name = os.path.basename(file_path).split('.')[0]
    for file in os.listdir(f'./data/prod/audio/segments/{file_name}'):
        f_n = file.split('.mp3')[0]
        gen_spec(f"./data/prod/audio/segments/{file_name}/{file}", file_name, f_n)