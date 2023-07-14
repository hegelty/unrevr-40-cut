import random

import PIL.ImageShow
import cv2, os
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/upload_file', methods=['POST'])
def file_upload():
    if request.method == 'POST':
        f = request.files['file']
        file_hash = str(hash(f))
        f.save("./videos/" + secure_filename(file_hash + ".mp4"))
        frames = get_frame(file_hash)
        print(len(frames))
        PIL.ImageShow.show(frames[0])
        return '파일이 저장되었습니다'


def get_frame(file_hash):
    v_cap = cv2.VideoCapture(os.path.abspath("./videos/" + file_hash + ".mp4"))

    frames = []
    while v_cap.isOpened():
        ret, image = v_cap.read()
        if ret:
            image = cv2.resize(image, (1920, 1080))
            frames.append(image)
        else:
            break

    return random.sample(frames, 40)


if __name__ == '__main__':
    app.run(debug=True, port=5000)