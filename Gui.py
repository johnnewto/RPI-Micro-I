##try:
##    # Python2
##    import Tkinter as tk
##    import ttk
##except ImportError:
##    # Python3
##    import tkinter as tk
##    import tkinter.ttk as ttk
from Tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, Checkbutton
import atexit
from UICommands import uiCommands, turnOffMotors

import threading


class uiGui:
    
    def __init__(self, master, hw):
        print ("initialise Gui")
        self.master = master
        self.hw = hw
        
        master.title("Micro-I")
        
        self.label = Label(master, text="Steps:")
        
        vcmd = master.register(self.validateEntry) # we have to wrap the command
        self.entStepAmount = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.entStepAmount.insert(0, '{:02d}'.format(hw.stepAmount))

        self.checkvar = IntVar()
        self.chk = Checkbutton(master, text="SenseCassette", variable=self.checkvar, command=self.setCassetteCheck)

        self.btnUp = Button(master,
                           text="Up",
                           command=hw.stepUp)

        self.btnDown = Button(master,
                           text="Down",
                           command=hw.stepDown)

        self.btnIn= Button(master,
                           text="In",
                           command=hw.stepIn)

        self.btnOut = Button(master,
                           text="Out",
                           command=hw.stepOut)

        self.btnStartPreview = Button(master,
                           text="Start Preview",
                           command=hw.startPreview)
        
        self.btnStopPreview = Button(master,
                           text="Stop Preview",
                           command=hw.stopPreview)

        self.btnCapture = Button(master,
                           text="Capture Stepper Sequence",
                           command=hw.captureSequence)


        self.btnCaptureFast = Button(master,
                           text="Capture Stepper Sequence Fast",
                           command=hw.captureSequenceFast)


        self.btnCaptureSeq = Button(master,
                           text="Capture Image Sequence",
                           command=hw.captureImageSequence)


        self.btnSetExposure = Button(master, 
                           text="Set Exposure", 
                           command=hw.setExposure)


        self.btnGtrExposure = Button(master, 
                           text="> Exposure", 
                           command=hw.moreExposure)


        self.btnLsrExposure = Button(master, 
                           text="< Exposure", 
                           command=hw.lessExposure)

        self.btnQuit = Button(master, 
                           text="QUIT", 
                           fg="red",
                           command=hw.exitGui)


        # LAYOUT
        self.entStepAmount.grid(row=1, column=0)

        self.chk.grid(row=1, column=1)
        
        self.btnUp.grid(row=2, column=0, sticky=W, pady=4)
                         
        self.btnDown.grid(row=3, column=0, sticky=W, pady=4)
        
        self.btnIn.grid(row=2, column=1, sticky=W, pady=4)
                         
        self.btnOut.grid(row=3, column=1, sticky=W, pady=4)

        self.btnStartPreview.grid(row=4, column=0, sticky=W, pady=4)

        self.btnStopPreview.grid(row=5, column=0, sticky=W, pady=4)

        self.btnCapture.grid(row=6, column=0, sticky=W, pady=4)

        self.btnCaptureFast.grid(row=7, column=0, sticky=W, pady=4)

        self.btnCapture.grid(row=8, column=0, sticky=W, pady=4)

        self.btnSetExposure.grid(row=9, column=0, sticky=W, pady=4)

        self.btnGtrExposure.grid(row=10, column=0, sticky=W, pady=4)

        self.btnLsrExposure.grid(row=11, column=0, sticky=W, pady=4)

        self.btnQuit.grid(row=12, column=0, sticky=W, pady=4)
        self.btnDown.bind('<Button-1>', self.parse)
        

        master.bind_all('u', hw.stepUp)  
        master.bind_all('d', hw.stepDown)  
        master.bind_all('i', hw.stepIn)  
        master.bind_all('o', hw.stepOut)  
        master.bind_all('c', hw.captureSequence)  
        master.bind_all('s', hw.stopPreview)  
        master.bind_all('x', hw.setExposure)  
        master.bind_all('q', hw.exitGui)

    def parse(self, event):
        print("You clicked?")

    def validateEntry(self, new_text):
        if not new_text: # the field is being cleared
            self.hw.setStepAmount(0) 
            return True

        try:
            self.hw.setStepAmount(int(new_text))
            return True
        except ValueError:
            return False
        
    def setCassetteCheck(self):
        #print("CheckVar = {:02d}".format(self.checkvar))
        print "variable is", self.checkvar.get()
        if self.checkvar.get() == 1:
            self.hw.runCassetteMotorOnSense = True
        else:
            self.hw.runCassetteMotorOnSense = False
        print "variable is", self.hw.runCassetteMotorOnSense
                
        


class testUICommands:
    def stepUp(self):
        return
    def stepDown(self):
        return
    def startPreview(self):
        return
    def stopPreview(self):
        return
    def captureImageSequence(self):
        return

    def captureSequence(self):
        return
    def captureSequenceFast(self):
        return
    def setExposure(self):
        return
    def moreExposure(self):
        return
    def lessExposure(self):
        return
    def exitGui(self):
        quit()
        return







if __name__ == "__main__":
    window = Tk()
    window.geometry('300x500+0+100')
    ui_Commands = uiCommands()
    gui = uiGui(window,ui_Commands)


    

    window.mainloop()
    
