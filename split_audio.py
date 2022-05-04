from pydub import AudioSegment
AUDIO_FILE = "kpt_scem.m4a"
sound = AudioSegment.from_file(AUDIO_FILE)

halfway_point = len(sound) 
# print(halfway_point)

first_second = sound[:1000]

# # create a new file "first_half.mp3":
# first_second.export("first_half.mp3", format="mp3")

# segment sound every 5000ms
for i in range(0, len(sound), 5000):
    segment = sound[i:i+5000]
    segment.export(".\hc\hcsegment-%s.mp3" % (i/5000), format="mp3")
