#Import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)

cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

#Read LBPH Face Recognizer from recognizer folder
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer/recognizer.yml")

def unlock():
    print ("UNLOCKED!")
    GPIO.output(21,True)
    return;

def captureVid():
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
                  break
              else:
                  Id="Unknown"
                  cv2.putText(image,str(Id),(x,y-10),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),3)
                  unlock()
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

captureVid()
    