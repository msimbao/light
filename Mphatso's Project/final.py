"Import Important Modules For Hardware and GUI"
import random
import pygame

import tkinter as tk
import PIL
import PIL.Image as Image
import PIL.ImageTk as ImageTk

import RPi.GPIO as GPIO
import time

import LCD1602


"Initialize important storage variables for reusable strings, lists and numbers"

colors = [0xFF0000, 0xFF6600, 0x0000FF, 0xFFF00, 0xFF00FF, 0x00FFFF]

habit_tracker_colors = [0xA9EAD2,0xdcedc1,0xFF00FF]

R = 11
G = 12
B = 13

RelayPin = 29

habit_file = open("_memory/habit_tracking","r")
count=habit_file.readline()
     
habit_file.close()

"Hardware Setup Functions For LED and Relay Controls"

def setup(Rpin, Gpin, Bpin):
    global pins
    global p_R, p_G, p_B
    pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)  # Set pins' mode is output
        GPIO.output(pins[i], GPIO.HIGH)  # Set pins to high(+3.3V) to off led

    p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
    p_G = GPIO.PWM(pins['pin_G'], 1999)
    p_B = GPIO.PWM(pins['pin_B'], 5000)

    p_R.start(100)  # Initial duty Cycle = 0(leds off)
    p_G.start(100)
    p_B.start(100)
    
    #Set Up pins for other hardware
 
    
    GPIO.setup(RelayPin, GPIO.OUT) #Relay 
    GPIO.output(RelayPin, GPIO.HIGH)
    
    LCD1602.init(0x27, 0)	# init(slave address, background light) #LCD
    LCD1602.write(0, 0, 'Hello!')
    LCD1602.write(1, 1, '(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ ')
    time.sleep(2)
    

    
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def off():
    for i in pins:
        GPIO.output(pins[i], GPIO.HIGH)  # Turn off all leds

def setColor(col):  # For example : col = 0x112233
    R_val = (col & 0xff0000) >> 16
    G_val = (col & 0x00ff00) >> 8
    B_val = (col & 0x0000ff) >> 0

    R_val = map(R_val, 0, 255, 0, 100)
    G_val = map(G_val, 0, 255, 0, 100)
    B_val = map(B_val, 0, 255, 0, 100)

    p_R.ChangeDutyCycle(100 - R_val)  # Change duty cycle
    p_G.ChangeDutyCycle(100 - G_val)
    p_B.ChangeDutyCycle(100 - B_val)



def loop(dur):
	while True:
		for col in colors:
			setColor(col)
			time.sleep(dur)
def destroy():
    p_R.stop()
    p_G.stop()
    p_B.stop()
    GPIO.output(RelayPin, GPIO.HIGH)
    off()
    GPIO.cleanup()
    
    
    

