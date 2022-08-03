import os
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

from keras.preprocessing import image

from prod_split_audio import split_audio
from prod_gen_spectrograph import gen_spec_segments


split_audio('./data/audio/kpt-scem.m4a', 2)

gen_spec_segments('./data/audio/kpt-scem.m4a')

model = tf.keras.models.load_model('../Model/my_model.h5')

file_path = "./data/prod/spectrogram/segments/kpt-scem"

prediction = {}
print("kpt-scem")
for file in os.listdir(file_path):
    # print(file)
    img = image.load_img(os.path.join(file_path, file),
                         target_size=(310, 154, 3))

    x = image.img_to_array(img)
    x /= 255
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])

    classes = model.predict(images, batch_size=10)

    # print(classes[0])
    time_stamp = file.split("_")[1].rstrip(".png")
    maxi = max(classes[0])
    if classes[0][0] == maxi:
        # print(time_stamp, "bump")
        prediction[time_stamp] = "bump"
    elif classes[0][1] == maxi:
        # print(time_stamp, "gear-change")
        prediction[time_stamp] = "gear-change"
    elif classes[0][2] == maxi:
        # print(time_stamp, "horn")
        prediction[time_stamp] = "horn"
    elif classes[0][3] == maxi:
        # print(time_stamp, "regular")
        prediction[time_stamp] = "regular"

pprint(prediction)
