import time
import datetime
import os
import socket

from flask import Flask, render_template, Response
from deepi import DEEPi

camera = DEEPi()
app = Flask(__name__)

def get_ip():
    '''Figure out the IP address of this pi'''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def genName():
    '''Create a new filename to save files with clear time stamps'''
    while True:
        timeStamp = datetime.datetime.utcnow().isoformat()
        yield timeStamp[:-7].replace('-','').replace(':','')


def genFrame(camera=camera):
    '''
    Access last frame saved by camera.
    Frame should be updated continuously while camera is streaming
    '''
    #camera.start_stream()
    while True:
        camera.last_access = time.time()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + camera.last_frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(genFrame(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

commands = ['status'
            ,'rotate'
            ,'start_stream'
            ,'stop_stream'
            ,'snap_pic'
            ,'deploy'
            ,'reboot'
            ,'shutdown'
]

@app.route('/')
def index():
    return render_template('index.html', commands = commands, status=camera.status, ip=get_ip())

@app.route('/cmd/<command>')
def run(command):
    if command not in commands:
        return "Failure: {} not in predefined commands".format(command), 200, {'Content-Type': 'text/plain'}

    if command=='shutdown':
        os.system('sudo shutdown now')
    if command=='reboot':
        os.system('sudo reboot now')

    try:
        response = eval("camera.{}()".format(command))
    except:
        raise

    return "Success: {}".format(command), 200, {'Content-Type': 'text/plain'}


if __name__=='__main__':
    # Start then Stop prieview to fill last frame
    camera.start_stream()
    time.sleep(1)
    camera.stop_stream()
    app.run(host='0.0.0.0', threaded=True, port=5000)
