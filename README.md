# Biometric-Face-Detection-Lock
INTRODUCTION~
House security matters and people always try to make life easier at the same time.
That’s why we put up with our project, Face Recognition Door Lock System.
We developed this system based on Raspberry-pi 3, to make the house only accessible
when your face is recognized by the recognition algorithms from OpenCV library and meanwhile
you are allowed in by the house owner, who could monitor entrance remotely. 
By doing so, the system is less likely to be deceived: since the owner can check 
each visitor in the remote console, getting recognized by the camera using a photo
won’t work. We also added passcode function for entrance in case that face recognition part corrupts.

OBJECTIVES~
Users could operate on a touchscreen to select entering the house by recognizing face or entering passcode. 

For face recognition, an image will be captured by pi camera and preprocessed by Raspberry pi like converting,
resizing and cropping. Then face detection and recognition are performed. For passcode part, users could enter
or reset passcode through a keypad.

EQUIPMENTS REQUIRED~
1. Raspberry-Pi Model B
2. 16GB Micro-SD Card
3. Raspberry Pi Camera Module V2
3. Segolike DC12V Lock Tongue Luggage Electric Solenoid Assembly for Auto Door Sauna Cabinet Drawer
4. Jumper Wires
5. Adafruit piTFT 320X240 Screen
6. 4X3 Matrix Keypad

PROCEDURE~
1. Format the Micro-SD card and install Raspbian in it from https://www.raspberrypi.org/downloads/raspbian 
2. After setting up your raspberry-pi, install OpenCV library using pip3.
3. Connect picam and enable its configuration from raspberry pi configuration.
4. Connect the piTFT screen and set it up using the following article~ 
https://raspberrypi.stackexchange.com/questions/55575/how-do-i-setup-the-pitft-plus-3-5-touchscreen
5. Connect rest of the components as per the diagram given below~


6. Clone the repository into your Raspberry-Pi environment.
7. To generate your own dataset, Open Python3 & run dataset generator.py .Provide unique ID to every person in your database for convineince.
8. To train the face recognition model, run trainer.py 
9. If you have made until now, then congratulations! Now you only have to run interface.py to launch the User Interface.
10. Incase you want to operate the system seperately for face-unlock and matrix-unlock, you can run predictor.py or matrix.py separately.

CHEERS!
