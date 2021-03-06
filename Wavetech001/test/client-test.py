from math import sin, cos, radians, sqrt, fabs, copysign
import pygame as pyp
from time import sleep
import socket
from math import ceil,fabs
from time import sleep

####### SABİTLER ########
HOST = '192.168.43.88' #.2 3
PORT = 65432

pyp.init()
pyp.display.init()
pyp.joystick.Joystick(0).init()
pj = pyp.joystick.Joystick(0)

clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect((HOST,PORT))

def JoyButtonOku(a):
    pyp.event.pump()
    return str(bool(pj.get_button(a)))

def JoyAxisOku(a):
    pyp.event.pump()
    return str(ceil(pj.get_axis(a)*100)/100)
	
while True:
	#print(JoyAxisOku(0), JoyButtonOku(0))
	data = str(",".join([JoyAxisOku(i) for i in range(4)])+","+str(",".join([JoyButtonOku(i) for i in range(18)]))).encode()
	try:
		clientsocket.sendall(data)
		#print(data)
		print(clientsocket.recv(32))
	except:
		break
	sleep(0.1)

