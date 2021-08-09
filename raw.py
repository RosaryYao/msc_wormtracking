import h5py
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
import random
import gc

def get_raw_well(well, video_path="../22956814/22956814.mp4", well_name='A4', filename=False, frame_start=0, frame_end=9001, down_sampling=1):
    print('--------', well_name, '--------')
    frames = []

    ymin = well[0]
    ymax = well[1]
    xmin = well[2]
    xmax = well[3]

    #path = "../22956814/22956814.mp4"
    cap = cv2.VideoCapture(video_path)
    ret = True
    while ret:
        ret, img = cap.read() # read one frame from the 'capture' object; img is (H, W, C)
        if ret:
            frames.append(img[ymin:ymax, xmin:xmax, :])

    stacked = np.stack(frames, axis=0)
    stacked = stacked.astype(dtype='float32')
    stacked_mean = np.mean(stacked, axis=3)[:,:,:,None]

    if frame_start != 0 or frame_end != 9001 or down_sampling != 1:
        stacked_mean = stacked_mean[frame_start:(frame_end+1):down_sampling, :, :, :]

    if filename:
        output_fn = filename
    else:
        output_fn = 'well_A/raw_%s.npy' % well_name

    np.save(output_fn, stacked_mean)


def make_raw_videos(raw_video_path, mask_frame_info_fn, well_name, output_dir):
    #raw_video = np.load('../22956814/raw_wells/A1.npy')
    raw_video = np.load(raw_video_path)

    #mask_frame_info_fn = "../22956814/%s_not_empty.txt" % 'A1'

    with open(mask_frame_info_fn, 'r') as f:
        start_end_samplings = f.read().splitlines()  # Cool!!
        for i, each in enumerate(start_end_samplings):
            frame_start, frame_end, down_sampling = each.split(",")
            fn = output_dir + "/%s_raw_%d.npy" % (well_name, (i+1))

            frame_start = int(frame_start)
            frame_end = int(frame_end)
            down_sampling = int(down_sampling)

            raw_array = raw_video[frame_start:frame_end+1:down_sampling, :, :, :]
            print(raw_array.shape)

            # IMPORTANT!!
            if raw_array.shape[0] != 100:
                print("HAVE TO REMOVE: ", fn, " and its masked npy!")
                fn_remove.append(fn)

            np.save(fn, raw_array)

            # Clear the raw_array memory
            del raw_array
            gc.collect()

    # At the end, clear raw_video memory
    del raw_video
    gc.collect()
