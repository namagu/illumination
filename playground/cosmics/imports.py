# this sets where to look for inputs and store outputs
# (it will default to `~/.tess/spyffi` if the $SPYFFIDATA environment variable isn't set)
#import os
#os.environ["SPYFFIDATA"] = '/Users/zkbt/Cosmos/Data/TESS/FFIs'

# some basics
import numpy as np, matplotlib.pyplot as plt
import os, copy, subprocess, glob
import matplotlib.animation as ani
from astropy.io import fits
from .talker import Talker

def mkdir(path):
        '''
        A mkdir that doesn't complain if it already exists.
        '''
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
