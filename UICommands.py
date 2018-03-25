
#from Stepper import stepper
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

from picamera import PiCamera
import atexit
from time import sleep
import numpy as np
#from skimage.io import imread, imsave
import time
import threading
import RPi.GPIO as GPIO



# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()
camera = PiCamera()
#camera.resolution = (3280, 2464)    
camera.resolution = (3280//2, 2464//2)    

GPIO_LED_RED = 24
GPIO_CASSETTE_IN = 17


def turnOffMotors():
    print('Turning off motors')
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
    
def num(s):
    try:
        return int(s)
    except ValueError:
        return 1

class uiCommands:
    
    def __init__(self, stepAmount = 10):


        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(GPIO_LED_RED,GPIO.OUT)
        GPIO.setup(GPIO_CASSETTE_IN, GPIO.IN)
        self.setRedLED()
        self.runCassetteMotorOnSense = True

        # global steeper thread
        self.stepperThread = None


        self.focusMotor = mh.getStepper(48, 1)  # 200 steps/rev, motor port #1
        self.focusMotor.setSpeed(30)             # 30 RPM

        self.CassetteMotor = mh.getStepper(48, 2)  # 200 steps/rev, motor port #1
        self.CassetteMotor.setSpeed(80)             # 30 RPM
        
        turnOffMotors()
        # recommended for auto-disabling motors on shutdown!
        atexit.register(turnOffMotors)

        self.setExposure()
        #camera.resolution = (1640, 1232)
        self.stepAmount = stepAmount
        self.readCassetteSensor()


    def readCassetteSensor(self):
        if GPIO.input(GPIO_CASSETTE_IN):      
            GPIO.output(GPIO_LED_RED,GPIO.LOW)
        else:
            GPIO.output(GPIO_LED_RED,GPIO.HIGH)
            print("Cassette Triggered")
            if self.runCassetteMotorOnSense:      
                self.stepIn()

            
        self.timerThread = threading.Timer(1, self.readCassetteSensor)
        self.timerThread.start()

    def setRedLED(self):
        print "LED on"
        GPIO.output(GPIO_LED_RED,GPIO.HIGH)
        time.sleep(1)
        print "LED off"
        GPIO.output(GPIO_LED_RED,GPIO.LOW)
        
        

    def setStepAmount(self, amt):
        self.stepAmount = amt

         
    def stepUp(self, event=' '):
        print('Step Up {:02d}'.format(self.stepAmount))
        self.focusMotor.step(self.stepAmount, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.MICROSTEP)
        turnOffMotors()
        return
    
    def stepDown(self, event=' '):
        print('Step Down {:02d}'.format(self.stepAmount))
        self.focusMotor.step(self.stepAmount, Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.MICROSTEP)
        turnOffMotors()
        return

    def stepIn(self, event=' '):
        print('Step In {:02d}'.format(self.stepAmount))
        self.CassetteMotor.step(self.stepAmount*10, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.DOUBLE)
        turnOffMotors()
        return
    
    def stepOut(self, event=' '):
        print('Step Out {:02d}'.format(self.stepAmount))
        self.CassetteMotor.step(self.stepAmount*10, Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.DOUBLE)
        turnOffMotors()
        return

    def stepFor(self,dir, count):
        self.focusMotor.step(count, dir,  Adafruit_MotorHAT.MICROSTEP)
        turnOffMotors()
    
    def startPreview(self):
        camera.start_preview(resolution=(1440,1080))
        return
    def stopPreview(self):
        camera.stop_preview()
        return
    
    def captureImageSequence(self):
        return

    def captureSequence(self):
        return

    def __filenames(self):
        self.frame = 0
        __frames = 40
        while self.frame < __frames and self.stepperThread.isAlive():
            yield 'input/image{:02d}.jpeg'.format(self.frame)
            #print('input/image{:02d}.jpeg'.format(self.frame))
            self.frame += 1
    
    def captureSequenceFast(self):
        
       # global stepperThread
        camera.framerate = 10
        sleep(2)

        __start = time.time()
        __stepMultiply = 10
        camera.stop_preview()
        

        print('Stepping UP')
        self.stepperThread = threading.Thread(target=self.stepFor, args = (Adafruit_MotorHAT.FORWARD, self.stepAmount*__stepMultiply))    
        # stepFor(Adafruit_MotorHAT.FORWARD, 40)
        self.stepperThread.start()

        camera.capture_sequence(self.__filenames(), use_video_port=True)

        self.stepperThread.join()
        
        __finish = time.time()    
        print('Captured %d frames at %.2ffps' % (self.frame, self.frame / (__finish - __start)))
        print('Stepping DOWN')
        self.stepFor(Adafruit_MotorHAT.BACKWARD, self.stepAmount*__stepMultiply) 

        turnOffMotors()
        camera.framerate = 40
        return

    
    def setExposure(self):
        camera.exposure_mode = 'auto'
        camera.awb_mode = 'auto'
        camera.iso = 100;
        #camera.framerate = 5

        sleep(2)
        self.shutterSpeed = camera.exposure_speed
        print('Speed        = ', camera.shutter_speed )
        print('Exposure     = ', camera.exposure_speed )
        print('Analog Gain  = ', camera.analog_gain  )
        print('Digital Gain = ', camera.digital_gain )
        camera.shutter_speed = int(self.shutterSpeed*0.95)
        camera.exposure_mode = 'off'
        __g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = __g
        print('')
        print('Speed        = ', camera.shutter_speed )
        print('Exposure     = ', camera.exposure_speed )
        print('Analog Gain  = ', camera.analog_gain  )
        print('Digital Gain = ', camera.digital_gain )
        
        return
    def moreExposure(self):
        self.shutterSpeed = camera.exposure_speed
        print('')
        print('Speed        = ', camera.shutter_speed )
        print('Exposure     = ', camera.exposure_speed )

        camera.shutter_speed = int(self.shutterSpeed*1.05)
        camera.exposure_mode = 'off'
        __g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = __g
        print('')
        print('Speed        = ', camera.shutter_speed )
        print('Exposure     = ', camera.exposure_speed )
        return
    
    def lessExposure(self):
        self.shutterSpeed = camera.exposure_speed
        print('')
        print('Speed        = ', camera.shutter_speed )
        print('Exposure     = ', camera.exposure_speed )
        camera.shutter_speed = int(self.shutterSpeed*0.95)
        camera.exposure_mode = 'off'
        __g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = __g
        print('')
        print('Speed        = ', camera.shutter_speed )
        print('Exposure     = ', camera.exposure_speed )        
        return
    
    def exitGui(self):
        print("Cancel Timer")
        self.timerThread.cancel()
        quit()
        return
