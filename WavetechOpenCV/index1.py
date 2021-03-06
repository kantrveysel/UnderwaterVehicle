import cv2
import numpy as np
from math import fabs,exp,log
from time import time

from matplotlib import pyplot as pyp
k = []
l = []
m = []
x0,y0,r0 = (0,0,0)
#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640,480))

cam = cv2.VideoCapture('FRAME.mp4')
_,img = cam.read()
boy,en,_ = img.shape
ccc=0
kk=0
while True:
	t = time()
	#kk+=0.008
	#print(kk)
	#print(int(t))
	_,img = cam.read()
	#img = img[60:]
	img = cv2.resize(img,(0,0),fx=0.25,fy=0.25)
	cimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	_,cimg = cv2.threshold(cimg,100,255,cv2.THRESH_BINARY)
	#cimg = cv2.adaptiveThreshold(cimg, 355, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    #                                      cv2.THRESH_BINARY, 655, 21)
	cimg=cv2.blur(cimg,(5,5))
	#contours, _ = cv2.findContours(cimg,
    #        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			
	#mask = np.zeros(img.shape, np.uint8)
	#for i, contour in enumerate(contours):
#		c_area = cv2.contourArea(contour)
#		if c_area > 10000:
#			cv2.drawContours(mask, contours, i, (255,255,255), -1)
			#print(c_area)
	#img = cv2.bitwise_and(img,mask)
#	cimg = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
	
	if True:
		circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1.1, 800,
                                   param1=13, param2=30, minRadius=10,
                                   maxRadius=300)
		if circles is not None:
			ccc +=5
			if ccc>100:
				ccc=55
			if ccc>50 and len(circles)==1:
				circles = np.round(circles[0, :]).astype("int")
				#out.write(img) # VİDEO YAZ
				for (x, y, r) in circles:
					if x==0:
						continue
					k.append(x)
					l.append(t)
					#if np.array(k).std() < x-x0:
					#	continue
					xx = int(np.array(k).mean())
					#cv2.circle(img, (x, y), r, (0, 255, 0), 4)
					cv2.circle(img, (xx, y0), r0, (0, 0, 255), 4)
					cv2.rectangle(img, (xx - 5, y - 5), (xx + 5, y + 5), (0, 128, 255), -1)
					
					az  = log((en/2)/((x+0.1)/2),50)*fabs(x-en/2)/(en/2)
					azz = log((en/2)/((en-x)/2),50)*fabs(x-en/2)/(en/2)
					osa = (1-azz*(x>en/2))*(r/300)
					oso = (1-az*(x<en/2))*(r/300)
					if len(k)>kk:
						k = k[1:]
					#print(k,np.array(k).mean())
					#print("SAĞ"*(x>en/2) + "SOL"*(x<en/2),r)
					#print(len(circles),(x-x0,y-y0,r-r0), oso,osa,np.array(k).std())
					x0,y0,r0 = (x,y,r)
					
					m.append(xx>en/2 - xx<en/2)
					cv2.line(img, (x,int(img.shape[0]/2)), (int(en/2),int(img.shape[0]/2)), (0, 255, 0), thickness=3, lineType=8)
		if ccc>0:
			ccc-=1
	#print(ccc)
	cv2.imshow("FRAME",img)
	if cv2.waitKey(1) == 27:# ESC
		break

#out.release() ##YAZICIYI SERBEST BIRAK
cam.release()
pyp.plot(l[:len(m)],m)
#pyp.show()