class MainWindow:
    "An object containing a GUI program for running the Raspberry Pi Hardware"

    def __init__(self, master):
        "Initialize the GUI and the basic widgets for the main window"
        self.master = master
        self.frame = tk.Frame(self.master,width=600,height=400)
        
        "Initialize important Hardware Functions"
        
        setup(R, G, B)
        setColor(0xFF00FF)
        GPIO.output(RelayPin, GPIO.LOW)
       
        "Initialize Music"
        
        pygame.mixer.init()
        pygame.mixer.music.load("_music/bensound-tenderness.mp3")
        pygame.mixer.music.play()
        
        "Read in Habit_Tracker and saved habit tracking day streak"


        
        
        "Open and collect images for main window GUI"
        
        "Settings Icon"
        settingspic = Image.open("_images/Slide10.png")
        settingspic = settingspic.resize((40,20), Image.ANTIALIAS)
        self.set = ImageTk.PhotoImage(settingspic)
        
        "Colors Menu Icon"
        colorspic = Image.open("_images/Slide11.png")
        colorspic = colorspic.resize((40,20), Image.ANTIALIAS)
        self.col = ImageTk.PhotoImage(colorspic)
        
        "Close Menu Icon"
        close = Image.open("_images/Slide13.png")
        close = close.resize((40,20), Image.ANTIALIAS)
        self.cl = ImageTk.PhotoImage(close)
        
        
        mainBackgroundPic = Image.open("_images/Slide01.png")
        mainBackgroundPict = mainBackgroundPic.resize((700,400), Image.ANTIALIAS)
        self.mainPic = ImageTk.PhotoImage(mainBackgroundPic)  # IMAGES MUST ALWAYS BE OBJECT VARIABLES!!
        imgLabel = tk.Label(self.frame, image=self.mainPic,height=400,width=700)
        imgLabel.grid(row=0, column=0,rowspan=8,columnspan=40)

        "Button to open the Settings Window"
        self.button1 = tk.Button(self.frame, image=self.set, width ="30",height="20", command = self.set_window,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.button1.grid(row=7, column=1)

        "Button to open the Colors Info Window"
        self.bacteria = tk.Button(self.frame,image=self.col, width ="30",height="20", command = self.new_window,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.bacteria.grid(row=7,column=2)

        "Button to Close the entire GUI"
        self.close = tk.Button(self.frame, image=self.cl, width ="30",height="20", command = self.close_windows,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.close.grid(row=7, column=3)
        
        "Label for counting habit days"
        self.userCount = tk.Button(self.frame,text="", width="1", height ="1", command = self.add_count, bg="white", borderwidth="0",highlightbackground="white",activebackground="orange")
        self.userCount.grid(row=1, column=1)
        
        self.countLabel = tk.Label(self.frame,text=count, width="0",height="0")
        
        "Setup button control for counting days in habit traker"
  
        
        self.frame.pack()
        
        

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = ColorsWindow(self.newWindow)
        
    def set_window(self):
        self.setWindow = tk.Toplevel(self.master)
        self.app = SettingsWindow(self.setWindow)

    def close_windows(self):
        self.master.destroy()
        destroy()
    
    def add_count(self):
        count = self.countLabel["text"]
        days = int(count) + 1
        
        
        LCD1602.init(0x27, 1)
        LCD1602.write(0, 0, 'Your Count is')
        streak = str(days) + " " "days      "
        LCD1602.write(1, 1, streak)
        time.sleep(5)

        for col in habit_tracker_colors:
            setColor(col)
            time.sleep(0.5)
        
        outfile = open("_memory/habit_tracking","w")
        outfile.write(str(days))
    
        outfile.close()
        
        LCD1602.init(0x27, 0)
        LCD1602.clear()
        
        

class SettingsWindow:
    def __init__(self, master):
        "Initialize the GUI and widgets for the Settings Menu Window"
        self.master = master
        self.frame = tk.Frame(self.master,width=600,height=400)
        
        "Open and collect images for window GUI"
        
        "Home Icon"
        homepic = Image.open("_images/Slide12.png")
        homepic = homepic.resize((40,20), Image.ANTIALIAS)
        self.home = ImageTk.PhotoImage(homepic)
        
        "red Icon"
        redpic = Image.open("_images/Slide14.png")
        redpic = redpic.resize((90,20), Image.ANTIALIAS)
        self.red = ImageTk.PhotoImage(redpic)
        
        "orange Icon"
        opic = Image.open("_images/Slide15.png")
        opic = opic.resize((90,20), Image.ANTIALIAS)
        self.orange = ImageTk.PhotoImage(opic)
        
        "yellow Icon"
        yPic = Image.open("_images/Slide19.png")
        yPic = yPic.resize((90,20), Image.ANTIALIAS)
        self.yellow = ImageTk.PhotoImage(yPic)
        
        "green Icon"
        gPic = Image.open("_images/Slide16.png")
        gPic = gPic.resize((90,20), Image.ANTIALIAS)
        self.green = ImageTk.PhotoImage(gPic)
        
        "blue Icon"
        bPic = Image.open("_images/Slide18.png")
        bPic = bPic.resize((90,20), Image.ANTIALIAS)
        self.blue = ImageTk.PhotoImage(bPic)
        
        "purple Icon"
        pPic = Image.open("_images/Slide17.png")
        pPic = pPic.resize((90,20), Image.ANTIALIAS)
        self.purple = ImageTk.PhotoImage(pPic)
        
        "15 min Icon"
        fifPic = Image.open("_images/Slide20.png")
        fifPic = fifPic.resize((90,40), Image.ANTIALIAS)
        self.fif = ImageTk.PhotoImage(fifPic)
        
        "30 min Icon"
        thirtyPic = Image.open("_images/Slide21.png")
        thirtyPic = thirtyPic.resize((90,40), Image.ANTIALIAS)
        self.thirty = ImageTk.PhotoImage(thirtyPic)
        
        "1 hour Icon"
        onePic = Image.open("_images/Slide22.png")
        onePic = onePic.resize((90,40), Image.ANTIALIAS)
        self.one = ImageTk.PhotoImage(onePic)
        
        "2 hour Icon"
        twoPic = Image.open("_images/Slide23.png")
        twoPic = twoPic.resize((90,40), Image.ANTIALIAS)
        self.two = ImageTk.PhotoImage(twoPic)
        
        "5 hour Icon"
        fivePic = Image.open("_images/Slide24.png")
        fivePic = fivePic.resize((90,20), Image.ANTIALIAS)
        self.five = ImageTk.PhotoImage(fivePic)
        
        "Background Image"
        mainBackgroundPic = Image.open("_images/Slide09.png")
        mainBackgroundPict = mainBackgroundPic.resize((700,400), Image.ANTIALIAS)
        self.mainPic = ImageTk.PhotoImage(mainBackgroundPic)  # IMAGES MUST ALWAYS BE OBJECT VARIABLES!!
        imgLabel = tk.Label(self.frame, image=self.mainPic,height=400,width=700)
        imgLabel.grid(row=0, column=0,rowspan=9,columnspan=40)
        
        "Button to open the Settings Window"
        self.button1 = tk.Button(self.frame, image=self.home, width ="30",height="20", command = self.close_windows,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.button1.grid(row=8, column=1)
        
        self.rButton = tk.Button(self.frame, image=self.red, width ="100",height="20", command = self.red_led,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.rButton.grid(row=3, column=20)
        
        self.oButton = tk.Button(self.frame, image=self.orange, width ="100",height="20", command = self.orange_led,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.oButton.grid(row=4, column=20)
        
        self.yButton = tk.Button(self.frame, image=self.yellow, width ="100",height="20", command = self.yellow_led,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.yButton.grid(row=5, column=20)
        
        self.gButton = tk.Button(self.frame, image=self.green, width ="100",height="20", command = self.green_led,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.gButton.grid(row=6, column=20)
        
        self.bButton = tk.Button(self.frame, image=self.blue, width ="100",height="20", command = self.blue_led,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.bButton.grid(row=7, column=20)
        
        self.pButton = tk.Button(self.frame, image=self.purple, width ="100",height="20", command = self.purple_led,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.pButton.grid(row=8, column=20)
        
        self.fifButton = tk.Button(self.frame, image=self.fif, width ="130",height="30", command = self.fif_min,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.fifButton.grid(row=3, column=24)
        
        self.thirtyButton = tk.Button(self.frame, image=self.thirty, width ="130",height="30", command = self.thirty_min,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.thirtyButton.grid(row=4, column=24)
        
        self.oneButton = tk.Button(self.frame, image=self.one, width ="130",height="30", command = self.one_hour,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.oneButton.grid(row=3, column=27)
        
      
        
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()
        setColor(0xFF0000)

    def red_led(self):
        setColor(0xFF0000)
    
    def orange_led(self):
        setColor(0xFF6600)
        
    def yellow_led(self):
        setColor(0xFFF000)
        
    def green_led(self):
        setColor(0x00FF00)
        
    def blue_led(self):
        setColor(0x000FFF)
        
    def purple_led(self):
        setColor(0xFF00FF)
        
    def fif_min(self):
        for col in colors:
            try:
                setColor(col)
                time.sleep(5)
            except KeyboardInterrupt: #I've shortened the actual times to avoid a long loop when testing
                break
        
    
    def thirty_min(self):
        for col in colors:
            setColor(col)
            time.sleep(1) #I've shortened the actual times to avoid a long loop when testing
    
    def one_hour(self):
        GPIO.output(RelayPin, GPIO.LOW) #I've shortened the actual times to avoid a long loop when testing


class ColorsWindow:
    def __init__(self, master):
        "Initialize the GUI and widgets for the Colors Menu Window"
        self.master = master
        self.frame = tk.Frame(self.master,width=600,height=400)
        
        "Open and collect images for main window GUI"
        
        "Home Icon"
        homepic = Image.open("_images/Slide12.png")
        homepic = homepic.resize((40,20), Image.ANTIALIAS)
        self.home = ImageTk.PhotoImage(homepic)
        
        "red Icon"
        redpic = Image.open("_images/red.png")
        redpic = redpic.resize((90,100), Image.ANTIALIAS)
        self.red = ImageTk.PhotoImage(redpic)
        
        "orange Icon"
        opic = Image.open("_images/orange.png")
        opic = opic.resize((90,100), Image.ANTIALIAS)
        self.orange = ImageTk.PhotoImage(opic)
        
        "yellow Icon"
        yPic = Image.open("_images/yellow.png")
        yPic = yPic.resize((90,100), Image.ANTIALIAS)
        self.yellow = ImageTk.PhotoImage(yPic)
        
        "green Icon"
        gPic = Image.open("_images/green.png")
        gPic = gPic.resize((90,100), Image.ANTIALIAS)
        self.green = ImageTk.PhotoImage(gPic)
        
        "blue Icon"
        bPic = Image.open("_images/blue.png")
        bPic = bPic.resize((90,100), Image.ANTIALIAS)
        self.blue = ImageTk.PhotoImage(bPic)
        
        "purple Icon"
        pPic = Image.open("_images/purple.png")
        pPic = pPic.resize((90,100), Image.ANTIALIAS)
        self.purple = ImageTk.PhotoImage(pPic)
        
        "Background Image"
        mainBackgroundPic = Image.open("_images/colors.png")
        mainBackgroundPict = mainBackgroundPic.resize((700,400), Image.ANTIALIAS)
        self.mainPic = ImageTk.PhotoImage(mainBackgroundPic)  # IMAGES MUST ALWAYS BE OBJECT VARIABLES!!
        imgLabel = tk.Label(self.frame, image=self.mainPic,height=400,width=700)
        imgLabel.grid(row=0, column=0,rowspan=8,columnspan=40)
        
        "Button to open the Settings Window"
        self.button1 = tk.Button(self.frame, image=self.home, width ="30",height="20", command = self.close_windows,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.button1.grid(row=7, column=1)
        
        self.rButton = tk.Button(self.frame, image=self.red, width ="100",height="100", command = self.red_window,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.rButton.grid(row=3, column=31)
        
        self.oButton = tk.Button(self.frame, image=self.orange, width ="100",height="100", command = self.orange_window,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.oButton.grid(row=3, column=33)
        
        self.yButton = tk.Button(self.frame, image=self.yellow, width ="100",height="100", command = self.yellow_window,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.yButton.grid(row=3, column=35)
        
        self.gButton = tk.Button(self.frame, image=self.green, width ="100",height="100", command = self.green_window,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.gButton.grid(row=4, column=31)
        
        self.bButton = tk.Button(self.frame, image=self.blue, width ="100",height="100", command = self.blue_window,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.bButton.grid(row=4, column=33)
        
        self.pButton = tk.Button(self.frame, image=self.purple, width ="100",height="100", command = self.purple_window,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.pButton.grid(row=4, column=35)
        
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()

    def red_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = RedWindow(self.newWindow)
    
    def orange_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = OrangeWindow(self.newWindow)
        
    def yellow_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = YellowWindow(self.newWindow)
        
    def green_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = GreenWindow(self.newWindow)
        
    def blue_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = BlueWindow(self.newWindow)
        
    def purple_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = PurpleWindow(self.newWindow)
        
class RedWindow:
    def __init__(self, master):
        "Initialize the GUI and widgets for the Red Info Window"
        self.master = master
        self.frame = tk.Frame(self.master,width=600,height=400)
        
        "Open and collect images for window GUI"
        
        "Home Icon"
        homepic = Image.open("_images/Slide12.png")
        homepic = homepic.resize((40,20), Image.ANTIALIAS)
        self.home = ImageTk.PhotoImage(homepic)
        
        "Background Image"
        mainBackgroundPic = Image.open("_images/Slide08.png")
        mainBackgroundPict = mainBackgroundPic.resize((700,400), Image.ANTIALIAS)
        self.mainPic = ImageTk.PhotoImage(mainBackgroundPic)  # IMAGES MUST ALWAYS BE OBJECT VARIABLES!!
        imgLabel = tk.Label(self.frame, image=self.mainPic,height=400,width=700)
        imgLabel.grid(row=0, column=0,rowspan=8,columnspan=40)
        
        "Button to open the Settings Window"
        self.button1 = tk.Button(self.frame, image=self.home, width ="30",height="20", command = self.close_windows,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.button1.grid(row=7, column=1)
        
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()
        
class OrangeWindow:
    def __init__(self, master):
        "Initialize the GUI and widgets for the Orange Info Window"
        self.master = master
        self.frame = tk.Frame(self.master,width=600,height=400)
        
        "Open and collect images for window GUI"
        
        "Home Icon"
        homepic = Image.open("_images/Slide12.png")
        homepic = homepic.resize((40,20), Image.ANTIALIAS)
        self.home = ImageTk.PhotoImage(homepic)
        
        "Background Image"
        mainBackgroundPic = Image.open("_images/Slide03.png")
        mainBackgroundPict = mainBackgroundPic.resize((700,400), Image.ANTIALIAS)
        self.mainPic = ImageTk.PhotoImage(mainBackgroundPic)  # IMAGES MUST ALWAYS BE OBJECT VARIABLES!!
        imgLabel = tk.Label(self.frame, image=self.mainPic,height=400,width=700)
        imgLabel.grid(row=0, column=0,rowspan=8,columnspan=40)
        
        "Button to open the Settings Window"
        self.button1 = tk.Button(self.frame, image=self.home, width ="30",height="20", command = self.close_windows,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.button1.grid(row=7, column=1)
        
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()
        
class YellowWindow:
    def __init__(self, master):
        "Initialize the GUI and widgets for the Yellow Info Window"
        self.master = master
        self.frame = tk.Frame(self.master,width=600,height=400)
        
        "Open and collect images for window GUI"
        
        "Home Icon"
        homepic = Image.open("_images/Slide12.png")
        homepic = homepic.resize((40,20), Image.ANTIALIAS)
        self.home = ImageTk.PhotoImage(homepic)
        
        "Background Image"
        mainBackgroundPic = Image.open("_images/Slide07.png")
        mainBackgroundPict = mainBackgroundPic.resize((700,400), Image.ANTIALIAS)
        self.mainPic = ImageTk.PhotoImage(mainBackgroundPic)  # IMAGES MUST ALWAYS BE OBJECT VARIABLES!!
        imgLabel = tk.Label(self.frame, image=self.mainPic,height=400,width=700)
        imgLabel.grid(row=0, column=0,rowspan=8,columnspan=40)
        
        "Button to close the Window"
        self.button1 = tk.Button(self.frame, image=self.home, width ="30",height="20", command = self.close_windows,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.button1.grid(row=7, column=1)
        
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()
        
class GreenWindow:
    def __init__(self, master):
        "Initialize the GUI and widgets for the Green Info Window"
        self.master = master
        self.frame = tk.Frame(self.master,width=600,height=400)
        
        "Open and collect images for window GUI"
        
        "Home Icon"
        homepic = Image.open("_images/Slide12.png")
        homepic = homepic.resize((40,20), Image.ANTIALIAS)
        self.home = ImageTk.PhotoImage(homepic)
        
        "Background Image"
        mainBackgroundPic = Image.open("_images/Slide06.png")
        mainBackgroundPict = mainBackgroundPic.resize((700,400), Image.ANTIALIAS)
        self.mainPic = ImageTk.PhotoImage(mainBackgroundPic)  # IMAGES MUST ALWAYS BE OBJECT VARIABLES!!
        imgLabel = tk.Label(self.frame, image=self.mainPic,height=400,width=700)
        imgLabel.grid(row=0, column=0,rowspan=8,columnspan=40)
        
        "Button to close the Window"
        self.button1 = tk.Button(self.frame, image=self.home, width ="30",height="20", command = self.close_windows,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.button1.grid(row=7, column=1)
        
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()
        
class BlueWindow:
    def __init__(self, master):
        "Initialize the GUI and widgets for the Blue Info Window"
        self.master = master
        self.frame = tk.Frame(self.master,width=600,height=400)
        
        "Open and collect images for window GUI"
        
        "Home Icon"
        homepic = Image.open("_images/Slide12.png")
        homepic = homepic.resize((40,20), Image.ANTIALIAS)
        self.home = ImageTk.PhotoImage(homepic)
        
        "Background Image"
        mainBackgroundPic = Image.open("_images/Slide05.png")
        mainBackgroundPict = mainBackgroundPic.resize((700,400), Image.ANTIALIAS)
        self.mainPic = ImageTk.PhotoImage(mainBackgroundPic)  # IMAGES MUST ALWAYS BE OBJECT VARIABLES!!
        imgLabel = tk.Label(self.frame, image=self.mainPic,height=400,width=700)
        imgLabel.grid(row=0, column=0,rowspan=8,columnspan=40)
        
        "Button to close the Window"
        self.button1 = tk.Button(self.frame, image=self.home, width ="30",height="20", command = self.close_windows,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.button1.grid(row=7, column=1)
        
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()
        
class PurpleWindow:
    def __init__(self, master):
        "Initialize the GUI and widgets for the Purple Info Window"
        self.master = master
        self.frame = tk.Frame(self.master,width=600,height=400)
        
        "Open and collect images for window GUI"
        
        "Home Icon"
        homepic = Image.open("_images/Slide12.png")
        homepic = homepic.resize((40,20), Image.ANTIALIAS)
        self.home = ImageTk.PhotoImage(homepic)
        
        "Background Image"
        mainBackgroundPic = Image.open("_images/Slide04.png")
        mainBackgroundPict = mainBackgroundPic.resize((700,400), Image.ANTIALIAS)
        self.mainPic = ImageTk.PhotoImage(mainBackgroundPic)  # IMAGES MUST ALWAYS BE OBJECT VARIABLES!!
        imgLabel = tk.Label(self.frame, image=self.mainPic,height=400,width=700)
        imgLabel.grid(row=0, column=0,rowspan=8,columnspan=40)
        
        "Button to close the Window"
        self.button1 = tk.Button(self.frame, image=self.home, width ="30",height="20", command = self.close_windows,bg="white",borderwidth=0,highlightbackground="white",activebackground="white")
        self.button1.grid(row=7, column=1)
        
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()

def main():
    
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
    

if __name__ == '__main__':
     
    main()
