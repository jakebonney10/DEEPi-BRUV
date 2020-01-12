# Standalone DEEPi drop cameras
> DEEPi will be attached to drop camera BRUVs and record video.

## Overview

Tasked with creating a DEEPi BRUV system to film sharks in the Bahamas. This system will only include a single node which can be directly controlled by the client computer when on the surface.

## Quickstart

1. Power on DEEPi Cams in range of a DEEPi Router and wait until blinking is done. DEEPi Cams will autostart the appropriate Python scripts.
2. Connect a laptop to the DEEPi router.
4. Open a web browser and go to http://raspberrypi.local:5000 
5. Click start stream to view stream.
6. Click rotate until the view is facing the correct way.
7. Click deploy to start recording video.
8. Mark the time or hold a watch to the camera.
9. Click stop stream to pause the stream (saves power and processing speed)
10. DIVE
11. Recover
12. Reconnect browser to http://raspberrypi.local:5000 
13. Click reboot to stop recording and reset the device
<!-- TODO: add a stop recording button -->

## Accessing Media

1. Power on DEEPi Cams in range of a DEEPi Router and wait until blinking is done. DEEPi Cams will autostart the appropriate Python scripts.
2. Connect a laptop to the DEEPi router.
3. Open an FTP client such as FileZilla.
4. Set host to raspberrypi.local
5. Set user and password to pi and raspberry
6. Leave port blank (or set to 21, the standard FTP port)
7. Connect
8. Navigate to </home/pi/Videos> or </home/pi/Pictures>.
9. Transfer all the files to the user computers and delete off the DEEPi
   > WARNING: The DEEPi is inherently unstable storage for many reasons, not the least of which is that it could be eaten by a shark... Never leave files on the device when you have the opportunity to remove them. Additionally, storage is limited and potentially crippling until that bug is solved, so be sure to wipe the drive clean before each use.

## Troubleshooting

### Changing code

Change code on your computer and transfer it to the pi via FTP. You can do it over SSH, but that makes it hard to record changes. Best practice would be to clone this repo and use GIT to track changes.

### Address not recognized

It is possible that an incorrect address is being used or that Avahi/Bonjour is not working properly for hostname recognition. In this case access the routers admin page and go to the DHCP clients list. 

### No Connection (browser or ftp)

1. Double check that DEEPi and router are on.
2. Double check that the router has the correct SSID and PSK.

	ESSID = DEEPiNet
	PSK = deepinet
	
3. Try to [add a network](#add-network)

### Scripts not auto-starting/working

The auto start works by running in the file </etc/rc.local>. It is a single line right **before** the end of the file. 

```
runuser -l  pi -c 'python3 /home/pi/deepi/app.py'
```

To check this is working, SSH into the DEEPi and run ```ps aux | grep python``` which lists all jobs currently running and then displays only lines that have the phrase 'python' in them. To get a list of all jobs, run ```ps aux```. To get a list of jobs owned by the current user, run ```ps```. Using these commands you can find out if the app.py is running. 

> Note: ```ps``` commands will also display themselves in the list of jobs running. 

If the script is running, kill it. ```killall python3``` or ```killall python```. This may require ```sudo```. Now run the script manually, and see if any errors pop up while using it. If errors do pop up, read the error message and correct the code. 

The most likely issue is that the save point is not working properly. Check where the error message says it is attempting to save files and make sure those directories exist. 

```
mkdir /path/to/directory
```

### Add network 

If you have SSH access to the DEEPi, this can be done through ```sudo raspi-config```. 

If you have access to the SD card, a network can be added through the <wpa_supplicant.conf> file in the <boot/> directory. 

>WARNING: The <wpa_supplicant.conf> file is simple, but if you mess it up when the DEEPi is potted, you could brick the DEEPi.

If you do not have access to SSH or the SD card, you can try modifying the network SSID and PSK to match what you believe the DEEPi is configured for. Cell phone hotspots allow these changes. 

>Note: DEEPi will only connect to 2.4 GHz networks.

### Modify to simplify

If things really are not working, we can go to a simplier script. Below is the method within the DEEPi class which called the deploy button is clicked.

``` Python
def deploy(self, splitTime = 600):
	'''Run deployment script'''
	print("Recording first video")
	PiCamera.start_recording( self, output='/home/pi/Videos/{}.h264'.format(next(name) ), splitter_port=1)
	while True:
		PiCamera.wait_recording(self, timeout=splitTime, splitter_port=1)
		print("Splitting recording")
		PiCamera.split_recording( self, output='/home/pi/Videos/{}.h264'.format(next(name)), splitter_port=1)
```

If we are trying to simplify, we can do away with the app and just make a script that calls this function. Then use rc.local to call this script. In this case we do not have any way to confirm the workings of camera, but it should run.

```Python
import deepi

cam = deepi.DEEPi()
cam.deploy(splittime=600)
```

## Hardware

See further notes from Nick and Brennan.

- ?x DEEPi Cams (1x standalone)
- 1x DEEPi Router with 2.4GHz Network set to SSID=DEEPiNet ans PSK=deepinet. The router can be reached at http://192.168.8.1 and the admin password is admin.


## Contributors

This is a University of Rhode Island [URIL](https://web.uri.edu/uril/) project.

  * Brennan Phillips
  * Nicholas Chaloux
  * Russell Shomberg

## Appendix

### Client Software Dependencies

- python3
- deepiclient: For python dependencies, see requirements.txt


### DEEPiCam Setup

> This setup process is now handled by the [deepi-boot-script]() which will be linked shortly. 
<!-- TODO: link deepi-boot-script... -->

<!-- TODO: this belongs in a seperate document -->

```apt-get install python3```

```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```

```sudo apt-get install python3-distutils```

```python3 get-pip.py --user```

```pip3 install picamera --user```

```pip3 install flask --user```

From local computer
<!-- TODO: just use the FTP to move this over -->
```scp -r ./* pi@raspberrypi.local:```

Add this line to rc.local
```runuser -l pi -c 'python3 /home/pi/app.py'  &```

```mkdir Videos```

```mkdir Pictures```

Set up FTP server
```sudo apt install proftpd```

```sudo raspi-config```
Enable camera and reboot.


