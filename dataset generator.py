#Import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
sampleNum=0
Id=input('Enter the ID: ') # Give a unique ID to each particular indivisual for convinience
Name=input('Enter your Name: ') # Enter the name of the person whose database you have to generate

# allow the camera to warmup
time.sleep(0.1)


# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    # grab the raw NumPy array representing the image, then initialize the timestamp
   	 # and occupied/unoccupied text
    image = frame.array   
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # Converting coloured images to grayscale, because our LBPH_recognizer trains only on gray images
    hist=cv2.equalizeHist(gray)
    blur=cv2.bilateralFilter(hist,9,75,75)
    faces=faceDetect.detectMultiScale(blur,1.3,5) 
    for (x,y,w,h) in faces:
        sampleNum=sampleNum+1
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2) # Generating rectangle around the faces
        cv2.imwrite("dataset/"+Name+"."+str(Id)+"."+str(sampleNum)+".jpg",blur[y:y+h,x:x+h]) # writing images into dataset folder
        cv2.waitKey(10)
    cv2.imshow("Face",image)
    cv2.waitKey(10)
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    if (sampleNum>99): # You can change 99 to any desired number for varying number of images per person 
        break
camera.stop_preview()   
camera.close()
cv2.destroyAllWindows()

