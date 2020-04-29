import os

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
    import cv2
except ImportError:
    print('Needs CV2')

try:
    import our_classify as ourClassify
except ImportError:
    print('Needs a classification file')

try:
    import custom_display as cd
except ImportError:
    print('Needs customdisplay file')

import time
import random
'''
Takes image from folder
Detects straight, horizontal staff lines
Removes staff lines and highlights areas of interest
Detects separate notes in areas of interest and passes them to external
  classification program
Displays layers of array on screen

Changed from 1.0: flood fill keeps track of edgemost pixels
                  fixed return from floodfill to disclude not floodfilled
Changed from 1.1: classify when clicked
Changed from 1.2: options added, also some options are broken OOP
Changed from 1.3: -hopefully- it actually works
'''


DEFAULTPATH = 'HearMeOutSmall.png'

STAFFDETECTION = ['sum','run'][0] #change index to change algorithm used
STAFFLENGTHTHRESHHOLD = 500 #used by staff detection, minimum sum or run to be detected as a staff line
STAVEDISTHRESHHOLD = 25 #minimum distance between staff lines to group as block, best if 2.5*normal width

DRAWSTAVES = False
DRAWRELEVANT = True

MORGANSTAFFS = 3 #ask morgan why the variable name is dumb

TESTALL = False
DRAW = True
CLASSIFY = True


def test():
    
    arr = loadImage()
    arr,classifier = preProcess(arr)
    startTime = time.time()
    arr = process(arr,classifier)
    print('Process time:',time.time()-startTime)
    arr = postProcess(arr,classifier)

#------------------------------------------------------------------------------

def loadImage():


    scriptDir = os.path.dirname(__file__) #<-- absolute dir the script is in
    relPath = "images"
    folderPath = os.path.join(scriptDir,relPath)

    inDir = next(os.walk(folderPath))[2]
    print('PNGs in directory:')
    for thing in inDir:
        if thing[-4:]=='.png':
            print(' -',thing)
    print()

    path = input('Enter path of image to load: ')
    if path == '':
        path = DEFAULTPATH

    path = os.path.join(folderPath,path)

    arr = cd.load_as_array( path ) # Try and load image of array

    if type(arr) == type(None) : #If no image in the directory was found, return
        raise 'Image not found in directory, rerun and change input'

    return arr
    

def preProcess(arr):
    
    arr = binarize( arr[:,:,:],200 ) #Turns array into 0s and 1s
    arr *= 255

    classifier = None#ourClassify.Classifier()

    return arr, classifier


def process(arr,classifier):

    s = staves( arr[:,:,0]/255 ) #calculate position of staves
    if s != []:
        slist = pair_up(s) #turn stave list from [3,4,5,10] to [[3,5],[10,10]]

        allStaves = groupStaves( slist, pair=False)
        groups = [ [ g[0][0],g[-1][-1] ] for g in allStaves ] #turns staves into chunks
        arr[:,:,0] = removeAllStaves( arr[:,:,0], slist )
        if DRAWSTAVES:
            drawRegions( arr[:,:,1], slist )
        if DRAWRELEVANT:
            drawRegions( arr[:,:,2], groups )

    
    if TESTALL:

        for note in nextNote(arr[:,:,0],groups, 0):
            removeClassifyNote( arr, note[0], note[1], classifier )

    return arr


def postProcess(arr,classifier):

    if DRAW:
        big_draw_plus( arr,classifier ) 

    return arr

#------------------------------------------------------------------------------

def binarize( arr, threshhold ):

    if len(arr.shape) == 2:
        narr = np.zeros( arr.shape, dtype = int )
        narr[arr>threshhold] = 1
        return narr

    elif len(arr.shape) == 3:
        narr = np.ones( arr.shape, dtype = int )
        narr[:,:,0] = np.sum( arr, axis=2 )
        narr[narr>threshhold*arr.shape[2]] = 1
        narr[narr!=1] = 0
        return narr
        
        
def staves( arr ):

    height = arr.shape[1]

    staves = []

    if STAFFDETECTION == 'sum':
        rowsums = arr.shape[0]-np.sum(arr,axis=0)
    else:
        rowsums = [ longest_run(arr[:,i], 0 ) for i in range(height) ]

    for i in range(height):
        #run = longest_run(arr[:,i], 1)
        run = rowsums[i]
        if run > STAFFLENGTHTHRESHHOLD:
            staves.append(i)

    return staves


def pair_up( staves ):

    pairstaves = [staves[0]]
    
    for i in range(len(staves)-1):
        if staves[i]+1 != staves[i+1]:
            pairstaves.extend((staves[i], staves[i+1]))

    pairstaves.append(staves[-1])

    pairstaves = [ [pairstaves[i],pairstaves[i+1]] for i in range(0,len(pairstaves),2) ]
  
    return pairstaves
        
    
