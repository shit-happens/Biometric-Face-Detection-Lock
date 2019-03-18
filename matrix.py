#Import the necessary packages
import RPi.GPIO as GPIO #import all the GPIO pins
import time
import os

GPIO.setmode(GPIO.BCM) #setup Board Mode(we can also setup GPIO.BOARD, then we have to change pins value
GPIO.setup(21,GPIO.OUT) # take pin 21 as a output pin

# Unlock funtion to unlock the Face-lock by setting up pin 21 high and enable the switch
def unlock():
    print ("UNLOCKED")
    GPIO.output(21,True)
    time.sleep(10)
    GPIO.output(21,False)
    return;

K=0
MATRIX=[[1,2,3],[4,5,6],[7,8,9],['*',0,'#']] #keypad matrix Numbers
R=[0,5,6,13]
C=[19,26,20]
password="3546" # Password PIN set to '3546'
p=''
k=''
c=0

#set coloum buttons as output pins and rows Button as Input pins by using the pullup resistors
for i in range(3):
    GPIO.setwarnings(False)
    GPIO.setup(C[i],GPIO.OUT)
    GPIO.output(C[i],1)
for j in range(4):
    GPIO.setup(R[j],GPIO.IN,pull_up_down=GPIO.PUD_UP)
try:
    while(True):
        for i in range(3):
            GPIO.output(C[i],0)
            for j in range(4):
                if (GPIO.input(R[j])==0):
                    
                    if((MATRIX[j][i]!='*')&(MATRIX[j][i]!='#')):
                        p=p+str(MATRIX[j][i])
                        print(p)
                        k=k+'*'
                        print(k)
                        
                    if((MATRIX[j][i]=='*')):
                        p=p[:-1]
                        print(p)
                        k=k[:-1]
                        print(k)
                    
                    if(MATRIX[j][i]=='#'):
                        if(p==password):
                            unlock()
                            K=1
                        else:
                            print("Password Doesn't match, Try again")
                            p=''
                            c=c+1
                    
                    while(GPIO.input(R[j])==0):
                          pass
                    
            GPIO.output(C[i],1)
            if(K==1):
                break
                
        if(K==1):
            break
except KeyboardInterrupt:
    GPIO.cleanup()
    
