import random

import cv2, os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
import qrcode

from result import make_40_cut, make_4_cut

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_40_cut():
    cut_count = int(request.form['type'])
    if cut_count not in [4, 40]:
        return "error"

    f = request.files['file']
    file_hash = str(hash(f))
    f.save("./videos/" + secure_filename(file_hash + ".webm"))
    frames = get_frame(file_hash, cut_count)
    print(len(frames))
    os.makedirs("./images/" + file_hash)
    for i in range(len(frames)):
        cv2.imwrite("./images/" + file_hash + "/" + str(i) + ".png", frames[i])

    if cut_count == 40:
        make_40_cut(file_hash)
    else:
        make_4_cut(file_hash)

    os.remove("./videos/" + file_hash + ".webm")
    for i in range(len(frames)):
        os.remove("./images/" + file_hash + "/" + str(i) + ".png")

    return file_hash


@app.route('/image/<file_hash>', methods=['GET'])
def get_image(file_hash):
    return send_from_directory("./images/" + file_hash, "output.png")


@app.route('/qr/<file_hash>', methods=['GET'])
def get_qr(file_hash):
    with open("./images/" + file_hash + "/qr.png", "wb") as f:
        qrcode.make(request.root_url + "image/" + file_hash).save(f, "PNG")

    return send_from_directory("./images/" + file_hash, "qr.png")


def get_frame(file_hash, frame_count):
    v_cap = cv2.VideoCapture(os.path.abspath("./videos/" + file_hash + ".webm"))
    frames = []
    while v_cap.isOpened():
        ret, image = v_cap.read()
        if ret:
            image = cv2.resize(image, (1920, 1080))
            frames.append(image)
        else:
            break

    return random.sample(frames, frame_count)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
