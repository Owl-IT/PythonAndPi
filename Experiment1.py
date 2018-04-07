from tkinter import * # pylint: disable=W0614

import RPi.GPIO as GPIO

mode = GPIO.BOARD
ledChannel = 11
pushChannel = 12
msgCount = 0

def destroy():
    try:
        GPIO.output(ledChannel, False)
        GPIO.cleanup()
    except:
        print("Error in destroy() ", sys.exc_info()[1])

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def client_exit(self):
        self.master.destroy()

    def ledOn(self):
        GPIO.output(ledChannel, True)

    def ledOff(self):
        GPIO.output(ledChannel, False)

    def init_window(self):
        self.master.title("Testing RPi.GPIO")
        self.pack(fill=BOTH, expand=1)
        self.quitButton = Button(self, text="Exit", command=self.client_exit)
        self.quitButton.place(x=0, y=0)
        self.ledOnButton = Button(self, text="LED on", command=self.ledOn)
        self.ledOnButton.place(x=100, y=0)
        self.ledOffButton = Button(self, text="LED off", command=self.ledOff)
        self.ledOffButton.place(x=200, y=0)
        self.pushText = Text(self, height=4, width=40)
        self.pushText.place(x=100, y=100)

    def gpioCallback(self, channel):
        global msgCount
        msg = "pressed" if GPIO.input(pushChannel) else "not pressed"
        self.pushText.delete("1.0", END)
        self.pushText.insert(END, msg)
        msgCount = msgCount + 1
        print(msgCount, msg)

class App(): 
    def __init__(self):
        self.root = Tk()
        self.root.geometry("400x300")
        self.window = Window(self.root)
        
    def run(self):
        GPIO.setmode(mode)
        GPIO.setup(ledChannel, GPIO.OUT)
        GPIO.setup(pushChannel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pushChannel, GPIO.BOTH, callback=self.window.gpioCallback)
        self.root.mainloop()        

app = App()
try:
    app.run()
except:
    print("Error in app.run() ", sys.exc_info()[1])
finally:
    destroy()

