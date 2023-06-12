'''
实现将ex_labeled的数据二值化 并且产生4个不同方向的分身 用来训练 而却按照10 80 10 的比例产生验证集 训练集 测试集

'''

import argparse
import os
import random
import re
import sys
import cv2

sys.path.insert(0, os.path.abspath('.'))

import colorful as cf
import numpy as np
import pandas as pd

import common



CLASSES = ['down', 'left', 'right', 'up']
TRAINING_DIR = './data/' + 'ex_training/'
VALIDATION_DIR = './data/' + 'ex_validation/'
TESTING_DIR = './data/' + 'ex_testing/'

def main():
    create_directories()
    for path,filename in common.get_files('./data/ex_labeled/'):
        img = cv2.imread(path)
        c = aa(img)
        bb(c,filename)


#实现图片二值化
def aa(img):
    image = canny(filter_color(img))
    image_GRAY= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    img_binary = cv2.adaptiveThreshold(image_GRAY, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, -1)
    return img_binary
 
def filter_color(image): 
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (1, 100, 100), (75, 255, 255))

    # Mask the image
    color_mask = mask > 0
    #写了 一张原图大小的 0 数组
    arrows = np.zeros_like(image, np.uint8)
    arrows[color_mask] = image[color_mask]
    return arrows

def canny(image):
    image = cv2.Canny(image, 200, 300)
    colored = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # colored = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    return colored

def arrow_labels(name):
    ddict = {'d':'down','l':'left','u':'up','r':'right'}
    tokens = re.split('_', name)
    arrow_direction = ddict.get(tokens[0])

    return arrow_direction

def bb(img,filename):
    dlist = ['down','left','up','right','down','left','up']
    print(filename)
    arrow_label = arrow_labels(filename)
    num = dlist.index(arrow_label)
    img1 = img
    d = re.split('-',filename)[1]
    for _ in range(4):
        c = dlist[num]
        a = '000{}'.format(num)
        a = a[-4:]
        arrow_path = TRAINING_DIR + c + '/' + c + a + d + '.png'
        cv2.imwrite(arrow_path,img1)
        img1 = cv2.rotate(img1,cv2.ROTATE_90_CLOCKWISE)
        num += 1


def create_directories():
    directories = []
    for d in [TRAINING_DIR, VALIDATION_DIR, TESTING_DIR]:
        for c in CLASSES:
            directories.append(d + c + '/')
    
    for d in directories:
        os.makedirs(d, exist_ok=True)



if __name__ == "__main__":
    main()
    # create_directories()
