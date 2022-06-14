from flask import Flask, render_template, request, render_template_string
import requests
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
from prod_gen_spectrograph import gen_spec_segments
from prod_split_audio import split_audio
from keras.preprocessing import image
from pprint import pprint
import numpy as np
import os
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "./"

model = tf.keras.models.load_model('../Model/my_model.h5')


def generate_result(prediction):
    color_map = {
        "regular": "lightgreen",
        "bump": "red",
        "gear-change": "orange",
        "horn": "yellow"
    }

    html = """
    <html>
        <body>
            <h1>Prediction</h1>
            <table>
                <tr>
                
    """
    for i in range(0, len(prediction)*2, 2):
        td = ""
        time_stamp = str(float(i)) + "-" + str(float(i+2))
        color = color_map[prediction[time_stamp]]
        td += f"<td style='width:100%;background-color:{color}'>{time_stamp}</td>"
        print(time_stamp, prediction[time_stamp])
        html += td

    html += """</tr></table>
    <br>
    <table>
        <tr><td style='background-color:lightgreen'>Regular</td></tr>
        <tr><td style='background-color:red'>Bump</td></tr>
        <tr><td style='background-color:orange'>Gear-change</td></tr>
        <tr><td style='background-color:yellow'>Horn</td></tr>
    </table>
    </body></html>"""

    return html


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file_two():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))

        split_audio('./'+secure_filename(f.filename), 2)
        gen_spec_segments('./'+secure_filename(f.filename))

        prediction = {}
        file_path = "./data/prod/spectrogram/segments/" + \
            secure_filename(f.filename).split(".")[0]

        print(file_path)

        for file in os.listdir(file_path):
            # print(file)
            img = image.load_img(os.path.join(
                file_path, file), target_size=(310, 154, 3))

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

        html = generate_result(prediction)

        # return prediction
        return render_template_string(html)


@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        f = request.form["url"]
        print(f)

        r = requests.get(f)
        # fname = os.path.basename(f).split("?")[0]
        fname = f.split("/")[-1]
        print(fname)
        with open(fname, 'wb') as f:
            f.write(r.content)

        split_audio('./' + fname, 2)
        gen_spec_segments('./' + fname)

        prediction = {}
        file_path = "./data/prod/spectrogram/segments/"+fname.split(".")[0]

        print(file_path)

        for file in os.listdir(file_path):
            # print(file)
            img = image.load_img(os.path.join(
                file_path, file), target_size=(310, 154, 3))

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

        # pprint(prediction)

        new_pred = {}
        for i in range(0, len(prediction)*2, 2):
            time_stamp = str(float(i)) + "-" + str(float(i+2))
            new_pred[time_stamp] = prediction[time_stamp]

        pprint(new_pred)
        return new_pred


if __name__ == '__main__':
    app.run(debug=True)
