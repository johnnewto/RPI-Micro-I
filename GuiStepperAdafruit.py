try:
    # Python2
    import Tkinter as tk
    import ttk
except ImportError:
    # Python3
    import tkinter as tk
    import tkinter.ttk as ttk

#from Stepper import stepper
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

from picamera import PiCamera
import atexit
from time import sleep
import numpy as np
#from skimage.io import imread, imsave
import time

#stepper variables

#[stepPin, directionPin, enablePin, limitPin]
#focusStepper = stepper([23, 24, 22, 4])

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myStepper = mh.getStepper(48, 1)  # 200 steps/rev, motor port #1
myStepper.setSpeed(40)             # 30 RPM
turnOffMotors()




def num(s):
    try:
        return int(s)
    except ValueError:
        return 1
def stepUp(event=' '):
    #focusStepper.step(num(e1.get()), "Up",10,False); #steps, dir, speed, stayOn
    myStepper.step(num(e1.get()), Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.MICROSTEP)
    turnOffMotors()

def stepDown(event=' '):
    #focusStepper.step(num(e1.get()), "Down",10,False); #steps, dir, speed, stayOn  
    myStepper.step(num(e1.get()), Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.MICROSTEP)
    turnOffMotors()
    
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
   # camera.preview_window=(600, 100, 1640, 1232)
    camera.start_preview(resolution=(1440,1080))
 

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


def captureImages(event=' '):
    frames = 20
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
    
    print('Captured %d frames at %.2ffps' % (frames,frames / (finish - start)))


def captureSequence(event=' '):
    #stopPreview();
    powerOn()
    #sleep(3)   # time to settle

    camera.capture('input/image{:02d}.jpg'.format(1), resize=(3280, 2464) ) 
    for z in range(1, 5):
        #focusStepper.step(num(e1.get()), "Up",3,'True'); #steps, dir, speed, stayOn
        myStepper.step(num(e1.get()), Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.MICROSTEP)

        camera.capture('input/image{:02d}.jpg'.format(z), resize=(3280, 2464) )

    for z in range(1, 5):
        myStepper.step(num(e1.get()), Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.MICROSTEP)
        #focusStepper.step(num(e1.get()), "Down",10,'False'); #steps, dir, speed, stayOn

    powerOff()


def powerOff():
    #focusStepper.step(num(0), "Down",1,False)
    turnOffMotors()

def powerOn():
    #focusStepper.step(num(0), "Down",1,True)
    turnOffMotors()
    
def setExposure(event=' '):
    camera.exposure_mode = 'auto'
    camera.awb_mode = 'auto'
    camera.iso = 100;
    sleep(2)
    shutterSpeed = camera.exposure_speed
    print('Speed        = ', camera.shutter_speed )
    print('Exposure     = ', camera.exposure_speed )
    print('Analog Gain  = ', camera.analog_gain  )
    print('Digital Gain = ', camera.digital_gain )
    camera.shutter_speed = int(shutterSpeed*0.95)
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    print('')
    print('Speed        = ', camera.shutter_speed )
    print('Exposure     = ', camera.exposure_speed )
    print('Analog Gain  = ', camera.analog_gain  )
    print('Digital Gain = ', camera.digital_gain )
    
def lessExposure(event=' '):
    shutterSpeed = camera.exposure_speed
    print('')
    print('Speed        = ', camera.shutter_speed )
    print('Exposure     = ', camera.exposure_speed )
    camera.shutter_speed = int(shutterSpeed*0.95)
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    print('')
    print('Speed        = ', camera.shutter_speed )
    print('Exposure     = ', camera.exposure_speed )
    
def moreExposure(event=' '):
    shutterSpeed = camera.exposure_speed
    print('')
    print('Speed        = ', camera.shutter_speed )
    print('Exposure     = ', camera.exposure_speed )

    camera.shutter_speed = int(shutterSpeed*1.05)
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    print('')
    print('Speed        = ', camera.shutter_speed )
    print('Exposure     = ', camera.exposure_speed )


def exitGui(event=' '):
    powerOff()
    camera.stop_preview()
    camera.close()
    #focusStepper.cleanGPIO()
    turnOffMotors()
    quit()

##################################################

window = tk.Tk()
window.geometry('150x500+0+100')
frame = tk.Frame(window)
frame.pack()
tk.Label(frame, text="Step Amount").grid(row=0)
e1 = tk.Entry(frame)
e1.insert(10,"10")
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
                   command=captureImages)
btnCapture.grid(row=6, column=0, sticky=tk.W, pady=4)

btnCapture = tk.Button(frame,
                   text="Capture Sequence",
                   command=captureSequence)
btnCapture.grid(row=7, column=0, sticky=tk.W, pady=4)

btnQuit = tk.Button(frame, 
                   text="Set Exposure", 
                   command=setExposure)
btnQuit.grid(row=8, column=0, sticky=tk.W, pady=4)

btnQuit = tk.Button(frame, 
                   text="> Exposure", 
                   command=moreExposure)
btnQuit.grid(row=9, column=0, sticky=tk.W, pady=4)

btnQuit = tk.Button(frame, 
                   text="< Exposure", 
                   command=lessExposure)
btnQuit.grid(row=10, column=0, sticky=tk.W, pady=4)

btnQuit = tk.Button(frame, 
                   text="QUIT", 
                   fg="red",
                   command=exitGui)
btnQuit.grid(row=11, column=0, sticky=tk.W, pady=4)

window.bind_all('u', stepUp)  
window.bind_all('d', stepDown)  
window.bind_all('c', captureImages)  
window.bind_all('s', stopPreview)  
window.bind_all('x', setExposure)  
window.bind_all('q', exitGui)  


if True:
    camera = PiCamera()
    camera.resolution = (3280, 2464)    
    setExposure()
    #camera.resolution = (1640, 1232)
    #camera.framerate = 30


window.mainloop()
camera.stop_preview()

