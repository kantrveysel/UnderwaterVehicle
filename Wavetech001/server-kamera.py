import pickle
import socket
import struct
import cv2

HOST = '192.168.1.2' # 43.221
PORT = 8089
font = cv2.FONT_HERSHEY_SIMPLEX 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()

data = b'' ### CHANGED
payload_size = struct.calcsize("L") ### CHANGED

text = ""

while True:

    # Retrieve message size
    while len(data) < payload_size:
        data += conn.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGED

    # Retrieve all data based on message size
    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]
    try:
        with open("basinc.txt","r") as dosya:
            text = dosya.read()
    except:
        pass
		
    frame = pickle.loads(frame_data)
    #frame = cv2.resize(frame, (640,480), interpolation = cv2.INTER_LANCZOS4)
    # Display
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    #cv2.putText(frame, text, (50, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
    cv2.imshow('frame', frame)
    k = cv2.waitKey(5)
    if k == 111:
        break
	