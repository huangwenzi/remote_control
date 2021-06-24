import tkinter
import time
import threading
from PIL import Image,ImageTk




# 更新label
def update_label():
    path = 'image/as_{0}.png'
    idx = 1
    while True:
        path_1 = path.format(idx)
        print(path_1)
        img_open = Image.open(path_1)
        img=ImageTk.PhotoImage(img_open)
        label.config(image=img)
        label.pack()
        if idx == 1:
            idx = 2
        else:
            idx = 1
        time.sleep(1)









root = tkinter.Tk()
label = tkinter.Label(root)
# 线程更新
t1 = threading.Thread(target=update_label, args=())
t1.start()
root.mainloop()

















