# -*- coding:utf-8 -*-
import os
import can
import time
import sys

os.system('sudo ip link set can0 type can bitrate 250000') # change the value of baud-rate
                                                           # if your sensor has another value                    
os.system('sudo ifconfig can0 up')

#Construct and open a CAN bus instance of the specified type.
can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')# socketcan_native

#msg = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5, 6, 7], extended_id=False)
'''
Format of msg: class can.Message(timestamp=0.0, arbitration_id=0, is_extended_id=None,
is_remote_frame=False, is_error_frame=False, channel=None, dlc=None, data=None, is_fd=False,
bitrate_switch=False, error_state_indicator=False, extended_id=None, check=False)
'''
# Function to read data from LiDAR
def read_data():
    while True:
        msg = can0.recv(10.0) # receive data with timeout of 10seconds
        #************************************************
        if msg is None:
            print('[INFO] Timeout occurred, no message.')
            print('[INFO] CAN bus is downed')
            os.system('sudo ifconfig can0 down')
        #************************************************
        #print("Message contents: ")
        #print(msg)
        h_beat = msg.data[0]
        version = msg.data[1] + msg.data[2]#*256
        print("Time stamp:"+str(msg.timestamp))
        print("LiDAR id:"+str(hex(msg.arbitration_id)))
        print("Size of data-packet in bytes:"+str(msg.dlc))
        print("Heart beat packet:"+ str(h_beat))
        print("Heart beat binary:"+ str(bin(h_beat)))
        print("Version:" + str(version)+ "\n")
        time.sleep(3)




if __name__ == "__main__":
    try:    
        print ("[INFO] Python code for CAN communication")
        print("[INFO] You will continuously receive data, press Ctrl + C to exit")
        print("[INFO] This code works with Python2 and Python3")
        if (sys.version_info[0]) == 2:
            print("Python version is:"+ str(sys.version))
        if (sys.version_info[0]) == 3:
            print("Python version is:"+ str(sys.version))    
        time.sleep(5)
        read_data()
    except KeyboardInterrupt(): # ctrl + c in terminal.
        print("program interrupted by the user")
        print('[INFO] CAN bus is downed')
        os.system('sudo ifconfig can0 down')