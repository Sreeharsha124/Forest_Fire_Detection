# -*- coding: utf-8 -*- 
"""Forest Fire Image Recognition VGG16.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f0f0D_1raatkUOL0zeV6dAtEy7CcV5XA
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from sklearn.metrics import classification_report, log_loss, accuracy_score
from sklearn.model_selection import train_test_split

from google.colab import drive
drive.mount("/content/gdrive")

directory = '/content/gdrive/My Drive/Datasets/fire_dataset'

Name=[]
for file in os.listdir(directory):
    Name+=[file]
print(Name)
print(len(Name))

N=[]
for i in range(len(Name)):
    N+=[i]

normal_mapping=dict(zip(Name,N))
reverse_mapping=dict(zip(N,Name))

def mapper(value):
    return reverse_mapping[value]

File=[]
for file in os.listdir(directory):
    File+=[file]
    print(file)

trainx0=[]
testx0=[]
trainy0=[]
testy0=[]
count=0
for file in File:
    path=os.path.join(directory,file)
    t=0
    for im in os.listdir(path):
        image=load_img(os.path.join(path,im), grayscale=False, color_mode='rgb', target_size=(128,128))
        image=img_to_array(image)
        image=image/255.0
        n=len(os.listdir(path))
        if t<(n//10)*8:
            trainx0.append([image])
            trainy0.append(count)
        else:
            testx0.append([image])
            testy0.append(count)
        t+=1
    count=count+1

trainy2=to_categorical(trainy0)
X_train=np.array(trainx0).reshape(-1,128,128,3)
y_train=np.array(trainy2)

X_test=np.array(testx0).reshape(-1,128,128,3)

trainx,testx,trainy,testy=train_test_split(X_train,y_train,test_size=0.2,random_state=44)

print(trainx.shape)
print(testx.shape)
print(trainy.shape)
print(testy.shape)

datagen = ImageDataGenerator(horizontal_flip=True,vertical_flip=True,rotation_range=20,zoom_range=0.2,
                        width_shift_range=0.2,height_shift_range=0.2,shear_range=0.1,fill_mode="nearest")

pretrained_model3 = tf.keras.applications.VGG16(input_shape=(128,128,3),include_top=False,weights='imagenet',pooling='avg')
pretrained_model3.trainable = False

inputs3 = pretrained_model3.input
x3 = tf.keras.layers.Dense(128, activation='relu')(pretrained_model3.output)
outputs3 = tf.keras.layers.Dense(2, activation='softmax')(x3)
model = tf.keras.Model(inputs=inputs3, outputs=outputs3)

model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

his=model.fit(datagen.flow(trainx,trainy,batch_size=32),validation_data=(testx,testy),epochs=10)

y_pred=model.predict(testx)
pred=np.argmax(y_pred,axis=1)
ground = np.argmax(testy,axis=1)
print(classification_report(ground,pred))

get_acc = his.history['accuracy']
value_acc = his.history['val_accuracy']
get_loss = his.history['loss']
validation_loss = his.history['val_loss']

epochs = range(len(get_acc))
plt.plot(epochs, get_acc, 'r', label='Accuracy of Training data')
plt.plot(epochs, value_acc, 'b', label='Accuracy of Validation data')
plt.title('Training vs validation accuracy')
plt.legend(loc=0)
plt.figure()
plt.show()
