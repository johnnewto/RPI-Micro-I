
import io
import time
import picamera

with picamera.PiCamera() as camera:
    # Set the camera's resolution to VGA @40fps and give it a couple
    # of seconds to measure exposure etc.
    #camera.resolution = (640, 480)
    #camera.resolution = (3280//2, 2464//2)
    camera.resolution = (3280, 2464)
    #camera.resolution = (1648, 1232)
    #camera.resolution = (1664, 1232)
    #camera.resolution = (2800, 2464)
    camera.framerate = 80
    numImages = 10
    time.sleep(2)
    # Set up 40 in-memory streams
    outputs = [io.BytesIO() for i in range(numImages)]
    start = time.time()
    camera.capture_sequence(outputs, format='jpeg', use_video_port=True)
    finish = time.time()
    # How fast were we?
    print('Captured %d images at %.2ffps' % (numImages, numImages / (finish - start)))
