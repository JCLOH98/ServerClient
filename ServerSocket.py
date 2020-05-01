import cv2 as cv
import numpy as np
'''
import flask

from flask import Flask
from flask import Response
from flask import  render_template
'''
import socket
import pickle
import struct
'''
frame = None;
mirrorframe = None;
app = Flask(__name__);
'''

HOST = "localhost"
PORT=5000

#server socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
print("Socket created");
s.bind((HOST,PORT));
print("Socket binded");
s.listen(10);
print("Socket listening");
con, add = s.accept();
print(con);
print(add);

data = b"";
#unsigned long size (4 bytes)
payloadsize = struct.calcsize("L");

condi = True;

while condi:
    #Retrieve everything
    while len(data)<payloadsize:
        #data += con.recv(2**20);
        try:
            data += con.recv(2**20);
        except:
            #print("1")
            condi = False;
            break;

    #find the packed message size, which is the front part of the real data
    #and then find the length of data into data
    if(len(data)<payloadsize):
        continue;
    else:
        packed_msg_size = data[:payloadsize];
        data = data[payloadsize:];
        msg_size = struct.unpack("L",packed_msg_size)[0];

    #make sure all data are received
    while len(data) < msg_size:
        #data += con.recv(2**20);
        try:
            data += con.recv(2**20);
        except:
            #print("2")
            condi = False;
            break;
        
    if(len(data)<msg_size):
        continue;
    else:
        frame_data = data[:msg_size];    
        data = data[msg_size:];

        frame=pickle.loads(frame_data);
        cv.imshow("frame",frame);
        key = cv.waitKey(1);
        if key==ord("q"):
            break;

cv.destroyAllWindows();
s.close();
    

