
import numpy as np
import matplotlib.pyplot as plt

def floodFill(x, y, objectPoint, image, points):
    
    
    if x<0 or y<0 or x >= image.shape[1] or y >= image.shape[0] or [y,x] in objectPoint:
        #print(str(x) +" " +str(y)+ " is out of bound")
        return
    
    if image[y][x][0] == 255:
        return
    
    objectPoint.append([y,x])
    points.append([y,x])
    
    floodFill(x-1,y-1,objectPoint,image,points)
    floodFill(x,y-1,objectPoint,image,points)
    floodFill(x+1,y-1,objectPoint,image,points)
    floodFill(x-1,y,objectPoint,image,points)
    floodFill(x+1,y,objectPoint,image,points)
    floodFill(x-1,y+1,objectPoint,image,points)
    floodFill(x,y+1,objectPoint,image,points)
    floodFill(x+1,y+1,objectPoint,image,points)

def findBounds(objectPoint):
    maxX = objectPoint[0][1]
    maxY = objectPoint[0][0]
    minX = objectPoint[0][1]
    minY = objectPoint[0][0]
    for y,x in objectPoint:
        if y > maxY:
            maxY = y
        elif y < minY:
            minY = y
        if x > maxX:
            maxX = x
        elif x < minX:
            minX = x
    return [[minY-1,minX-1],[maxY+2,maxX+2]]

def extractImageAt(image, x, y,points):
    print("extracting at "+str(x)+" "+str(y))
    objectPoint = []
    
    floodFill(x,y,objectPoint,image,points)
    #print(objectPoint)
    bounds = findBounds(objectPoint)
    mins = bounds[0]
    maxs = bounds[1]
    
    newImage = np.array(image[mins[0]:maxs[0],mins[1]:maxs[1]])
    
    return newImage


def extractAllImages(image):
    notes = []
    points = []
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            #print(str(x)+" "+str(y))
            if image[y][x][0] == 0:
                if [y,x] not in points:
                    singleNote = extractImageAt(image,x,y,points)
                    notes.append(singleNote)
    return notes

def displayNewImages(images):
    index = -1
    while index < len(images):
        index += 1
        plt.figure()
        plt.imshow(images[i])
