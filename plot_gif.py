# Check gif

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np
import sys
import time
import pandas as pd
import cv2
import os
import imageio
import matplotlib as mpl
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import shutil

def plot_gif(np_array, output_fn):
    mpl.rcParams['image.interpolation'] = 'none'  # Prevent mpl smoothes the edges
    os.mkdir("pic_temporary")  # To temporarily store the files

    #spring = cm.get_cmap('spring', 256)
    #newcolors = spring(np.linspace(0, 256, 256))
    #black = np.array([0/256, 0/256, 0/256, 1])
    #newcolors[:1, :] = black
    #newcmp = ListedColormap(newcolors)

    pic_list = []
    flag = 0

    for i in range(np_array.shape[0]):
        #plt.imshow(np_array[i], cmap=newcmp)
        mask = np_array[i]
        mask = np.where(mask==0, -1, mask)
        #print(np.unique(mask_1))

        value = -1
        masked_array = np.ma.masked_where(mask == value, mask)

        #cmap = mpl.cm.get_cmap("spring")
        cmap = mpl.cm.get_cmap("spring").copy()
        cmap.set_bad(color='black')

        plt.imshow(masked_array, cmap=cmap)

        fn = 'pic_temporary/%d.jpg' % flag
        plt.savefig(fn)
        pic_list.append(fn)
        flag += 1

    with imageio.get_writer(output_fn, mode='I') as writer:
        for filename in pic_list:
            image = imageio.imread(filename)
            writer.append_data(image)

    # Remove the temporary file
    shutil.rmtree("pic_temporary")
