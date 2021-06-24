import socket
import json
import msgpack
import tkinter
import threading
from PIL import Image,ImageTk


import src.image_lib as ImageLib



def recv_data():
    # 接受全部文件
    while True:
        msg = None
        try:
            # 先接受包大小
            msg = s.recv(4)
            # 字节转int
            msg_len = int.from_bytes(msg, byteorder='big')
            print("msg_len:%s"%(msg_len))
            msg = s.recv(msg_len)
            # json数据太大
            # msg_data = json.loads(msg.decode('utf-8'))
            msg_data = msgpack.unpackb(msg)
            # 转图片
            img = ImageLib.list_to_image(msg_data)
            img=ImageTk.PhotoImage(img)
            print(img)
            label.config(image=img)
            label.pack()
        except Exception as err:
            print(err)
            print("err")




# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = "127.0.0.1"
port = 12000
s.connect((host, port))
# s.setblocking(False)

root = tkinter.Tk()
label = tkinter.Label(root)
# 线程更新
t1 = threading.Thread(target=recv_data, args=())
t1.start()
root.mainloop()








