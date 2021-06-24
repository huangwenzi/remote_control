import time
import socket
import select
import threading
import json
import msgpack



import src.image_lib as ImageLib

# 客户端列表
client_list = []

# 监听socket
def listen_client(client_list, ser_socket):
    inputs = [ser_socket,]
    while True:
        time.sleep(1)
        rlist,wlist,eList = select.select(inputs,[],[],0.5)
        # print("inputs:",inputs) # 查看inputs列表变化
        # print("rlist:",rlist) # 查看rlist列表变化
        # print("wlist:",wlist) # 查看rlist列表变化
        # print("eList:",eList) # 查看rlist列表变化
        for r in rlist:
            if r == ser_socket: # 如果r是服务端
                conn,address = r.accept()
                inputs.append(conn) # 把连接的句柄加入inputs列表监听
                client_list.append(conn)
                print (address)
            else:
                # 尝试读取数据
                client_data = None
                try:
                    client_data = r.recv(1024)
                    # 下面可以添加处理
                    
                except :
                    inputs.remove(r)
                    client_list.remove(r)
                    # 直接退出
                    return

# 初始化监听的socket
serversocket = socket.socket() 
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(("127.0.0.1", 12000))
serversocket.listen(5)

# 分线程去监听接入的客户端
t1 = threading.Thread(target=listen_client, args=(client_list, serversocket))
t1.start()


old_img_list = []
# 循环发送截图
while True:
    # 获取截图数组
    # img_list = ImageLib.get_screenshot_list([0,0,300,300])
    img_list = ImageLib.get_screenshot_list()
    # 获取变化的位置
    ImageLib.get_change_list(old_img_list, img_list)
    
    # json数据太大
    # send_str = bytes(json.dumps(img_list), encoding="utf-8")
    # send_str_len = len(send_str)
    packd = msgpack.packb(img_list)
    packd_len = len(packd)
    # print(time.time())
    # print("tmp_client send:%s"%(packd_len))
    # 发送文件
    for tmp_client in list(client_list):
        try:
            # 先发数据大小
            # int转字节
            packd_len_byte = packd_len.to_bytes(4,byteorder='big', signed=False)
            tmp_client.send(packd_len_byte)
            tmp_client.send(packd)
        except Exception as err:
            print("tmp_client send err")
            print(err)
            client_list.remove(tmp_client)
    old_img_list = img_list
    time.sleep(0.05)








