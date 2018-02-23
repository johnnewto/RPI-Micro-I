try:
    # Python2
    import Tkinter as tk
    import ttk
except ImportError:
    # Python3
    import tkinter as tk
    import tkinter.ttk as ttk

from Stepper import stepper
from picamera import PiCamera
from time import sleep
import numpy as np
from skimage.io import imread, imsave
import time

#stepper variables

#[stepPin, directionPin, enablePin, limitPin]
focusStepper = stepper([23, 24, 22, 4])

def num(s):
    try:
        return int(s)
    except ValueError:
        return 1
def stepUp(event=' '):
    print('hello')
    focusStepper.step(num(e1.get()), "Up",10,False); #steps, dir, speed, stayOn

def stepDown(event=' '):
    focusStepper.step(num(e1.get()), "Down",10,False); #steps, dir, speed, stayOn  

def old_startCamera(event=' '):

    #camera.resolution = (3280, 2464)    
    camera.resolution = (1640, 1232)
    #camera.framerate = 5
    camera.exposure_mode = 'auto'
    camera.awb_mode = 'auto'
    #camera.shutter_speed = 600000
    #camera.resolution = (640, 400)
    camera.iso = 100;
    sleep(2)
    print('Speed        = ', camera.shutter_speed )
    print('Exposure     = ', camera.exposure_speed )
    print('Analog Gain  = ', camera.analog_gain  )
    print('Digital Gain = ', camera.digital_gain )
    camera.shutter_speed = int(camera.exposure_speed*1)
    
    print('Speed        = ', camera.shutter_speed )
    print('Exposure     = ', camera.exposure_speed )
    
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
 

def startPreview(event=' '):
    #camera.preview_fullscreen=False
    #camera.preview_window=(100, 100, 960, 720)
    camera.start_preview()
 

def stopPreview(event=' '):
    camera.stop_preview()

def captureImage2File(event=' '):
    try: 
        captureImage.imgNum += 1; 
    except AttributeError: 
        captureImage.imgNum = 1
    camera.capture('input/image{}.jpg'.format(captureImage.imgNum))


def oldcaptureImage(event=' '):
    try: 
        captureImage.imgNum += 1; 
    except AttributeError: 
        captureImage.imgNum = 1
    #camera.resolution = (3296, 2464)
    images = []
    shp = camera.resolution
    image = np.empty((1664*shp[1]*3), dtype=np.uint8)
    for n  in range(0,10):
        print("capture image {}".format(n))
        camera.capture(image, 'rgb')
        imager = (np.reshape(image,(shp[1],1664,3)))
        images.append(imager)

    images = np.asarray(images)
    print ("averaging")
    image = np.average(images, axis = 0)

    
    #image = image[:3280, :2464]
    imsave('input/image{:02d}.jpg'.format(captureImage.imgNum), image)
    #camera.resolution = (3280, 2464) 


def captureImage(event=' '):
    frames = 10
    camera.resolution = (3280, 2464) 
    #camera.framerate = 30
    #camera.start_preview()
    # Give the camera some warm-up time
    #time.sleep(2)
    start = time.time()

    

    camera.capture_sequence([
        'input/image{:02d}.jpg'.format(i)
        for i in range(frames)
        ], use_video_port=True)
    finish = time.time()
    
    camera.stop_preview()
    print('Captured %d frames at %.2ffps' % (frames,frames / (finish - start)))
    camera.resolution = (1024, 768)


def captureSequence(event=' '):
    stopPreview();
    powerOn()
    sleep(3)   # time to settle
    camera.resolution = (3280, 2464)    

    camera.capture('input/image{:02d}.jpg'.format(1), resize=(3280, 2464) ) 
    for z in range(2, 10):
        focusStepper.step(num(e1.get()), "Up",3,'True'); #steps, dir, speed, stayOn
        camera.capture('input/image{:02d}.jpg'.format(z), resize=(3280, 2464) )

    for z in range(2, 10):
        focusStepper.step(num(e1.get()), "Down",10,'False'); #steps, dir, speed, stayOn

    powerOff()
    camera.resolution = (1640, 1232)


def powerOff():
    focusStepper.step(num(0), "Down",1,False)   

def powerOn():
    focusStepper.step(num(0), "Down",1,True)   

def exitGui(event=' '):
    powerOff()
    camera.stop_preview()
    camera.close()
    focusStepper.cleanGPIO()
    quit()

##################################################

window = tk.Tk()
window.geometry('150x300+0+100')
frame = tk.Frame(window)
frame.pack()
tk.Label(frame, text="Step Amount").grid(row=0)
e1 = tk.Entry(frame)
e1.insert(10,"100")
e1.grid(row=1, column=0)


btnUp = tk.Button(frame,
                   text="Up",
                   command=stepUp)
btnUp.grid(row=2, column=0, sticky=tk.W, pady=4)

btnDown = tk.Button(frame,
                   text="Down",
                   command=stepDown)
                 
btnDown.grid(row=3, column=0, sticky=tk.W, pady=4)

btnStartPreview = tk.Button(frame,
                   text="Start Preview",
                   command=startPreview)
btnStartPreview.grid(row=4, column=0, sticky=tk.W, pady=4)

btnStopPreview = tk.Button(frame,
                   text="Stop Preview",
                   command=stopPreview)
btnStopPreview.grid(row=5, column=0, sticky=tk.W, pady=4)

btnCapture = tk.Button(frame,
                   text="Capture Image",
                   command=captureImage)
btnCapture.grid(row=6, column=0, sticky=tk.W, pady=4)

btnCapture = tk.Button(frame,
                   text="Capture Sequence",
                   command=captureSequence)
btnCapture.grid(row=7, column=0, sticky=tk.W, pady=4)

btnQuit = tk.Button(frame, 
                   text="QUIT", 
                   fg="red",
                   command=exitGui)
btnQuit.grid(row=8, column=0, sticky=tk.W, pady=4)

window.bind_all('u', stepUp)  
window.bind_all('d', stepDown)  
window.bind_all('c', captureImage)  
window.bind_all('s', stopPreview)  
window.bind_all('q', exitGui)  

if True:
    camera = PiCamera()
    #camera.resolution = (3280, 2464)    

    camera.resolution = (1640, 1232)
    #camera.framerate = 30
    camera.exposure_mode = 'auto'
    camera.awb_mode = 'auto'
    camera.iso = 100;
    sleep(2)
    shutterSpeed = camera.exposure_speed
    print('Speed        = ', camera.shutter_speed )
    print('Exposure     = ', camera.exposure_speed )
    print('Analog Gain  = ', camera.analog_gain  )
    print('Digital Gain = ', camera.digital_gain )
    camera.shutter_speed = int(shutterSpeed*0.5)
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    print('')
    print('Speed        = ', camera.shutter_speed )
    print('Exposure     = ', camera.exposure_speed )
    print('Analog Gain  = ', camera.analog_gain  )
    print('Digital Gain = ', camera.digital_gain )


window.mainloop()
camera.stop_preview()

