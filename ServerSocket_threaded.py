import cv2 as cv
import numpy as np
import socket
import pickle
import struct

import threading
from threading import Thread

HOST = "localhost"
PORT=5000

#server socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
print("Socket created");
s.bind((HOST,PORT));
print("Socket binded");
s.listen(10);
print("Socket listening");

def receive(con,add):
    data = b"";
    #unsigned long size (4 bytes)
    payloadsize = struct.calcsize("L");

    condi = True;
    prev_data = 0;
    while condi:
        #Retrieve everything
        while len(data)<payloadsize:
            try:
                prev_data = data;
                data += con.recv(2**20);
                if (prev_data == data):
                    condi = False;
                    break;
            except:
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
            try:
                prev_data = data;
                data += con.recv(2**20);
                if (prev_data == data):
                    condi = False;
                    break;
            except:
                condi = False;
                break;
           
        if(len(data)<msg_size):
            continue;
        else:
            frame_data = data[:msg_size];    
            data = data[msg_size:];

            frame=pickle.loads(frame_data);
            cv.imshow(str(add[1]),frame);
            key = cv.waitKey(1);
            if key==ord("q") or cv.getWindowProperty(str(add[1]),cv.WND_PROP_VISIBLE) < 1:
                condi = False;
                con.close();
                break;
            
def main():
    while True:
        con, add = s.accept();
        print(add);
        t = Thread(target=receive,args=(con,add));
        t.daemon = True;
        t.start();
        '''
        #Retrieve everything
        while len(data)<payloadsize:
            try:
                data += con.recv(2**20);
            except:
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
            try:
                data += con.recv(2**20);
            except:
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
        '''    
main()
cv.destroyAllWindows();
s.close();
    

