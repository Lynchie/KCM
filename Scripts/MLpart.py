import numpy as np
import cv2
from sklearn import linear_model,preprocessing
from sklearn.model_selection import train_test_split
from sklearn import neighbors

import os

from joblib import dump, load

import matplotlib.pyplot as plt

import random

notes = []

label = []

def loadNotes(notes, label, count, file):
    for string in file:
        note = string[1:-3].split(",")
        note = list(map(float,note))
        notes.append(note)
        label.append(count)
    return notes, label
    
    

def loadFiles():
    notes = []
    label = []
    names = []
    count = 0
    directory = 'C:\\Users\\hbrit\\Desktop\\KCM\\KCMVENV'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            f = open(filename)        
            names.append(filename[:-4])
            notes, label = loadNotes(notes, label, count, f)
            count += 1
            continue
        else:
            continue
    return notes, label, names

def kModel(target,data):
    notes , label, names = loadFiles()
    model = neighbors.KNeighborsClassifier(5)
    model.fit(notes,label)
    return model.predict_proba(data), names

    

def lModel(target):
    notes , label = loadFiles(target)
    model = linear_model.LogisticRegression()


def test():

    notes , label = loadFiles(input("TargetFile"))

    print(notes)
    print(label)

    count = []
    randomstate = random.randrange(1,10)

    for size in range(1,180):

        x_train, x_test, y_train, y_test = train_test_split(notes,label,test_size=size*0.005, random_state=randomstate)

    # Logistic
        model1 = linear_model.LogisticRegression()
        model1.fit(x_train,y_train)
        prob = model1.predict_proba(x_test)[:,1]
        wrong1 = []
        for index in range(len(y_test)):
            if round(prob[index]) != y_test[index]:
                wrong1.append(x_test[index])      

    # K-nearest
        model2 = neighbors.KNeighborsClassifier(3)
        model2.fit(x_train,y_train)
        prob = model2.predict_proba(x_test)[:,1]
        wrong2 = []
        for index in range(len(y_test)):
            if round(prob[index]) != y_test[index]:
                wrong2.append(x_test[index])


        count.append([len(wrong1)/size,len(wrong2)/size])

    print("ERRORS\n")
    for i in range(len(count)):
        print("At "+str(i*0.5)+"% test data")
        print("Logistic: "+str(count[i][0]))
        print("KNearest: "+str(count[i][1])+"\n")


    x = [100 - i*0.5 for i in range(1,180)]
    y1 = [wrong[0] for wrong in count]
    y2 = [wrong[1] for wrong in count]

    plt.plot(x,y1,x,y2)
    plt.ylabel("Incorrect classifications")
    plt.xlabel("Training data percentage")
    plt.legend(["Logistic","K-Nearest Neighbour"])
    plt.show()
