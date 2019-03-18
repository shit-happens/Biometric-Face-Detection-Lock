#Import the necessary packages
import cv2
import os
import subprocess
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from tkinter import *
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)

cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer/recognizer.yml")

#import predictor
from tkinter import ttk
time.sleep(0.1)
def unlock():
    print ("UNLOCKED")
    GPIO.output(21,True)
    return;
window = Toplevel()
blank=" "

window.title(200*blank+"Biometric Face Recognition Lock")
window.geometry('1500x1500')

C = Canvas(window, bg="blue", height=200, width=250)
filename = PhotoImage(file = 'Face.png')
background_label = Label(window, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# If we want to use matrix keypad
def Keypad():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21,GPIO.OUT)
    btn4 = Button(window, text="UNLOCK", command=Function,height=2,width=20,fg='white',bg='black')
    btn4.place(relx=0.5, rely=0.7, anchor=CENTER)
    lbl = Label(window, text="--Enter PIN Here--")
    lbl.place(relx=0.5, rely=0.65, anchor=CENTER)
    txt = Entry(window,width=20)
    txt.place(relx=0.5, rely=0.65, anchor=CENTER)        
#    txt.insert(END, '12')
    txt.place(relx=0.5, rely=0.65, anchor=CENTER)

    K=0
    MATRIX=[[1,2,3],[4,5,6],[7,8,9],['*',0,'#']]
    R=[0,5,6,13]
    C=[19,26,20]
    password="3546"
    p=''
    k=0
    c=0
    for i in range(3):
        GPIO.setwarnings(False)
        GPIO.setup(C[i],GPIO.OUT)
        GPIO.output(C[i],1)
    for j in range(4):
        GPIO.setup(R[j],GPIO.IN,pull_up_down=GPIO.PUD_UP)
    while(True):
                for i in range(3):
                    GPIO.output(C[i],0)
                    for j in range(4):
                        if (GPIO.input(R[j])==0):
                            
                            if((MATRIX[j][i]!='*')&(MATRIX[j][i]!='#')):
                                p=p+str(MATRIX[j][i])
                                print(p)
                                k=k+1
                                txt.insert(END,'*')
                                
                            if((MATRIX[j][i]=='*')):
                                p=p[:-1]
                                print(p)
                                txt.delete(k-1,END)
                                txt.insert(END,'*')
                                
                            
                            if(MATRIX[j][i]=='#'):
                                if(p==password):
                                    unlock()
                                    K=1
                                else:
                                    print("Password doesn't match, Try again!")
                                    p=''
                                    c=c+1
                            
                            while(GPIO.input(R[j])==0):
                                  pass
                            
                    GPIO.output(C[i],1)
                    if(K==1):
                        exedfile('close.py')
                        break
                        
                if(K==1):
                    break
    
    return;

# If we want to use Facial recognition
def captureVid():
    try:
        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(640, 480))
        
        # allow the camera to warmup
        time.sleep(0.1)
        # capture frames from the camera
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                # grab the raw NumPy array representing the image, then initialize the timestamp
                # and occupied/unoccupied text
              width_d, height_d = 280, 280
              X=0
              image = frame.array
              gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
              hist=cv2.equalizeHist(gray)
              blur=cv2.bilateralFilter(hist,9,75,75)
              faces=faceCascade.detectMultiScale(blur,1.3,5)
              for (x,y,w,h) in faces:
                  cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
                  Id,conf=recognizer.predict(cv2.resize(blur[y:y+h,x:x+w], (width_d, height_d)))
                  if (Id==1):
                      Id="Anshit"
                      cv2.putText(image,str(Id),(x,y-10),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),3)
                      unlock()
                      X=1
                      break
                  else:
                      Id="Unknown"
                      cv2.putText(image,str(Id),(x,y-10),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),3)
                      unlock()
                      X=1
                      break
                                   
              cv2.imshow("Face",image)
              key = cv2.waitKey(1) & 0xFF              
              # clear the stream in preparation for the next frame
              rawCapture.truncate(0)
              if key == ord("q"):                  
                  break
             
        camera.stop_preview()
        camera.close()
        cv2.destroyAllWindows()
    except KeyboardInterrupt:
        camera.stop_preview()
        camera.close()
        cv2.destroyAllWindows()
    return;

#This function enable the switch and close the lock by setting pin 21 low
def Function():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21,GPIO.OUT)
    GPIO.output(21,False)
    print('LOCKED')

lbl1 = Label(window, text=200*blank+"Welcome! Unlock using Face Recognition or Entering PIN on the Keypad."+200*blank)
lbl1.grid(column=7, row=0)

#define button for selecting the method 
btn1 = Button(window, text="Recognize Face", command=captureVid,height=2,width=20,fg='white',bg='black')
btn2 = Button(window, text="Keypad Unlock", command=Keypad,height=2,width=20,fg='white',bg='black')
btn3 = Button(window, text="****Lock***", command=Function,height=2,width=20,fg='white',bg='black')

#Position of Buttons in window
btn1.place(relx=0.2, rely=0.5, anchor=CENTER)
btn2.place(relx=0.5, rely=0.6, anchor=CENTER)
btn3.place(relx=0.8, rely=0.5, anchor=CENTER)

window.mainloop()
