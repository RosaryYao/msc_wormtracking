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

def plot_gif(np_array, output_fn, raw=False, sequential=False, interpolation='none'):
    
    if raw == True:
        sequential = True  # So will not change the original colors!    
        print("Processing raw video.")
    
    if sequential == False:
        # If sequential is False, need to substitute worm indices into sequential for easy colouring
        ## Check the unique values in the np arrays - the original worm indices
        uniques_original = list(np.unique(np_array))[1:]  # [1:] to omit values == '0'
        print('unique_worm_ids: ', uniques_original)
        sequential_ids = range(1, len(uniques_original)+1)
        for i, original in enumerate(uniques_original):
            np_array[np_array == uniques_original[i]] = sequential_ids[i]  # Update stacked_array with sequential worm_ids
        print('sequential ids: ', list(np.unique(np_array))[1:])
    
    mpl.rcParams['image.interpolation'] = interpolation  # Prevent mpl smoothes the edges
    os.mkdir("pic_temporary")  # To temporarily store the files

    pic_list = []
    flag = 0

    np_array[:, 0:2, 0:2] = 10
    np_array[:, 528:530, 528:530] = 1
    
    for i in range(np_array.shape[0]):
        #plt.imshow(np_array[i], cmap=newcmp)
        mask = np_array[i]
        mask = np.where(mask==0, -1, mask)
        #print(np.unique(mask_1))

        value = -1
        masked_array = np.ma.masked_where(mask == value, mask)

        #cmap = mpl.cm.get_cmap("spring")
        if raw == False:
            cmap = mpl.cm.get_cmap("tab20").copy()
        elif raw == True:
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
    

    
def plot_gif_more(np_array, output_fn, raw=False, sequential=False):
    
    if raw == True:
        sequential = True  # So will not change the original colors!    
        print("Processing raw video.")
    
    if sequential == False:
        # If sequential is False, need to substitute worm indices into sequential for easy colouring
        ## Check the unique values in the np arrays - the original worm indices
        uniques_original = list(np.unique(np_array))[1:]  # [1:] to omit values == '0'
        print('unique_worm_ids: ', uniques_original)
        sequential_ids = range(1, len(uniques_original)+1)
        for i, original in enumerate(uniques_original):
            np_array[np_array == uniques_original[i]] = sequential_ids[i]  # Update stacked_array with sequential worm_ids
        print('sequential ids: ', list(np.unique(np_array))[1:])
    
    mpl.rcParams['image.interpolation'] = 'none'  # Prevent mpl smoothes the edges
    os.mkdir("pic_temporary")  # To temporarily store the files

    pic_list = []
    flag = 0

    np_array[:, 0:2, 0:2] = 310
    np_array[:, 528:530, 528:530] = 1
    
    for i in range(np_array.shape[0]):
        #plt.imshow(np_array[i], cmap=newcmp)
        mask = np_array[i]
        mask = np.where(mask==0, -1, mask)
        #print(np.unique(mask_1))

        value = -1
        masked_array = np.ma.masked_where(mask == value, mask)

        #cmap = mpl.cm.get_cmap("spring")
        if raw == False:
            cmap = mpl.cm.get_cmap("tab20").copy()
        elif raw == True:
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
    
    
    
def plot_pic(np_array, output_fn, raw=False, sequential=False):    
    mpl.rcParams['image.interpolation'] = 'none'  # Prevent mpl smoothes the edges
    
    np_array[0:2, 0:2] = 10
    np_array[528:530, 528:530] = 1

    mask = np_array
    mask = np.where(mask==0, -1, mask)

    value = -1
    masked_array = np.ma.masked_where(mask == value, mask)
    cmap = mpl.cm.get_cmap("tab20").copy()
    cmap.set_bad(color='black')
    plt.imshow(masked_array, cmap=cmap)
    plt.savefig(output_fn)
    
def plot_tierpsy_pic(array, output_fn, raw=False, sequential=False):

    uniques_original = list(np.unique(array))[1:]  # [1:] to omit values == '0'
    print('unique_worm_ids: ', uniques_original)
    sequential_ids = range(2, len(uniques_original)+2)

    array[0:2, 0:2] = 10
    array[528:530, 528:530] = 1
    for i, original in enumerate(uniques_original):
        array[array == uniques_original[i]] = sequential_ids[i]  # Update stacked_array with sequential worm_ids
    print('sequential ids: ', list(np.unique(array))[1:])

    plt.imshow(array, cmap="gist_ncar")
    plt.savefig(output_fn)
    

    
    
    
    
    
    

