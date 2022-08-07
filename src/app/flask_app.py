import cv2
from flask import Flask, Response, render_template
from art import tprint
from loguru import logger

from .. core.config import Settings
from .. service.client import AbstractSocketClient, SocketClient

app = Flask(__name__, template_folder='../../static/templates')


@app.route('/video_feed')
def video_feed():
    def gen_frames():
        while True:
            client: AbstractSocketClient = SocketClient()
            frame = client.parse_frame_from_server()

            array_str = ', '.join(map(str, client.parse_array_from_server()))
            logger.opt(colors=True).info(f'<m>Array: {array_str}, was recieved from server!</m>')

            tprint(f'{array_str}', font="italic")

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')


def run_flask_server():
    settings = Settings()
    app.run(host=settings.flask_server.host, port=settings.flask_server.port, threaded=True)
