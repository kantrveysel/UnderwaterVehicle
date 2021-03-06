from math import sin, cos, radians, sqrt, fabs, copysign
import pygame as pyp
from time import sleep
import socket
from math import ceil,fabs
from time import sleep

# ARDA JOYSTICK
# AXES
# 1 -> İleri - Geri
# 2 -> R' L'
# 0 -> Saat yönü
# 3 -> BAT ÇIK
# 4 -> Dik Sağ dik sol
# BUTTON
# 5 -> R1
# 4 -> L1
# 1 -> B
# 0 -> A

while True:
	try:
		pyp.init()
		pyp.display.init()
		pyp.joystick.Joystick(0).init()
		pj = pyp.joystick.Joystick(0)
		break
	except:
		print("JOYSTICK BEKLENIYOR")

def JoyButtonOku(a):
    pyp.event.pump()
    return str(bool(pj.get_button(a)))

def JoyAxisOku(a):
    pyp.event.pump()
    return str(ceil(pj.get_axis(a)*100)/100)

while True:
	sleep(0.2)
	a = []
	b = []
	for i in range(28):
		try:
			a.append(i)
			b.append(JoyAxisOku(i))
		except:
			pass
	#print(dict(zip(a,b)))
	
	sleep(0.2)
	a = []
	b = []
	for i in range(28):
		try:
			a.append(i)
			b.append(JoyButtonOku(i))
		except:
			pass
	print(dict(zip(a,b)))