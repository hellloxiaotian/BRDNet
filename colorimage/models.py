# -*- coding: utf-8 -*-

import numpy as np
#import tensorflow as tf
from keras.models import *
from keras.layers import  Input,Conv2D,BatchNormalization,Activation,Lambda,Subtract,concatenate,Add,merge
import keras.backend  as K
from batch_renorm import BatchRenormalization
def BRDNet(): #original format def BRDNet(), data is used to obtain the reshape of input data
    inpt = Input(shape=(None,None,3)) #if the image is 3, it is color image. If the image is 1, it is gray color, 201807082123tcw
    # 1st layer, Conv+relu
    x = Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), padding='same')(inpt)
    x = BatchRenormalization(axis=-1, epsilon=1e-3)(x)
    x = Activation('relu')(x)
    # 15 layers, Conv+BN+relu
    for i in range(7):
        x = Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), padding='same')(x)
        x = BatchRenormalization(axis=-1, epsilon=1e-3)(x)
        x = Activation('relu')(x)   
    # last layer, Conv 
    for i in range(8):
        x = Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), padding='same')(x)
        x = BatchRenormalization(axis=-1, epsilon=1e-3)(x)
        x = Activation('relu')(x) 
    x = Conv2D(filters=3, kernel_size=(3,3), strides=(1,1), padding='same')(x) #gray is 1 color is 3
    x = Subtract()([inpt, x])   # input - noise
    y = Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), padding='same')(inpt)
    y = BatchRenormalization(axis=-1, epsilon=1e-3)(y)
    y = Activation('relu')(y)
    # 15 layers, Conv+BN+relu
    for i in range(7):
        y = Conv2D(filters=64, kernel_size=(3,3), strides=(1,1),dilation_rate=(2,2), padding='same')(y)
        y = Activation('relu')(y)   
    y = Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), padding='same')(y)
    y = BatchRenormalization(axis=-1, epsilon=1e-3)(y)
    y = Activation('relu')(y) 
    for i in range(6):
        y = Conv2D(filters=64, kernel_size=(3,3), strides=(1,1),dilation_rate=(2,2), padding='same')(y)
        y = Activation('relu')(y)
    y = Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), padding='same')(y)
    y = BatchRenormalization(axis=-1, epsilon=1e-3)(y)
    y = Activation('relu')(y)    
    y = Conv2D(filters=3, kernel_size=(3,3), strides=(1,1), padding='same')(y)#gray is 1 color is 3
    y = Subtract()([inpt, y])   # input - noise
    o = concatenate([x,y],axis=-1)
    z = Conv2D(filters=3, kernel_size=(3,3), strides=(1,1), padding='same')(o)#gray is 1 color is 3
    z=  Subtract()([inpt, z])
    model = Model(inputs=inpt, outputs=z)
    return model
   




