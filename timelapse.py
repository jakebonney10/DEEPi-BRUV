from deepi import DEEPi

'''
Super simple script which calls on deepi class to use time_lapse function.
Set delay to choose frame rate (s). Set wait_to_start (s) to wait before beginning timelapse.
'''

camera = DEEPi()
DEEPi.time_lapse(camera, delay = 10, resolution = (3280,2464))