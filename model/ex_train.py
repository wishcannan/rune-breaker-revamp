from keras.callbacks import EarlyStopping, TensorBoard
from keras.layers import Activation, Dense, Flatten, Dropout
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator

import common
import argparse
import os

BATCH_SIZE = 128
def main(batch_size, model_name):
    pass


def make_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same', input_shape=common.INPUT_SHAPE))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    pass


if __name__ == "__main__":
    os.system('color')
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--batch_size', type=int, default=BATCH_SIZE,
                      help="指定训练次数")
    parser.add_argument('-m', '--model', type=str, default="arrow_model.h5",
                      help="指定模型名称")

    args = parser.parse_args()

    main(args.batch_size, args.model)