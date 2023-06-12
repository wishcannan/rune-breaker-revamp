#用来对新版本的图进行测试用的demo版本 对照功能 preprocess.py
import argparse
import os
import re
import uuid
import sys

sys.path.insert(0, os.path.abspath('.'))

import colorful as cf
import cv2
import numpy as np
import pandas as pd
from skimage import morphology
import time

import common



def main():
    global direction_label
    labeled_imgs = common.get_files(common.LABELED_DIR)
    path, filename = labeled_imgs[1]
    # for path, filename in labeled_imgs:
    display = cv2.imread(path)
    height, width, _ = display.shape
    print(height,width,filename)
    img = display[120:height//2, width//4:3*width//4]
    #简单的去点噪声
    img1 = cv2.GaussianBlur(img, (3, 3), 0)
    image = canny(filter_color(img1))
    #转灰度
    image_GRAY= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #二值化
    img_binary = cv2.adaptiveThreshold(image_GRAY, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, -1)
    #寻找轮廓
    contours, _ = cv2.findContours(
        img_binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    #按照面积将所有轮廓逆序排序
    contours2 = sorted(contours, key=lambda a: cv2.contourArea(a), reverse=True)
    print(len(contours2),cf.skyBlue('contours2')) 
    i = 0
    alist = []
    img3 = img
    for c in contours2: 
        hull = cv2.convexHull(c)                
        # print(len(hull),i)
        if(len(hull) > 9):
            # cv2.polylines(img, [hull], True, (0, 255, 0), 2)
            # x,y,w,h=cv2.boundingRect(c)         
            # cv2.rectangle(img3,(x,y),(x+w,y+h),(0,255,0),2)
            (cx, cy), r = cv2.minEnclosingCircle(hull)
            center = (int(cx),int(cy))
            # print(center,x,y,w,h)
            radius  = int(r)
            # s1 = '{},{}'.format(center[0],center[1])
            # print(s1)
            # cv2.circle(img3, center , radius, (0,0,255),1)
            # cv2.putText(img3,s1,center, cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            # cv2.imshow('circle',img3)
            # cv2.waitKey()
            # cv2.destroyAllWindows()
            # print(center)      
            img4 = get_reference_arrows(center,img)
            sava_arrows(img4,filename,i)
        i += 1 
        


        
    # cv2.imshow('frame', canny(filter_color(image)))
    # img2=cv2.drawContours(img,contours,-1,(0,255,0),1)
    

def canny(image):
    """
    Performs Canny edge detection on IMAGE.
    对图像执行Canny边缘检测。
    :param image:   The input image as a Numpy array.
    :return:        The edges in IMAGE.
    """

    image = cv2.Canny(image, 200, 300)
    colored = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # colored = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    return colored
def filter_color(image):
    """
    Filters out all colors not between orange and green on the HSV scale, which
    eliminates some noise around the arrows.
    过滤掉 HSV 等级上不介于橙色和绿色之间的所有颜色，即消除箭头周围的一些噪音。
    :param image:   The input image.
    :return:        The color-filtered image.
    """

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (1, 100, 100), (75, 255, 255))

    # Mask the image
    color_mask = mask > 0
    #写了 一张原图大小的 0 数组
    arrows = np.zeros_like(image, np.uint8)
    arrows[color_mask] = image[color_mask]
    return arrows

def get_reference_arrows(center,img):
    '''
    实现一个根据圆心 裁取正方形的效果
    img 是二值图
    center是圆心
    '''
    r = 30
    # xmin,xmax,ymin,ymax = center[0] -r +320,center[0] + r + 320,center[1]- r + 120,center[1] + r + 120
    xmin,xmax,ymin,ymax = center[0] -r,center[0] + r,center[1]- r,center[1] + r
    arrow = img[ymin:ymax,xmin:xmax]
    return arrow

def sava_arrows(img,n,i):
    '''
    保存图片用的
    '''
    arrow_path = common.EX_DIR + n + str(i)
    cv2.imwrite(arrow_path + ".png", img)

def on_press(event):
    global direction_label







    

if __name__ == "__main__":
    main()