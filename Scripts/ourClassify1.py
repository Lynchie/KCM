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
    from MLpart import kModel, lModel 
except ImportError:
    print("needs ML script")
    
manual = True


class Classifier():
    def classify(self, image, posx, posy, fileName, ADDDATA ):
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
        print(str([w,h,pixelDensity,edgePerPixel]))


        if ADDDATA:
            notes = open(fileName+".txt",'a')
            
            notes.write(str([w,h,pixelDensity,edgePerPixel])+"\n")
            notes.close()
        else:
            prob, names = kModel(fileName,[[w,h,pixelDensity,edgePerPixel]])
            for name in names:
                print(name,end=" ")
            print()
            for index in range(len(names)):
                print(str(prob[0][index]).center(len(names[index])),end=' ')
            print()
                        
        #print(hu)
##        try:
##            
##            if list(np.log10(np.absolute(hu))) not in sharps or manual:
##                
##                notes.append(list(np.log10(np.absolute(hu))))
##                label.append(1)
##                print(notes)
##                print(label)
##        except:
##            return

            
        
class Song():

    def __init__(self):

        self.sheets = []


    def addSheet(self, path):

        self.sheets

        


    

    

    
