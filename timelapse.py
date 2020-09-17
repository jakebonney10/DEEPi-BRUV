from deepi import DEEPi

camera = DEEPi()
DEEPi.time_lapse(camera, delay = 10)

'''
camera = PiCamera()
sleep(2)
for filename in camera.capture_continuous('img-{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
    print('Captured %s' % filename)
    sleep(10) # wait 10 seconds
'''