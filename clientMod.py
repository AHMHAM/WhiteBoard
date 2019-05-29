                                                   # # # # # # # # # # # # # # # # # # # # # # # # # # #                                                           
from socket import AF_INET, socket, SOCK_STREAM    # Networking Library                                #
import pickle                                      # Library That Convert List to bytes and vice versa #
import time                                        # time Library For Delay                            #
import os, sys                                     # Os and sys Library                                #                                   
import queue                                       # Queue Library                                     #
                                                   # # # # # # # # # # # # # # # # # # # # # # # # # # #

# This fuction used to recieve data from server [Function called by function (receive)] 
                                                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #        
def recieveData_clientSpeak(client_socket,BUF_SIZ): # client_socket -> client socket which connect to server                  #
                                                    # BUF_SIZ -> rate which we used for recieving data from server            # 
                                                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    string=b''                                      # string -> accumulate on it recvd_data data [all data as bytes]          #
    i=0                                             # i -> counter used to check if server send empty data                    #
    while True:                                     # loop until recieve all chunks of data or [time out]                     #
        recvd_data =client_socket.recv(BUF_SIZ)     # recieve data from server with [BUF_SIZ] and store it in [recvd_data]    # 
        string+=recvd_data                          # recvd_data -> contain current chunk of data and accumulate on string    # 
        if string[-1:] == b'.':                     # to detect if i recieve all chunks [list] from server cuz data end>b'.'  #
            break                                   # break if we reciev all chunks of data                                   #
        elif len(string)==0 and i>=50:              # detect if server send empty data give it 50 time and break [time out]   # 
            break                                   # break if [time out]                                                     #
        i+=1                                        #                                                                         #
    return string                                   # return [string] wich contain all chunks of data [list]                  #
                                                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# This fuction used to recieve data from server by calling [fuction (recieveData_clientSpeak)] and store it in queue
                                                                  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         
def receive(client_socket,BUF_SIZ,data_queue):                    # client_socket -> client socket which connect to server passed by [App]  #
                                                                  # BUF_SIZ -> rate which we used for recieving data from server            # 
                                                                  # data_queue -> queue wich store recieved data in it                      #
                                                                  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    while True:                                                   # loop until client close                                                 #
        try:                                                      # to catch exception if client close we use try and catch                 #
            data = recieveData_clientSpeak(client_socket,BUF_SIZ) # data -> store on it returned data from [recieveData_clientSpeak]        #
            if data[0:1] == b'\x80' and data[-1:] == b'.':        # to detect if it data [list] to store in queue or normal message         #
                data=pickle.loads(data)                           # convert data [list] from bytes to list again                            #
                data_queue.put(data)                              # store data [list] in queue [enqueue] using [.put]                       #
        except OSError:                                           # Possibly client has left                                                #
            break                                                 # break if client has left                                                #
                                                                  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# This fuction used to send data to server [Function called by function (sendData_ClientSpeak)] 
                                 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def send(message,client_socket): # message -> data [list] as bytes to send it to server passed by [sendData_ClientSpeak]   #               
                                 # client_socket -> client socket which connect to server passed by [sendData_ClientSpeak] #
                                 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    client_socket.send(message)  # send data [list] to server using [.send]                                                #
                                 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# This fuction used to convert data to bytes and pass it to [send]
                                              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #    
def sendData_ClientSpeak(client_socket,data): # client_socket -> client socket which connect to server passed by [sendData_ClientSpeak] #
                                              # data -> will be convert it to bytes and send it                                         #            
                                              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    message=pickle.dumps(data)                # convert [data] to bytes using [.dumps] and store it into [message]                      #
    send(message,client_socket)               # send [message],[client_socket] to function [send] to send data to server                #
                                              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #       
