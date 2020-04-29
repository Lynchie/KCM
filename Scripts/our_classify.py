try:
    import numpy as np
    from scipy import ndimage
except ImportError:
    print('Needs numpy')
    raise

try:
    import pygame
except ImportError:
    print('Needs pygame')
    raise

try:
    from scipy import ndimage
except ImportError:
    print('Needs scipy')

try:
    import cv2
except ImportError:
    print("needs OpenCV")


try:
    from MLpart import kModel 
except ImportError:
    print("needs ML script")
    
manual = True


class Classifier():
    def classify(self, image, posx, posy, fileName, ADDDATA, CurrentSong ):
        #given 2d array of 0s and 1s, return whO knows

        w,h = image.shape

        total = np.sum( image )
        pixelDensity = total/w/h

        borderedImage = np.zeros( (w+2,h+2) )
        borderedImage[1:-1,1:-1] = image
        edgesx = ndimage.sobel( borderedImage, axis = 0 )
        edgesx[edgesx<0]*=-1
        edgesy = ndimage.sobel( borderedImage, axis = 1 )
        edgesy[edgesy<0]*=-1
        edgePerPixel = np.sum( np.hypot(edgesx,edgesy))/total
        edgePerPixelSqr = edgePerPixel/total
        #print(str([w,h,pixelDensity,edgePerPixel]))


        if ADDDATA:
            notes = open(fileName+".txt",'a')
            
            notes.write(str([w,h,pixelDensity,edgePerPixel])+"\n")
            notes.close()
        else:
            prob, names = kModel([[w,h,pixelDensity,edgePerPixel]])

            
            '''
            for name in names:
                print(name,end=" ")
            print()
            for index in range(len(names)):
                print(str(round(prob[0][index],3)).center(len(names[index])),end=' ')
            print('\n')
            '''

            
            symbol = names[np.argmax(prob)]

            if symbol == "clef":
                if CurrentSong.Clef == [0,0,0,0]:
                    CurrentSong.Clef = [posy,posx,h,w]
                    #print('CLEF')
            elif symbol == 'sharp':
                CurrentSong.sharps.append([posy,posx])
            elif symbol == 'flat':
                CurrentSong.flats.append([posy,posx])
            elif symbol == 'natural':
                CurrentSong.naturals.append([posy,posx])
                

        return CurrentSong
            
        
class Song():

    def __init__(self):

        self.Clef=[0,0,0,0]
        self.Key = 0
        self.sharps = []
        self.flats = []
        self.naturals = []
        self.bpm = 0
        self.timesignature = [0,0]
        

    def FindKey(self):
        for sharp in self.sharps:
            if abs(self.Clef[0]+0.5*self.Clef[2]-sharp[0]) < self.Clef[2] and abs(self.Clef[1]+0.5*self.Clef[3]-sharp[1]) < 3*self.Clef[2]:
                self.Key += 1

        if self.Key == 0:
            for flat in self.flats:
                if self.Clef[0]- 0.1 * self.Clef[2] <= flat[0] <= self.Clef[0] + 1.1* self.Clef[2] and flat[1] < (self.Clef[1] + 3*self.Clef[3]):
                    self.Key -= 1


        print(self.Key)