def longest_run( arr, value ):
    longest = 0
    current = 0
    for i in range(arr.shape[0]):
        if arr[i] == value:
            current += 1
            longest = max(longest,current)
        else:
            current = 0
    return longest


def removeAllStaves( arr, staves ):

    for line in staves:
        removeStave(arr,line)

    return arr
        

def removeStave( arr, line ):

    lineAbove = arr[:,line[0]-1]
    lineBelow = arr[:,line[1]+1]

    newLine = np.logical_and( lineAbove,lineBelow )

    for i in range(line[0],line[1]+1):
        arr[:,i] = newLine
        arr[:,i]*= 255

    
def drawRegions( arr, staves ): # draws horizontal regions based on a list of lists of top and bottom of regions

    sx,sy = arr.shape

    for line in staves:
        arr[ 0:sx, line[0]:line[1]+1 ] = 0

    return arr


def groupStaves( staves, pair=False ):
    
    if len(staves)%5:
        print('Staves detected not a multiple of 5')

    staves = staves.copy()
    grouped = []

    while staves:
        grouped.append( [ staves.pop(0) ] )

        bigGap = False
        while staves and not bigGap:     
        
            if staves[0][0] - grouped[-1][-1][-1] < STAVEDISTHRESHHOLD:
                grouped[-1].append( staves.pop(0) )
            else:
                bigGap = True

    if pair:
        if len(grouped)%MORGANSTAFFS:
            grouped.append( [] )
            print('Odd number of stave groups detected')


        if MORGANSTAFFS == 3:
            grouped = [ grouped[i]+grouped[i+1]+grouped[i+2] for i in range(0,len(grouped),3) ]
        else:    

            grouped = [ grouped[i]+grouped[i+1] for i in range(0,len(grouped),2) ]

    return grouped
            
#-------------------------- Separate -------------------------------

def nextNote( arr, regions, value ):

    for region in regions:
        regionStart, regionEnd = region#[0][0], region[-1][-1]

        for row in range(regionStart,regionEnd):
            for column in range( arr.shape[0] ):
                if arr[column,row] == value:
         
                    yield column, row#floodFillRemove( arr, column,row )


def relativeIndices( arr, true, centre ):
    
    relPos = np.where( arr==centre )
    relX = relPos[0][0]
    relY = relPos[1][0]

    trues = np.where( arr==true )
    truePairs = [ (trues[0][i],trues[1][i]) for i in range(len(trues[0])) ] 
    relTruePairs = [ (pair[0]-relX,pair[1]-relY) for pair in truePairs ]

    return relTruePairs
    

def floodFillRemove( arr, x, y ):

    connected = np.array(((1,1,1),
                          (1,2,1),
                          (1,1,1))) #Gives what is a connection, looks relative to the 2
    conList = relativeIndices(connected,1,2)
    #turns connected into a list of indices for all values of 1, relative to the 2

    temparr = np.zeros( arr.shape, dtype = int )
    temparr[ arr==arr[x,y] ] = 1
    temparr[x,y] = 2

    edges = [ (x,y) ]

    left,right,top,bottom = x,x,y,y

    sizex,sizey = arr.shape

    while edges:
        #print(edges)
        ex,ey = edges.pop(0)
        for con in conList:
            newx,newy = ex+con[0],ey+con[1]
            if 0<=newx<sizex and 0<=newy<sizey:
                if temparr[newx,newy] == 1:
                    edges.append((newx,newy))
                    temparr[newx,newy] = 2

                    #Keeps running track of where the extremes of the image are
                    left   = min(left,  newx)
                    right  = max(right, newx)
                    top    = min(top   ,newy)
                    bottom = max(bottom,newy)

    arr[temparr==2] = 255
    
    temparr = temparr==2
    return temparr[ left:right+1 , top:bottom+1 ], left, top

        

def removeClassifyNote( arr, x, y, classifier ):

    image,x,y = floodFillRemove( arr[:,:,0], x, y )
    w,h = image.shape

    if CLASSIFY:
        #classifier.classify( image, x, y )
        ourClassify.classify( image, x, y )

    arr[x:x+w, y:y+h,1][image==True] = 0#(1-image)*255

              
#------------------------- Draw ------------------------------------
        
def big_draw_plus( arr,classifier ):
    #give a 2D or 3D array, outputs a numpy window :)

    surf = cd.array_to_surface( arr )

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

            if not TESTALL:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx,my = pygame.mouse.get_pos()

                    if not arr[mx,my,0]==0:
                        pass
                        #print('Not note')
                    else:
                        removeClassifyNote( arr, mx,my, classifier )
                        
                        surf = cd.array_to_surface( arr )
                        screen.blit( surf, (0,0) )
                        pygame.display.update()
    

    
if __name__ == '__main__':
    test()
