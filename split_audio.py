from pydub import AudioSegment
import os
import argparse

# accept two cli parameters file_name and split_duration
# as -f and -d
parser = argparse.ArgumentParser()  
parser.add_argument("-f", help="file name")
parser.add_argument("-d", help="split duration")

# assign the cli parameters to variables
args = parser.parse_args()
print(args)
file_name = args.f
split_duration = int(args.d)

AUDIO_FILE = f"{file_name}"

file_name, extention = AUDIO_FILE.split('.')

# create folder to store the audio files
if not os.path.exists(f"./data/audio/segments/{file_name}"):
    os.makedirs(f"./data/audio/segments/{file_name}")

if not os.path.exists(f"./data/spectrogram/segments/{file_name}"):
    os.makedirs(f"./data/spectrogram/segments/{file_name}")

AUDIO_FILE_PATH = f"./data/audio/{AUDIO_FILE}"

sound = AudioSegment.from_file(AUDIO_FILE_PATH)

halfway_point = len(sound) 

# segment sound every 5000ms
for i in range(0, len(sound), split_duration * 1000):
    segment = sound[i:i+split_duration*1000]
    segment_duration = str((i/(1000))) + '-' + str((i+split_duration*1000)/(1000))
    # print(i/1000, '-', (i+5000)/1000)
    segment.export(f"./data/audio/segments/{file_name}/{file_name}_{segment_duration}.mp3" , format="mp3")
