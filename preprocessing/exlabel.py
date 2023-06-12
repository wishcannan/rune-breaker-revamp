'''
主旨是给ex文件夹下的 图片打标签用的 顺便丢弃一下没用的图片（现在没有做打分系统 所以 不像箭头的图片也进来了)
'''
import os
import sys
import time
sys.path.insert(0, os.path.abspath('.'))
import matplotlib.pyplot as plt
import numpy as np
import common
plt.rcParams['figure.figsize']=(3.6, 3.6)


def main():
    print("ARROW KEYS = label directions\n")
    global direction_label
    unlabeled_imgs = common.get_files(common.EX_DIR)
    num_labeled = 0
    for path, filename in unlabeled_imgs:
        print("Processing {}...".format(filename))
        #打开图片
        img = plt.imread(path)
        ax = plt.gca()
        fig = plt.gcf()
        plot = ax.imshow(img)
        #不显示x和y轴
        plt.axis('off')
        plt.tight_layout()
        plt_text = plt.text(0, 0, "")
        #开启监听
        fig.canvas.mpl_connect('key_press_event', on_press)
        #全屏用的 用不到
        # mng = plt.get_current_fig_manager()
        # mng.window.state('zoomed')

        plt.show()

        if direction_label == 'z':
            plt.close()
            os.remove(path)
            print(filename,'不符合arrow')
            num_labeled += 1
            direction_label = ''
            continue
        elif direction_label:
            dst_filename = "{}_{}.png".format(direction_label,time.strftime("%Y%m%d-%H%M%S"))
            os.rename(path, './data/ex_labeled/' + dst_filename)
            time.sleep(0.5)
            direction_label = ''
            num_labeled += 1

    if len(unlabeled_imgs) > 0:
        print("\nLabeled {} out of {} images ({}%).".format(
            num_labeled, len(unlabeled_imgs), 100 * num_labeled // len(unlabeled_imgs)))
        print("Finished!")
    else:
        print("\nThere are no images to label.")

def on_press(event):
    global direction_label

    if event.key in ['left', 'right', 'up', 'down']:
        direction_label = event.key[0]
        plt.close()
        return

    elif event.key == 'z':
        direction_label = 'z'
        plt.close()
        return
    

if __name__ == "__main__":
    main()