import numpy as np

sharp = [-2, -0.3, 25,	4, 23]

def logReg(feat,note):
    y = feat[0]*note[0]+ feat[1]*note[1]+feat[2]*note[2]+feat[3]*note[3]+note[4]
    return 1/(1+np.e**-y)
