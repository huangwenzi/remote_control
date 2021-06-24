import tkinter as tk
import pyautogui
from PIL import ImageGrab
from PIL import Image
import numpy as np
import time
import math


# 图片块大小
block_size = 100


# 获取显示器大小
def get_monitor_size():
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    return width,height

# 获取屏幕截图数组
def get_screenshot_list(region = False):
    # img = ImageGrab.grab() 略慢
    # img = pyautogui.screenshot()
    # img = pyautogui.screenshot(region=[0,0,300,300])
    # 截取屏幕
    img = None
    if not region:
        # 默认全屏
        img = pyautogui.screenshot()
    else:
        img = pyautogui.screenshot(region = region)
    # 这里获得的是np数组 注意dtype
    array = np.asarray(img, dtype=np.uint8)
    # np数组转list
    list = array.tolist()
    # img.save('image/as_1.png')
    return list

# 获取图片地址转数组
def get_list_by_path(path):
    img = Image.open(path)
    # 这里获得的是np数组 注意dtype
    array = np.asarray(img, dtype=np.uint8)
    # np数组转list
    list = array.tolist()
    # img.save('image/as_1.png')
    return list

# 数组转图片
def list_to_image(array):
    # 转np数组 注意dtype
    array = np.array(array, dtype="uint8")
    # np数组转图片
    image = Image.fromarray(array) 
    return image

# 获取变化的区域列表
def get_change_list(old_img_list, img_list):
    # 高度，宽度
    max_x = len(img_list)
    max_y = len(img_list[0])
    if len(old_img_list) == 0:
        return [[0, 0, len(img_list), len(img_list[0])], img_list]
    
    x_block_num = math.ceil(max_x/block_size)
    y_block_num = math.ceil(max_y/block_size)
    # 遍历y图片块
    for y_block in range(y_block_num):
        # 遍历x图片块
        for x_block in range(x_block_num):
            # 起始点
            begin_pos = [x_block*block_size, y_block*block_size]
            end_pos = [(x_block+1)*block_size, (y_block+1)*block_size]

# 两个数组，开始到结束的位置是否相同
def list_is_identical(list_a, list_b, begin_pos, end_pos):
    # 根据list修改end_pos
    a_max_x = len(list_a)
    a_max_y = len(list_a[0])
    b_max_x = len(list_b)
    b_max_y = len(list_b[0])
    min_x = min([a_max_x, b_max_x, end_pos[0]])
    min_y = min([a_max_y, b_max_y, end_pos[1]])
    
    


old_img_list = get_list_by_path('image/as_1.png')
img_list = get_list_by_path('image/as_2.png')
get_change_list(old_img_list, img_list)



# list = image_to_list(get_screenshot())
# img = list_to_image(list)
# img.save('image/as_1.png')

# begin = time.time()
# end = time.time()
# print(end - begin)

