                                                 # # # # # # # # # # # #
from socket import AF_INET, socket, SOCK_STREAM  # Networking Library  #
from threading import Thread                     # Threading Library   #
                                                 # # # # # # # # # # # #

# This fuction used to handling connection for incoming clients
def server_incoming_connections():
    while True:                                                              # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
        client_connection, client_address = SERVER.accept()                  # if server socket accept connection                              #
                                                                             # [client_connection] -> contain client socket                    #
                                                                             # [client_address] -> contain client address                      #
        print("%s:%s has connected." % client_address)                       #                                                                 #
        addresses[client_connection] = client_address                        # store in [addresses] list client address in index [connection]  #
        Thread(target=server_client_side, args=(client_connection,)).start() # Creat and start thread for each clients connect to server       #
                                                                             # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# This fuction used to handling a single client connection
                                                            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def server_client_side(client):                             # client -> client socket                                                 #
                                                            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    clients[client] = client                                # store client socket in [clients] list in index client                   #
    while True:                                             #                                                                         #
        msg = client.recv(BUF_SIZ)                          # msg -> contain recieved data from this client                           #
        if msg != bytes("{quit}", "utf8"):                  # if data recieved from client it {quit} it's mean client will close      #
            broadcast(msg,client)                           # if not send message and client socket to [broadcast] to send to clients #
        else:                                               # else client send {quit} and it will close                               #
            client.close()                                  # close connection between client and server                              #
            del clients[client]                             # remove this client socket from list [clients]                           #
            break                                           # break it's mean this client thread func end                             #
                                                            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# This fuction used to Broadcasts a message to all the clients except client call this function
def broadcast(data,client): # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    for sock in clients:    # loop in list [clients] , current element stored in sock   #
        if sock!=client:    # to handle data didn't sent to client that send this data  # 
            sock.send(data) # send data to all clients in list [clients] except me      #
                            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


                     # # # # # # # # # # # # # # # # # # # # # # # # # # #        
clients = {}         # clients -> clients list                           #
addresses = {}       # addresses -> client addresses list                #
HOST = '127.0.0.1'	 # HOST -> host ip                                   #
PORT = 33000         # PORT -> port number                               #
BUF_SIZ = 1024       # BUF_SIZ -> sending or recieving rate              #
ADDR = (HOST, PORT)  # ADDR -> create addresss tuble using [HOST],[PORT] #
                     # # # # # # # # # # # # # # # # # # # # # # # # # # #
     

                                      # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #                   
SERVER = socket(AF_INET, SOCK_STREAM) # SERVER -> contain server socket wich created by [socket] , TCP connection #
SERVER.bind(ADDR)                     # bind server address using [ADDR] tuble                                    #
                                      # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


if __name__ == "__main__":
                                                               # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    SERVER.listen(5)                                           # Enable a server to accept connections                             #         
    print("Waiting for connection...")                         #                                                                   #
    ACCEPT_THREAD = Thread(target=server_incoming_connections) # ACCEPT_THREAD -> create thread dor [server_incoming_connections]  #
    ACCEPT_THREAD.start()                                      # start Thread                                                      #
    ACCEPT_THREAD.join()                                       # join Thread                                                       #
                                                               # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    SERVER.close()