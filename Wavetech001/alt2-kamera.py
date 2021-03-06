import cv2
import io
import socket
import struct
import time
import pickle
import zlib
from picamera import PiCamera
from picamera.array import PiRGBArray

camera = PiCamera()
rawCapture =PiRGBArray(camera)

clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.43.221',8089))

img_counter = 0
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
	camera.capture(rawCapture, format="bgr")
	frame = rawCapture.array
	frame = cv2.resize(frame, (640,480), interpolation = cv2.INTER_AREA)
	_,frame = cv2.imencode(".jpg", frame, encode_param)
	data = pickle.dumps(frame, 0)
	size = len(data)
	clientsocket.sendall(struct.pack(">L", size) + data)
	img_counter +=1


