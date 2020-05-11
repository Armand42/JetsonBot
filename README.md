# JetsonBot
### Autonomous Object Tracking Car 

The purpose of this project was to combine multiple technologies into an autonomous object tracking car. The main two hardware components used were Nvidia's Jetson Nano and an Arduino developer board. The software used was written in Python 3.6 and utilized both OpenCv for object tracking and the pyfiramta library for servo and motor control. The car is currently able to lock onto a target of a specified color and follow that target until a certain proximity. A custom gimbal made from 2 servos allow a 2-axis rotation for the Arducam camera so that a full 2-axis object tracking can take place. Eventually, this robot will be improved and will deploy a machine learning model using Convolutional Neural Networks so that object tracking can specified to a trained target.

### To compile and Run
1) Make sure the Arduino is connected to the Jetson Nano. Open a terminal a enter the following command:
```
sudo chmod 666 /dev/ttyACM0 
```
2) In the same terminal window, run the script by typing:
```
python3 robot.py
```

Note: If you encounter any errors regarding the video camera, change the value of: camera = cv2.VideoCapture(-1) to camera = cv2.VideoCapture(0). Different machines may require different camera port access, so be sure that the camera is connected.
