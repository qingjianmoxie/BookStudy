#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: 694317828@qq.com
@software: pycharm
@file: keras_inception3.py
@time: 2019/5/7 14:54
@desc: 用原生态的Keras实现非顺序模型，多输入和多输出模型
"""

import keras
from tflearn.layers.core import fully_connected
from keras.datasets import mnist
from keras.layers import Input, Dense
from keras.models import Model
from keras import backend as K


# 类似前面的方式生成trainX、trainY、testX、testY
num_calsses = 10
img_rows, img_cols = 28, 28

# 通过Keras封装好的API加载MNIST数据。其中trainX就是一个60000x28x28的数组，
# trainY是每一张图片对应的数字。
(trainX, trainY), (testX, testY) = mnist.load_data()

trainX = trainX.reshape(len(trainX), -1)
testX = testX.reshape(len(testX), -1)

# 将图像像素转化为0到1之间的实数。
trainX = trainX.astype('float32')
testX = testX.astype('float32')
trainX /= 255.0
testX /= 255.0

# 将标准答案转化为需要的格式（One-hot编码）。
trainY = keras.utils.to_categorical(trainY, num_calsses)
testY = keras.utils.to_categorical(testY, num_calsses)

# 定义两个输入，一个输入为原始的图片信息，另一个输入为正确答案。
input1 = Input(shape=(784, ), name='input1')
input2 = Input(shape=(10, ), name='input2')

# 定义一个只有一个隐藏节点的全连接网络。
x = Dense(1, activation='relu')(input1)
# 定义只使用了一个隐藏节点的网络结构的输出层。
output1 = Dense(10, activation='softmax', name='output1')(x)
# 将一个隐藏节点的输出和正确答案拼接在一起，这个将作为第二个输出层的输入。
y = keras.layers.concatenate([x, input2])
# 定义第二个输出层。
output2 = Dense(10, activation='softmax', name='output2')(y)

# 定义一个有多个输入和多个输出的模型，这里只需要将所有的输入和输出给出即可。
model = Model(inputs=[input1, input2], outputs=[output1, output2])

# 定义损失函数、优化函数和评测方法。若多个输出的损失函数相同，可以只指定一个损失函数。
# 如果多个输出的损失函数不同，则可以通过一个列表或一个字典来指定每一个输出的损失函数。
# 比如可以使用：loss = {'output1': 'binary_crossentropy', 'output2': 'binary_crossentropy'}
# 来为不同的输出指定不同的损失函数。类似的，Keras也支持为不同输出产生的损失指定权重，
# 这可以通过通过loss_weights参数来完成。在下面的定义中，输出output1的权重为1，output2
# 的权重为0.1。所以这个模型会更加偏向于优化第一个输出。
model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.SGD(), loss_weights=[1, 1], metrics=['accuracy'])

# 模型训练过程。因为有两个输入和输出，所以这里提供的数据也需要有两个输入和两个期待的正确
# 答案输出。通过列表的方式提供数据时，Keras会假设数据给出的顺序和定义Model类时输入输出
# 给出的顺序是对应的。为了避免顺序不一致导致的问题，这里更推荐使用字典的形式给出。
model.fit(
    [trainX, trainY], [trainY, trainY],
    batch_size=128,
    epochs=20,
    validation_data=([testX, testY], [testY, testY])
)