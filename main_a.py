import socket
import json
import msgpack
import tkinter
import threading
from PIL import Image,ImageTk


import src.image_lib as ImageLib
import src.cfg as Cfg



def recv_data():
    # 初始化界面
    
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
            for item in msg_data:
                pos = item[0]
                img_data = item[1]
                # 转图片
                img = ImageLib.list_to_image(img_data)
                img=ImageTk.PhotoImage(img)
                list_key = "%d_%d"%(pos[1],pos[0])
                label_list[list_key].config(image=img)
                # 下面这个很关键，少了只会显示一个图片块
                label_list[list_key].image=img
            # root.update()
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
root.geometry("%dx%d"%(Cfg.img_range[2]-Cfg.img_range[0], Cfg.img_range[3]-Cfg.img_range[1]))
# label_list
label_list = {}
pos_list = ImageLib.get_begin_pos_list()
for pos in pos_list:
    # 边框为0
    tmp_label = tkinter.Label(root, text="%s"%(pos), borderwidth = 0)
    tmp_label.place(x = pos[0], y = pos[1])
    list_key = "%d_%d"%(pos[0],pos[1])
    label_list[list_key] = tmp_label
# 线程更新
t1 = threading.Thread(target=recv_data, args=())
t1.start()
root.mainloop()








