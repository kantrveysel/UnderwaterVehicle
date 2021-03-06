import pickle
import socket
import struct
import cv2
import numpy as np

HOST = '192.168.1.2'  # 43.221
PORT = 8089
font = cv2.FONT_HERSHEY_SIMPLEX

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()

data = b''  ### CHANGED
payload_size = struct.calcsize("L")  ### CHANGED

text = ""
circlePos = (0,0,0)
a = [[0,0],[0,0],[0,0]]

while True:

    # Retrieve message size
    while len(data) < payload_size:
        data += conn.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]  ### CHANGED

    # Retrieve all data based on message size
    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data)
    # frame = cv2.resize(frame, (640,480), interpolation = cv2.INTER_LANCZOS4)
    # Display
    img = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Görüntüyü Siyah Beyaz yapar
    # cimg = cv2.cvtColor(cimg,cv2.COLOR_GRAY2BGR)
    cimg = cv2.medianBlur(cimg, 5)  # Median Blur
    # et, cimg = cv2.threshold(cimg, 80, 255, cv2.THRESH_BINARY) # Şekilleri ayırt etmeye yarar görsel, siyahlık, beyaztonu, thresh tipi
    cimg = cv2.adaptiveThreshold(cimg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 205, 3.5)

    try:
        circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1.3, 200,
                                   param1=6, param2=60, minRadius=0,
                                   maxRadius=480)  # img, type, dp, mindist şeklindedir 40lık radius 70cmden 10cmlik gözükür
        circles = np.uint16(np.around(circles))  # Toplanan verileri 16'lık int listesi yapar
        for i in circles[0, :]:
            a[0].append(i[0])  # Çemberin merkezinin X leri
            a[1].append(i[1])  # Çemberin merkezinin Y leri
            a[2].append(i[2])  # Çemberin merkezinin r leri

            if len(a[0]) > 10:  # Liste 10 tane çember aldığı zaman
                a[0] = a[0][1:]  #
                a[1] = a[1][1:]  # İlk çemberi sil
                a[2] = a[2][1:]  #
            std = [np.std(a[0]), np.std(a[1]), np.std(a[2])]  # Standart sapmalarını listeler
            anew = [[], [], []]  # sapan çemberlerin atılmış halini listeler
            means = [np.mean(a[0]), np.mean(a[1]), np.mean(a[2])]  # ortalamaların olduğu liste
            for u in a[0]:  # X lerin listesi içindeki sapan çemberleri atar
                if u < means[0] + std[0] and u > means[0] - std[0]:
                    anew[0].append(u)
            for u in a[1]:
                if u < means[1] + std[1] and u > means[1] - std[1]:
                    anew[1].append(u)
            for u in a[2]:
                if u < means[2] + std[2] and u > means[2] - std[2]:
                    anew[2].append(u)
            # cv2.circle(img, (int(np.mean(anew[0])), int(np.mean(anew[1]))), int(np.mean(anew[2])), (255, 0, 0), 2) # Çemberi çizdir
            circlePos = (int(np.mean(anew[0])), int(np.mean(anew[1])), int(np.mean(anew[2])))  # Çember pozisyonunu döndürür

            #print(30 * 95 / (np.mean(anew[2])))  # 30cm uzaklık -> 95px yarı çap
            print(circlePos)
    except:
        circlePos = (0,0,0)
        pass
    cv2.circle(img,(circlePos[0],circlePos[1]),circlePos[2],0x00ff00)
    cv2.imshow('frame', img)
    k = cv2.waitKey(5)
    if k == 111:
        break