from math import sin, cos, radians, sqrt, fabs, copysign
import pygame as pyp
from time import sleep
import socket
from math import ceil,fabs
from time import sleep

####### SABİTLER ########
HOST = '192.168.43.39' #.43.88
PORT = 65432

pyp.init()
pyp.display.init()
pyp.joystick.Joystick(0).init()
pj = pyp.joystick.Joystick(0)

clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect((HOST,PORT))

def JoyButtonOku(a):
	try:
		pyp.event.pump()
		return str(bool(pj.get_button(a)))
	except:
		return "False"

def JoyAxisOku(a):
    pyp.event.pump()
    return str(ceil(pj.get_axis(a)*100)/100)
	

while True:
	#print(JoyAxisOku(0), JoyButtonOku(0))
	data = str(",".join([JoyAxisOku(i) for i in range(5)])+","+str(",".join([JoyButtonOku(i) for i in range(18)]))).encode() # 5>4
	try:
		clientsocket.sendall(data)
		#print(data)
	except:
		break
	basinc = clientsocket.recv(32)
	print(str(basinc).split(",")[0])
	if len(str(basinc))>8:
		try:
			with open("basinc.txt","w") as dosya:
				dosya.write(str(basinc))
		except:
			pass
	#sleep(0.1)

"""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as baglanti:
    baglanti.connect((HOST,PORT))
    while True:

        JAxises = list(map(str,[JoyAxisOku(0),-JoyAxisOku(1),JoyAxisOku(2),JoyAxisOku(3),JoyAxisOku(4)])) # ileri (+) , geri (-) yapılmıştır
        #sagsol, ilerigeri, vites, dikeksen, bilinmeyenEksen
        JButtons = list(map(str,list(map(int,[JoyButtonOku(i) for i in range(12)]))))

        veri = "/".join(JAxises)+"/ ; /"+"/".join(JButtons)+"/ ; /" + str(JoyHatOku())
        print(veri)
        veriyolla = VeriYolla(baglanti, veri)

        if not veriyolla:
            break
except Exception as e:
    warn("BAĞLANTI YOK - {}".format(d.now()))
"""