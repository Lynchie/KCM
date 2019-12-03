import numpy as np
import pygame
import cv2
from scipy import ndimage



def load_as_array( path ):

    #takes path of image
    #returns array of pixel values 0-255
    #each pixel is accessed using [x,y,col] where col= 0,1,2 for R,G,B

    arr = cv2.imread( path )
    if type(arr) != type(None):
        return np.swapaxes( arr[:,:,::-1], 0, 1 )


def array_to_surface( arr ):

    #give a 2D array or 3D array with depth 3
    #returns a surface, either black and white if 2D or RGB if 3D    

    if len(arr.shape) == 2:
        narr = np.zeros( (arr.shape[0],arr.shape[1],3) )
        narr[:,:,0] = arr
        narr[:,:,1] = arr
        narr[:,:,2] = arr
    else:
        narr = arr.copy()

    narr[narr>255] = 255
    narr[narr< 0 ] =  0

    surf = pygame.Surface( narr.shape[:2] )

    surfarray = pygame.surfarray.pixels3d(surf)

    ax,ay = narr.shape[:2]
    surfarray[:,:] = narr
    del surfarray

    return surf


def big_draw( arr ):
    #give a 2D or 3D array, outputs a numpy window :)

    surf = array_to_surface( arr )

    pygame.init()
    screen = pygame.display.set_mode( arr.shape[:2] )

    screen.blit( surf, (0,0) )
    pygame.display.update()

    clock = pygame.time.Clock()
    while True:

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

path = input('Enter path of image to load: ')

arr = load_as_array( path )

if type(arr) != type(None) :
    big_draw( arr )

