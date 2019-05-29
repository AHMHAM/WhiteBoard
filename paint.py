from tkinter import *
from tkinter.colorchooser import askcolor
from random import random
import clientMod as client
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import os, sys
import copy
import queue


pixel=[]
send=False


def set_exit_handler(func):
    if os.name == "nt":
        try:
            import win32api
            win32api.SetConsoleCtrlHandler(func, True)
        except ImportError:
            version = ".".join(map(str, sys.version_info[:2]))
            raise Exception("pywin32 not installed for Python " , version)
    else:
        import signal
        signal.signal(signal.SIGTERM, func)
        
class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'green'

    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='brush', command=self.use_brush)
        self.brush_button.grid(row=0, column=1)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.choose_size_button = Scale(self.root, from_=1, to=100, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)

        self.c = Canvas(self.root, bg='black', width=600, height=600)
        self.c.grid(row=1, columnspan=5)

        self.setup()
        update_thread = Thread(target=update,args=(self,))
        send_thread = Thread(target=send,args=(self,))
        send_thread.start()
        update_thread.start()
        
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)


#-------------------------------- clear with ------------------------------------------


    def clear_with(self,point_indxes):  
        print(len(point_indxes))
        try:
            for i in range(0,len(point_indxes)-1):
                self.c.create_line(point_indxes[i][0], point_indxes[i][1], point_indxes[i+1][0], point_indxes[i+1][1],
                                           width=point_indxes[i][3], fill=point_indxes[i][2],
                                           capstyle=ROUND, smooth=TRUE, splinesteps=36)
        except:
            print()
            print(len(point_indxes))
            print("ERROR")
            pass

    def exractData_fromQueue(self,data_queue):
        while data_queue.empty()==False:
            print("hello")
            self.clear_with(copy.deepcopy(data_queue.get()))



    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'black' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        pixel_data=(event.x,event.y,paint_color,self.line_width)
        pixel.append(pixel_data)
        self.old_x = event.x
        self.old_y = event.y


    def reset(self, event):
        global send
        self.old_x, self.old_y = None, None
        send=True

def on_exit(sig, func=None):
    print("exit handler triggered")
    client.send("{quit}".encode(),client_socket)
    client_socket.close()


def sendData(client_socket,data):
    set_exit_handler(on_exit)
    client.sendData_ClientSpeak(client_socket,data)

def update(u):
    print("ajhjasjhd")
    while True:
        u.exractData_fromQueue(data_queue)

def send(u):
    global send
    global pixel
    print("ajhjasjhd")
    while True:
        if(send==True):
            print("haaaaaaaaaaaaaaaaaaaaaaaaaaa : ",len(pixel))
            sendData(client_socket,pixel)
            #time.sleep(1)
            del pixel[0:]
            pixel=[]
            send=False

if __name__ == '__main__':
    data_queue=queue.Queue()
    Host='127.0.0.1'
    PortNO=33000
    BUF_SIZ = 1024
    ADDR = (Host, PortNO)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)
    receive_thread = Thread(target=client.receive,args=(client_socket,BUF_SIZ,data_queue))
    receive_thread.start()
    Paint()
    #Paint()