import socket
import Adafruit_PCA9685
from time import sleep
from math import sqrt, fabs
import subprocess as sp

HOST = '192.168.1.2' # 43.88
PORT = 65432
OSO = 1
OSA = 4
ASA = 5
ASO = 0
DSO = 2
DSA = 3
servo = 7
aci = 80
ftoa = lambda x : int(x*520/180 + 130)
fservo = lambda x: int(x*525/180+110)

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
	#print(data)
	try:
		sl = float(data[2])
		ss = -float(data[1])
		saat = -float(data[0])/10
		dso = (-float(data[3]))*((sl+ss)==0.0)
		dsa = dso
	except:
		pass
	osa = (ss*sqrt(2) + 2*sl/sqrt(2)) / 1.4142135623730951 + saat/sqrt(2)
	asa = (sl-ss)/sqrt(2) / 0.7071067811865475 - saat/sqrt(2)
	oso = -asa - 2*saat/sqrt(2)
	aso = -osa + 2*saat/sqrt(2)
	k = 1/(max(fabs(oso),fabs(osa),fabs(aso),fabs(asa))+1/100000)
	k = (k>1)*1 + k*(k<=1)
	signsl = (fabs(sl)/(sl+0.000001) == 0) + (fabs(sl)/(sl+0.000001) != 0)*fabs(sl)/(sl+0.000001)
	signsl2 = (fabs(sl)/(sl+0.000001) == 0)*(-1) + (fabs(sl)/(sl+0.000001) != 0)*fabs(sl)/(sl+0.000001)
	print("osa",osa,"asa",asa,"oso",oso,"aso",aso)
	if signsl>0:
		osa = k*osa*(-signsl2) #- saat
		asa = k*asa*(-signsl2) #+ saat
		oso = k*oso*signsl #+ saat
		aso = k*aso*signsl #- saat
	else:
		osa = k*osa*(signsl2) #- saat
		asa = k*asa*(signsl2) #+ saat
		oso = k*oso*(-signsl) #+ saat
		aso = k*aso*(-signsl) #- saat
	print("OSA",osa,"ASA",asa,"OSO",oso,"ASO",aso,"ss",ss,"sl",sl,"signsl",signsl,"signsl2",signsl2)
	if data[13] == "True" and aci > 20:
		aci -=10
	if data[12] == "True" and aci < 140:
		aci +=10
	print(aci, data[13], data[12])
	pwm.set_pwm(OSO, 0, ftoa(mapp(oso,0,-1,90,30)*(oso<0) + mapp(oso,0,1,96,150)*(oso>0) + (oso == 0)*94))
	pwm.set_pwm(OSA, 0, ftoa(mapp(osa,0,-1,90,30)*(osa<0) + mapp(osa,0,1,96,150)*(osa>0) + (osa == 0)*94))
	pwm.set_pwm(ASA, 0, ftoa(mapp(asa,0,-1,90,30)*(asa<0) + mapp(asa,0,1,96,150)*(asa>0) + (asa == 0)*94))
	pwm.set_pwm(ASO, 0, ftoa(mapp(aso,0,-1,90,30)*(aso<0) + mapp(aso,0,1,96,150)*(aso>0) + (aso == 0)*94))
	pwm.set_pwm(DSO, 0, ftoa(mapp(dso,0,-1,90,30)*(dso<0) + mapp(dso,0,1,96,150)*(dso>0) + (dso == 0)*94))
	pwm.set_pwm(DSA, 0, ftoa(mapp(dsa,0,-1,90,30)*(dsa<0) + mapp(dsa,0,1,96,150)*(dsa>0) + (dsa == 0)*94))
	pwm.set_pwm(servo, 0, fservo(aci))
	print("OSO", mapp(oso,0,-1,30,90)*(oso<0) + mapp(oso,0,1,96,150)*(oso>0) + (oso == 0)*94)
	print(oso,asa,oso,aso,_bar30())
	conn.send(str("#"+str(_bar30())+"#").encode())
	sleep(0.01)

s.close()



