import cv2 as cv
import numpy as np
import socket
import pickle
import struct

#cap = cv.VideoCapture(0, cv.CAP_DSHOW);

#client socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
s.connect(("localhost",5000));

while True:
    #ret, frame = cap.read();
    frame = cv.imread("cam2.jpg");
    #change the frame into byte form
    data = pickle.dumps(frame);
    #pack the unsigned long and size of data in front of the data
    #then add the data behind
    try:
        s.sendall(struct.pack("L", len(data))+data);
    except:
        #print("Stopped Sending Data");
        break;
    #cv.imshow("OriCam",frame);
    key = cv.waitKey(1);
    if key==ord("q"):
        break;
    
#print(struct.pack("L", len(data))+data);
#cap.release();
#cv.destroyAllWindows();
s.shutdown(socket.SHUT_RDWR);
s.close();
