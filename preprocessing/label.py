import os
import re
import sys
import time

sys.path.insert(0, os.path.abspath('.'))

import matplotlib.pyplot as plt
import numpy as np

import common

type_label = None
direction_label = ''

plt_text = None

type_dictionary = {'1': 'round', '2': 'wide', '3': 'narrow'}


def main():
    # 可去掉
    common.create_directories()

    print("         Q = ignore image")  # 似乎不是这个效果
    print("         1 = label as round")
    print("         2 = label as wide")
    print("         3 = label as narrow")
    print("ARROW KEYS = label directions\n")

    global type_label  # 3 可以修改为定植
    global direction_label  # lrud 字符串 表示上下左右，键盘的上下左右控制
    global plt_text     # 显示的一些提示文字，按Q会显示输入的一些内容

    unlabeled_imgs = common.get_files(common.SCREENSHOTS_DIR)

    num_labeled = 0  # 现在标记了多少
    for path, filename in unlabeled_imgs:
        print("Processing {}...".format(filename))

        img = plt.imread(path)

        ax = plt.gca()
        fig = plt.gcf()
        plot = ax.imshow(img)

        plt.axis('off')
        plt.tight_layout()
        plt_text = plt.text(0, 0, "")

        # 监听键盘输入事件 zq123上下左右,z是取消之前的输入
        fig.canvas.mpl_connect('key_press_event', on_press)

        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')

        plt.show()

        if type_label and direction_label:
            print('111')
            dst_filename = "{}_{}_{}.png".format(
                type_dictionary[type_label], direction_label, time.strftime("%Y%m%d-%H%M%S"))
            

            os.rename(path, common.LABELED_DIR + dst_filename)

            direction_label = ''
            type_label = None

            num_labeled += 1

    if len(unlabeled_imgs) > 0:  # 这个有修改过吗？os.rename就修改了？
        print("\nLabeled {} out of {} images ({}%).".format(
            num_labeled, len(unlabeled_imgs), 100 * num_labeled // len(unlabeled_imgs)))
        print("Finished!")
    else:
        print("\nThere are no images to label.")


def on_press(event):
    global type_label
    global direction_label

    if event.key in ['1', '2', '3']:
        type_label = event.key
        if len(direction_label) == 4:
            plt.close()
            return

    elif event.key in ['left', 'right', 'up', 'down']:
        if len(direction_label) < 4:
            direction_label += event.key[0]
        if len(direction_label) >= 4 and type_label:
            plt.close()
            return

    elif event.key == 'z':
        type_label = None
        direction_label = ''
    
    if event.key != 'q':
        if not type_label:
            t = '-'
        else:
            t = type_dictionary[type_label]

        plt_text.set_text(make_text(t, direction_label))
        plt.draw()


def make_text(type_label, direction_label):
    directions = []

    for d in direction_label:
        if d == 'd':
            directions.append('down')
        elif d == 'l':
            directions.append('left')
        elif d == 'r':
            directions.append('right')
        elif d == 'u':
            directions.append('up')

    for x in range(len(direction_label), 4):
        directions.append('-')

    return "%s: { %s, %s, %s, %s }" % (type_label, directions[0], directions[1], directions[2], directions[3])

# 这是一个标记功能的程序，并将原文件重命名了，为type-lrud-datetime这样的格式，还没有到训练的地方
if __name__ == "__main__":
    main()
