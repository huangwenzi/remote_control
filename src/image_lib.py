import tkinter as tk
import pyautogui
from PIL import ImageGrab
from PIL import Image
import numpy as np
import time
import math


import src.cfg as Cfg


# 获取显示器大小
def get_monitor_size():
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    return width,height

# 获取屏幕截图列表
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
        
    # time_1 = time.time()
    # # 这里获得的是np数组 注意dtype
    # array = np.asarray(img, dtype=np.uint8)
    # # np数组转list
    # data_list = array.tolist()
    # time_2 = time.time()
    
    # 尝试新算法
    pixels = img.getdata()
    data_list_1 = list(pixels)
    data_list_2 = data_to_two_arr(data_list_1, pixels.size[0])
    # time_3 = time.time()
    # print(time_2 - time_1, time_3 - time_2)
    
    # img.save('image/as_1.png')
    return data_list_2

# 像素数组转二维
# data ： 像素数据
# row_max ： row数
# ps : 
def data_to_two_arr(data, row_max):
    two_data = []
    data_len = len(data)
    col_max = data_len//row_max
    for idx in range(0, col_max):
        two_data.append(data[idx*row_max : idx*row_max + row_max])
    return two_data

# 获取图片地址转列表
def get_list_by_path(path):
    img = Image.open(path)
    # 这里获得的是np数组 注意dtype
    array = np.asarray(img, dtype=np.uint8)
    # np数组转list
    list = array.tolist()
    # img.save('image/as_1.png')
    return list

# 列表转图片
def list_to_image(array):
    # 转np数组 注意dtype
    array = np.array(array, dtype="uint8")
    # np数组转图片
    image = Image.fromarray(array) 
    return image

# 获取变化的区域列表
def get_change_list(old_img_list, img_list):
    block_size = Cfg.block_size
    ret_list = []
    # 高度，宽度
    max_x = len(img_list)
    max_y = len(img_list[0])
    if len(old_img_list) == 0:
        return [[0, 0, len(img_list), len(img_list[0])]]
    
    x_block_num = math.ceil(max_x/block_size)
    y_block_num = math.ceil(max_y/block_size)
    # 遍历y图片块
    for y_block in range(y_block_num):
        # 遍历x图片块
        for x_block in range(x_block_num):
            # 起始点
            begin_pos = [x_block*block_size, y_block*block_size]
            end_pos = [(x_block+1)*block_size, (y_block+1)*block_size]
            ret, ret_range = list_is_identical(old_img_list, img_list, begin_pos, end_pos)
            if not ret:
                ret_list.append(ret_range)
    return ret_list

# 获取开始点列表
def get_begin_pos_list():
    block_size = Cfg.block_size
    img_range = Cfg.img_range
    ret_list = []
    # 高度，宽度
    max_x = img_range[2] - img_range[0]
    max_y = img_range[3] - img_range[1]
    
    x_block_num = math.ceil(max_x/block_size)
    y_block_num = math.ceil(max_y/block_size)
    # 遍历y图片块
    for y_block in range(y_block_num):
        # 遍历x图片块
        for x_block in range(x_block_num):
            # 起始点
            begin_pos = [x_block*block_size, y_block*block_size]
            ret_list.append(begin_pos)
    return ret_list

# 两个列表，开始到结束的位置是否相同
def list_is_identical(list_a, list_b, begin_pos, end_pos):
    # 根据list修改end_pos
    a_max_x = len(list_a)
    a_max_y = len(list_a[0])
    b_max_x = len(list_b)
    b_max_y = len(list_b[0])
    min_x = min([a_max_x, b_max_x, end_pos[0]])
    min_y = min([a_max_y, b_max_y, end_pos[1]])
    # 遍历
    for pos_x in range(begin_pos[0], min_x):
        for pos_y in range(begin_pos[1], min_y):
            a_pos = list_a[pos_x][pos_y]
            b_pos = list_b[pos_x][pos_y]
            if a_pos != b_pos:
                return False,begin_pos + [min_x, min_y]
    return True,[]

# 根据范围获取图片列表
def get_list_buy_range(img_list, img_range):
    # 数组才能直接转
    # return img_list[img_range[0]:img_range[2], img_range[1]:img_range[3]]
    # 提取列表的数据
    ret_list = []
    for x_pos in range(img_range[0], img_range[2]):
        y_list = []
        for y_pos in range(img_range[1], img_range[3]):
            y_list.append(img_list[x_pos][y_pos])
        ret_list.append(y_list)
    return ret_list


# old_img_list = get_list_by_path('image/as_1.png')
# ret_list = get_list_buy_range(old_img_list, [0,0,100,200])
# img = list_to_image(ret_list)
# img.save('image/as_11.png')


# old_img_list = get_list_by_path('image/as_1.png')
# img_list = get_list_by_path('image/as_2.png')
# ret_list = get_change_list(old_img_list, img_list)
# send_list = []
# for list_range in ret_list:
#     ret_range_list = get_list_buy_range(img_list, list_range)
#     send_list.append([list_range, ret_range_list])


# list = image_to_list(get_screenshot())
# img = list_to_image(list)
# img.save('image/as_1.png')

# begin = time.time()
# end = time.time()
# print(end - begin)

