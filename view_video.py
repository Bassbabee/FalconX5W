import socket
import binascii
import threading
import cv2
import numpy as np

IP = '192.168.4.153'
UDPPORT1 = 8080
MESSAGE1 = binascii.unhexlify(b'4276')

def stream(x):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sock.sendto(MESSAGE1, (IP, UDPPORT1))
    data_bytes = bytes()
    while True:
        try:
            data = sock.recv(1472)
            data_bytes += data[8:]
            jpg_start = data_bytes.find(b'\xff\xd8')
            jpg_end = data_bytes.find(b'\xff\xd9')
            if jpg_start != -1 and jpg_end != -1:
                if jpg_start > jpg_end:
                    data_bytes = data_bytes[jpg_start:]
                    continue
                image_bytes = data_bytes[jpg_start:jpg_end+5]
                data_bytes = b''
                decoded = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), 1)
                cv2.imshow('KVADRO', decoded)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            break

# x = threading.Thread(target=stream, args=('Trash',))
# x.start()
stream(1)
