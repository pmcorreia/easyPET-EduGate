

from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt

from skimage.io import imread
from skimage import data_dir
from skimage.transform import radon, rescale
from skimage.transform import iradon
from skimage.morphology import disk
from skimage.filters import rank, gaussian,gabor,hessian,frangi
import scipy.misc

import sys


filename=sys.argv[1]
sinogram = imread(filename, as_grey=True)
theta = np.linspace(0., 360.,360, endpoint=False)
sinogram = gaussian(sinogram,  sigma=1, mode='mirror',
                    cval=0, multichannel=None,
                    preserve_range=False, truncate=1.0)
reconstruction_fbp = iradon(sinogram, theta=theta, circle=True,
                            filter='cosine', interpolation='cubic')
scipy.misc.imsave('outfile.jpg', reconstruction_fbp)
