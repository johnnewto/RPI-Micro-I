from Stepper import stepper
#import RPi.GPIO as gpio
#import gpiozero


#gpio.cleanup()
#stepper variables
#[stepPin, directionPin, enablePin]
testStepper = stepper([23, 24, 22])

#test stepper

testStepper.step(1000, "right"); #steps, dir, speed, stayOn

#clean up GPIO before end
testStepper.cleanGPIO()
