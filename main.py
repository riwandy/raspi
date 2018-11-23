from flask import Flask, render_template, Response

# emulated camera
from webcamvideostream import WebcamVideoStream

import cv2

app = Flask(__name__, template_folder='.\template')

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('streaming.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.read()
        ret, jpeg = cv2.imencode('.jpg', frame)

        # print("after get_frame")
        if jpeg is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        else:
            print("frame is none")



@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(WebcamVideoStream(0).start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed2')
def video_feed2():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(WebcamVideoStream(1).start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='localhost', port=5010, debug=True, threaded=True)