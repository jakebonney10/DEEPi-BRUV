#!/usr/bin/python3

'''DEEPi Light module

Class and supporting functions for controlling DEEPi Light hardware as
part of the DEEPi project (TODO: insert link).

'''

__author__ = "Nicholas Chaloux (URI)"
__version__ = 0.1

#Imports 
from time import sleep 
from gpiozero import DigitalOutputDevice

LIGHT_PIN = 18
delay = 0.2

class DEEPiLight: # TODO: increase docstring
    '''DEEPi Light controls a GPIO pin which will controll the a
    light. The light is a modified headlamp with a single button.  The
    button operates the light through a series of presses.

    '''

    # Possible modes
        
    def __init__(self,pin,delay):
        self.pwm = DigitalOutputDevice(pin=pin, active_high=True,
                                   initial_value=True, pin_factory=None) 
        self.delay = delay

    def press_button(self):
        '''Simulate a button press on the modified head lamp by setting the
        pin high and then low

        '''
        self.pwm.value = 0.0
        sleep(self.delay)
        self.pwm.value = 1.0
        sleep(self.delay)
            
if __name__ == "__main__": # Runs if called as an individual script

    light = DEEPiLight(LIGHT_PIN,delay) # Initialize light

    while True:                      # TODO: add some way to quit this loop
        # Request user input
        mode = input('Enter = Button Press\n')
        light.press_button(delay)
