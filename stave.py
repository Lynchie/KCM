import random

#makes an array of numbers - u might have guessed that the line of 1st is the stave
img = [[random.randint(0, 1) for i in range(10)],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [random.randint(0,1) for i in range(10)],
        [random.randint(0,1) for i in range(10)]]


#B I C   B O I
bigImg = [[random.randint(0,1) for i in range(100)],
           [1 for i in range(100)],
           [random.randint(0,1) for i in range(100)],
           [random.randint(0,1) for i in range(100)],
           [1 for i in range(100)]]



for i in range(50):
    bigImg.append([random.randint(0,1) for i in range(100)])

#just print the image innit
for i in range(len(img)):
    print(img[i])


def findStaves(image):
    foundOnes = []
    staves = []
    for column in range(len(image[0])):
        for row in range(len(image)):
            if image[row][column] == 1:
                foundOnes.append(row)
    for i in range(len(image)):
        if foundOnes.count(i) == len(image[0]):
            staves.append(True)
        else:
            staves.append(False)
    return staves

            
imgStaves = findStaves(img)
#print(imgStaves)
bigImgStaves = findStaves(bigImg)
#print(bigImgStaves)

#let's convert this into a list of y coords because that's disgusting
def yOfStaves(staveList):
    returnList = []
    for i in range(len(staveList)):
        if staveList[i]:
            returnList.append(i)
    return returnList

print(yOfStaves(imgStaves))
print(yOfStaves(bigImgStaves))