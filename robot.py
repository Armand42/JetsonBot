# sudo chmod 666 /dev/ttyACM0 
# May need to change video value from 0 to -1
# Restart computer everytime you swap cameras
# Pyfirmata library must be uploaded to Arduino board
# Machine Learning Object Recognition Robot
# import the necessary packages
from collections import deque
from pyfirmata import Arduino, util
from pyfirmata import ArduinoMega
from pyfirmata import INPUT, OUTPUT, PWM
import RPi.GPIO as GPIO
import numpy as np
import argparse
import imutils
import cv2
import math
import pandas as pd
import matplotlib.pyplot as plt
import time
import serial   # import serial library
arduinoSerialData = serial.Serial('/dev/ttyACM0', 9600, timeout=10)

board = ArduinoMega('/dev/ttyACM0')
servoX = board.get_pin('d:3:s')
servoY = board.get_pin('d:2:s')
# for 1st Motor on ENA
ENA = 33
IN1 = 35
IN2 = 37

# set pin numbers to the board's
GPIO.setmode(GPIO.BOARD)

# initialize EnA, In1 and In2
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)

# GPIO.output(IN1, GPIO.HIGH)
# GPIO.output(IN2, GPIO.HIGH)

# time.sleep(5)
# GPIO.output(IN1, GPIO.LOW)
# GPIO.output(IN2, GPIO.LOW)

# Initialize servo angles
angleX = 90
angleY = 90
# Servo tilt functions
def moveServoX(v):
    servoX.write(v)
def moveServoY(v):
    servoY.write(v)
def gstreamer_pipeline (capture_width=3280, capture_height=2464, display_width=820, display_height=616, framerate=21, flip_method=0) :   
    return ('nvarguscamerasrc ! ' 
    'video/x-raw(memory:NVMM), '
    'width=(int)%d, height=(int)%d, '
    'format=(string)NV12, framerate=(fraction)%d/1 ! '
    'nvvidconv flip-method=%d ! '
    'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
    'videoconvert ! '
    'video/x-raw, format=(string)BGR ! appsink'  % (capture_width,capture_height,framerate,flip_method,display_width,display_height))

	

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(-1)
	#camera = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

#Creating a Pandas DataFrame To Store Data Point
Data_Features = ['x', 'y', 'time']
Data_Points = pd.DataFrame(data = None, columns = Data_Features , dtype = float)

#Reading the time in the begining of the video.
start = time.time()

# keep looping
while True:
	#if (arduinoSerialData.inWaiting() > 0): 
	#	myData = arduinoSerialData.readline()
	#	print(mydata)


	# grab the current frame
	(grabbed, frame) = camera.read()
	
	#Reading The Current Time
	current_time = time.time() - start

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=800)
	#blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# Draw circle target
	(h,w) = frame.shape[:2]
	cv2.circle(frame, (w//2,h//2), 50, (255,255,255),0)
	cv2.rectangle(frame, (350,250), (450,350),(255,255,255), 0)
	font = cv2.FONT_HERSHEY_SIMPLEX


	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		
		#print("The center of the circle is: ",center)

		# only proceed if the radius meets a minimum size
		if (radius < 300) & (radius > 10 ): 
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

			print("X is:", x)
			print("Y is: ", y)
			#moveCamera(x,y)
			#if (x < 400):
			#	GPIO.output(IN1, GPIO.HIGH)
			#Object if left so move left
			if (x < 400):
				#if (x < 350):
					#GPIO.output(IN1, GPIO.HIGH)
				#GPIO.output(IN2, GPIO.LOW)
				angleX += 3
				if (angleX > 170):
					angleX = 170
				moveServoX(angleX)
			#GPIO.output(IN2, GPIO.LOW)

			# Object is right so move right
			if (x > 400):
				#GPIO.output(IN2, GPIO.HIGH)
				#GPIO.output(IN1, GPIO.LOW)
				angleX -= 3
				if (angleX < 30):
					angleX = 30
				moveServoX(angleX)
			# Object is down so move down
			if (y < 295):
				angleY -= 3
				if (angleY < 70):
					angleY = 70
				moveServoY(angleY)
			# Object is up so move down
			if (y > 305):
				angleY += 3
				if (angleY > 150):
					angleY = 150
				moveServoY(angleY)

			#print("Angle X is: ", angleX)
			#print("Angle Y is: ", angleY)
			#if(radius < 50):
			#	print("Object too far!")
			
			# Move based on centered detection
			if (x > 345 and x < 455 and y > 245 and y < 355 and radius < 50):
				cv2.putText(frame, 'Locked', (370,300), font, .5, (255,255,255), 1, cv2.LINE_AA)
				cv2.circle(frame, (w//2,h//2), 50, (0,3,255),1)
				cv2.rectangle(frame, (350,250), (450,350),(0,3,255), 1)
				GPIO.output(IN1, GPIO.HIGH)
				GPIO.output(IN2, GPIO.HIGH)
				#time.sleep(2)
			elif (x < 100):
				GPIO.output(IN1, GPIO.HIGH)
				GPIO.output(IN2, GPIO.LOW)
			elif (x > 500):
				GPIO.output(IN2, GPIO.HIGH)
				GPIO.output(IN1, GPIO.LOW)


			else:
				GPIO.output(IN1, GPIO.LOW)
				GPIO.output(IN2, GPIO.LOW)


           
            
			
			#Save The Data Points
			Data_Points.loc[Data_Points.size/3] = [x , y, current_time]
    
	# update the points queue
	pts.appendleft(center)


	
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

#'h' is the focal length of the camera
#'X0' is the correction term of shifting of x-axis
#'Y0' is the correction term ofshifting of y-axis
#'time0' is the correction term for correction of starting of time
h = 0.2
X0 = -3
Y0 = 20
time0 = 0
theta0 = 0.3

#Applying the correction terms to obtain actual experimental data
Data_Points['x'] = Data_Points['x']- X0
Data_Points['y'] = Data_Points['y'] - Y0
Data_Points['time'] = Data_Points['time'] - time0

#Calulataion of theta value
Data_Points['theta'] = 2 * np.arctan(Data_Points['y']*0.0000762/h)#the factor correspons to pixel length in real life
Data_Points['theta'] = Data_Points['theta'] - theta0

#Creating the 'Theta' vs 'Time' plot
plt.plot(Data_Points['theta'], Data_Points['time'])
plt.xlabel('Theta')
plt.ylabel('Time')

#Export The Data Points As cvs File and plot
Data_Points.to_csv('Data_Set.csv', sep=",")
plt.savefig('Time_vs_Theta_Graph.svg', transparent= True)

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()



