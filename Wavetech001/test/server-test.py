import socket
import Adafruit_PCA9685
from time import sleep
from math import sqrt, fabs
import subprocess as sp

HOST = '192.168.43.88'
PORT = 65432
OSO = 1
OSA = 4
ASA = 5
ASO = 0
DSO = 2
DSA = 3
ftoa = lambda x : int(x*520/180 + 130)

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

def mapp(n,imin,imax,omin,omax):
    return (n-imin)*(omax-omin)/(imax-imin)+omin

def _bar30():
	try:
		return list(map(float, sp.Popen(["python2","bar30.py"], stdout=sp.PIPE).communicate()[0].decode().split("\n")[:-1]))
	except:
		pass

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()
print(addr[0],"CONNECTED")
sl,ss,saat,dso,dsa = (0,0,0,0,0)

while True:
	data = conn.recv(512).decode().split(",")
	print("\033c")
	print(data)
	conn.send(b'123456789')

