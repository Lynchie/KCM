import random
import cv2
import numpy as np

def findStaves(image):
    foundOnes = []
    staves = []
    for column in range(image.shape[1]):
        for row in range(image.shape[0]):
            if image[row][column] == 255:
                foundOnes.append(row)
    for i in range(image.shape[0]):
        if foundOnes.count(i) == image.shape[1]:
            staves.append(True)
        else:
            staves.append(False)
    return yOfStave(staves)

#let's convert this into a list of y coords because that's disgusting
def yOfStaves(staveList):
    returnList = []
    for i in range(len(staveList)):
        if staveList[i]:
            returnList.append([i,i])
    return returnList


def removeStave(image, staveLines):
  newImage = image
  for line in staveLines:
    newline = np.array([int( (newImage[line[0]-1][i] or newImage[line[1]+1][i])) for i in range(newImage.shape[0])])
    for i in line:
      newImage[i] = newline
  return newImage


image = np.zeros(shape=(100,100))
image[70] = 255
image[60] = 255
image[50] = 255
image[40] = 255
image[30] = 255

for x in range(30,71,10):
  image[x+1] = [random.choice([0,0,0,255]) for i in range(100)] 
  image[x-1] = [random.choice([0,0,0,255]) for i in range(100)]
            
staves = findStaves(img)
newImage = removeStave(image,staves)
cv2.imshow(image)
cv2.imshow(newImage)
