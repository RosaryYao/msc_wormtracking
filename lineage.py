import h5py
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np
import sys
import time
import pandas as pd
import shutil
import gc

def make_lineage(traj, well_dict, well, frame_infotxt_dir, mask_npy, suffix):
    """suffix = the number at the end of the mask_npy"""

    array = np.load(mask_npy)
    unique_worm_ids = list(np.unique(array))[1:]

    txt = '../%s/%s_not_empty.txt' % (frame_infotxt_dir, well)
    with open(txt, 'r') as f:
        start_end_samplings = f.read().splitlines()  # Cool!!
        frame_start, frame_end, down_sampling = start_end_samplings[suffix-1].split(",")
        sampling = range(int(frame_start), int(frame_end)+1, int(down_sampling))

    pd = traj.loc[well_dict[well], :]
    lineages = {}

    for worm in unique_worm_ids:
        #worm_pd = pd.loc[pd['worm_index_joined'] == worm]

        nested_dict = {}
        nested_dict['label'] = int(worm)

        frame_list = []

        for i, frame in enumerate(array[:]):
            unique_pixels = list(np.unique(frame))
            if worm in unique_pixels:
                frame_list.append(i)

        #nested_dict['label'] = int(worm)
        nested_dict['frames'] = frame_list
        nested_dict['daughters'] = []
        #nested_dict['capped'] = False
        #nested_dict['frame-div'] = None
        nested_dict['parent'] = None

        lineages[int(worm)] = nested_dict

    del array
    gc.collect()

    return lineages
