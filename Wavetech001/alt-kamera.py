import cv2
import numpy as np
import socket
import sys
import pickle
import struct
from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep
from datetime import datetime
import time

camera = PiCamera()
camera.resolution = (1080,566)
#camera.start_recording()
rawCapture = PiRGBArray(camera)

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]

current_milli_time = lambda: int(round(time.time() * 1000))

#cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.3',8089)) # 43.221



while True:
	ntime = current_milli_time()
	rawCapture = PiRGBArray(camera)
	#sleep(0.2)
	camera.capture(rawCapture, format="bgr", use_video_port=True)
	img = rawCapture.array
	#img = cv2.resize(img, (640,480), interpolation = cv2.INTER_LANCZOS4)
	_,img = cv2.imencode(".jpg", img, encode_param)
	data = pickle.dumps(img)
	message_size = struct.pack("L", len(data))
	clientsocket.sendall(message_size + data)
	print("\033c")
	print(current_milli_time() - ntime)
	
