'''PiCamera implementation for deep sea applications'''

#TODO: impliment logging as necessary

import io
import os
import threading
import socket
import datetime
import time
import struct

from picamera import PiCamera

def genName():
    while True:
        timeStamp = datetime.datetime.utcnow().isoformat()
        yield timeStamp[:-7].replace('-','').replace(':','')

name = genName()


class DEEPi(PiCamera):
    '''
    PiCamera implementation for deep sea applications.
    '''
    
    def __init__(self, diveFolder="./"):
        '''Initiate camera and lock resources'''
        PiCamera.__init__(self)
        self.diveFolder=diveFolder
        self.deployed=False
        self.last_access=0
        self.stream = None
        self.thread = None
        self.last_frame = None

        # 180 corresponds with normal orrientation in lab
        self.rotation=180

    def close(self):
        '''Release all resources'''
        PiCamera.close(self)
        # TODO: check for threads and terminate/join them <>

    def status(self):
        #TODO: impliment dictionary with useful stuff
        status = "Recording: {}".format(self.deployed)
        return status

    def rotate(self):
        '''Rotate view 90 degrees'''
        rotation = int(self.rotation)
        if rotation==270:
            self.rotation=0
        else:
            self.rotation+=90

    def snap_pic(self):
        '''Save a picture with current time'''
        print("Taking Picture")
        PiCamera.capture(self,'/home/pi/Pictures/{}.jpeg'.format(next(name)), splitter_port=0)
        print('File saved /home/pi/Pictures/{}.jpeg'.format(next(name)))


    def update_frame(self):
        '''Continuous capture that saves the latest frame in memory.
        Any live stream applications will access this updating frame
        '''
        self.stream = io.BytesIO()
        print("Starting capture")
        for _ in PiCamera.capture_continuous(self, self.stream, 'jpeg', use_video_port=True, resize=(640,480)):
            if self.stream == None:
                self.stream = None
                break
            #TODO: ensure splitter port and resolution are properly calibrated.
            self.stream.seek(0)
            self.last_frame =  self.stream.read()
            self.stream.seek(0)
            self.stream.truncate()
            #TODO: double check the stream stop and start process
            #if ((time.time()-self.last_access)>10):
        print("Stopping capture")

    def start_stream(self):
        '''Start the threaded process for updating the live stream frame'''
        self.last_access=time.time()
        if self.thread is None:
            self.thread = threading.Thread(target=self.update_frame)
            self.thread.start()
        while self.last_frame is None:
            time.sleep(0)

    def stop_stream(self):
        '''End threaded process for updating the live stream frame'''
        self.stream = None
        self.thread.join()
        self.thread = None
    '''
    def time_lapse(self,delay=10, max_photos=None):
        basename = next(name)
        for filename in PiCamera.capture_continuous(self, '/home/pi/Pictures/{}{counter:03d}.jpg'.format(basename), use_video_port=True):
            print('Captured {}'.format(filename))
            time.sleep(delay)
    '''
    
    def start_recording(self, splitTime = 600):
        '''Run deployment script'''
        print("Recording first video")
        PiCamera.start_recording( self, output='/home/pi/Videos/{}.h264'.format(next(name) ), splitter_port=1)
        self.deployed = True
        while self.deployed:
            PiCamera.wait_recording(self, timeout=splitTime, splitter_port=1)
            print("Splitting recording")
            PiCamera.split_recording( self, output='/home/pi/Videos/{}.h264'.format(next(name)), splitter_port=1)

    def stop_recording(self):
        if not self.deployed:
            return

        PiCamera.stop_recording(self, splitter_port=1)
        self.deployed = False
        return

    def reboot(self):
        PiCamera.close()
        os.system("sudo reboot now")
        return

    def shutdown(self):
        PiCamera.close()
        os.system("sudo shutdown now")
        return


    def __enter__(self):
        '''Called whenever instance is opened using a with statement'''
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Close out anything necessary'''
        self.close()


if __name__ == '__main__':
    camera = DEEPi()
    
