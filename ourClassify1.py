
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


def classify( image, posx, posy ):
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

    print('w {:<3} h {:<3} pixelDensity {:<6.4g} edgePerPixel {:<6.4g}'.format(w,h,pixelDensity,edgePerPixel))

        
class Song():

    def __init__(self):

        self.sheets = []


    def addSheet(self, path):

        self.sheets

        


    

    

    
