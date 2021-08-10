import numpy as np
from PIL import Image, ImageDraw
import imageio
import pandas as pd
import time
import os

def make_dorsal_ventral_coor(dorsal, ventral, skeleton_id):
    d_x = []
    d_y = []
    v_x = []
    v_y = []

    for each in dorsal[skeleton_id][:]:
        d_x.append(each[0]/12.4)
        d_y.append(each[1]/12.4)

    for each in ventral[skeleton_id][:]:
        v_x.append(each[0]/12.4)
        v_y.append(each[1]/12.4)

    return d_x, d_y, v_x, v_y

def make_mask(d_x, d_y, v_x, v_y, well, worm_index):

    from PIL import Image, ImageDraw

    polygon = []

    x_i = 0
    while x_i < len(d_x):
        polygon.append(d_x[x_i])
        polygon.append(d_y[x_i])
        x_i += 1

    y_i = len(v_x)-1
    while y_i >= 0:
        polygon.append(v_x[y_i])
        polygon.append(v_y[y_i])
        y_i -= 1

    width = 3600
    height = 3036

    img = Image.new('L', (width, height), 0)
    ImageDraw.Draw(img).polygon(polygon, outline=worm_index, fill=worm_index)

    # Define well coordinates
    if well == 'D4': 
        mask = np.array(img)[180:710, 160:690]
    elif well == 'D3':
        mask = np.array(img)[180:710, 880:1410]
    elif well == 'D2':
        mask = np.array(img)[180:710, 1600:2130]
    elif well == 'D1':
        mask = np.array(img)[180:710, 2320:2850]
    elif well == 'C4':
        mask = np.array(img)[895:1425, 160:690]
    elif well == 'C3':
        mask = np.array(img)[895:1425, 880:1410]
    elif well == 'C2':
        mask = np.array(img)[895:1425, 1600:2130]
    elif well == 'C1':
        mask = np.array(img)[895:1425, 2320:2850]
    elif well == 'B4':
        mask = np.array(img)[1620:2150, 160:690]
    elif well == 'B3':
        mask = np.array(img)[1620:2150, 880:1410]
    elif well == 'B2':
        mask = np.array(img)[1620:2150, 1600:2130]
    elif well == 'B1':
        mask = np.array(img)[1620:2150, 2320:2850]
    elif well == 'A4':
        mask = np.array(img)[2340:2870, 180:710]
    elif well == 'A3':
        mask = np.array(img)[2340:2870, 880:1410]
    elif well == 'A2':
        mask = np.array(img)[2340:2870, 1600:2130]
    elif well == 'A1':
        mask = np.array(img)[2340:2870, 2320:2850]
    elif well == 'D8':
        mask = np.array(img)[180:710, 180:710]
    elif well == 'D7':
        mask = np.array(img)[180:710, 900:1430]
    elif well == 'D6':
        mask = np.array(img)[180:710, 1620:2150]
    elif well == 'D5':
        mask = np.array(img)[180:710, 2340:2870]
    elif well == 'C8':
        mask = np.array(img)[910:1440, 180:710]
    elif well == 'C7':
        mask = np.array(img)[910:1440, 900:1430]
    elif well == 'C6':
        mask = np.array(img)[910:1440, 1620:2150]
    elif well == 'C5':
        mask = np.array(img)[910:1440, 2340:2870]
    elif well == 'B8':
        mask = np.array(img)[1630: 2160, 180:710]
    elif well == 'B7':
        mask = np.array(img)[1630: 2160, 900:1430]
    elif well == 'B6':
        mask = np.array(img)[1630: 2160, 1620:2150]
    elif well == 'B5':
        mask = np.array(img)[1630: 2160, 2340:2870]
    elif well == 'A8':
        mask = np.array(img)[2350: 2880, 180:710]
    elif well == 'A7':
        mask = np.array(img)[2350: 2880, 900:1430]
    elif well == 'A6':
        mask = np.array(img)[2350: 2880, 1620:2150]
    elif well == 'A5':
        mask = np.array(img)[2350: 2880, 2340:2870]
        
        
    mask_cp = np.copy(mask)
    mask_cp = mask_cp.astype(np.uint16)
    if worm_index != 255:
        mask_cp[mask_cp >= 255] = worm_index

    return mask_cp



# function - create 9002*530*530 mask for each well
def make_well_mask(well, traj, dorsal, ventral, well_dict, filename=False, down_sampling=1, frame_start=0, frame_end=9001, sequential=False):
    # well='A4', dorsal=dorsal, ventral=ventral, well_dict=well_dict, filename=False, down_sampling=1, frame_start=0, frame_end=9001, sequential=False

    pd = traj.loc[well_dict[well], :]  # So here it is the position_index, not skel_id
    list_stack = []
    start_time = time.time()
    array_2d = np.zeros(shape=(530, 530), dtype=np.int16)

    print("--------------------%s------------------------" % well)

    ## Second, do frame by frame
    frame_index = frame_start
    while frame_index <= frame_end:
        array_2d = np.zeros(shape=(530, 530), dtype=np.int16)
        skel_id_inframe = list(pd[pd["frame_number"] == frame_index]['skeleton_id'])
        worm_id_inframe = list(pd[pd["frame_number"] == frame_index]['worm_index_joined'])

        for i, skel_id in enumerate(skel_id_inframe):
            worm_index = worm_id_inframe[i]
            dx, dy, vx, vy = make_dorsal_ventral_coor(dorsal, ventral, skel_id)
            mask = make_mask(dx, dy, vx, vy, well, worm_index)
            array_2d = array_2d + mask

        list_stack.append(array_2d)

        if frame_index == frame_start:
            print("Starts at: ", frame_index)

        if frame_index%200 == 0:
            print("Finish frame_index: ", frame_index)
            print("--- %s seconds ---" % (time.time() - start_time))

        if frame_index == frame_end:
            print("Finish!")
            print("--- %s seconds ---" % (time.time() - start_time))

        frame_index += 1
    print("length of list_stack: ", len(list_stack))
    stacked_array = np.stack(list_stack, axis=0)
    stacked_array = stacked_array[:,:,:, np.newaxis]

    if filename:
        output_filename = filename
    else:
        output_filename = "worm_data/22956814/mask_%s.npy" % well

    if down_sampling != 1:
        stacked_array = stacked_array[frame_start:(frame_end+1):down_sampling, :, :, :]

    # Added sequential here
    if sequential == True:
        # Check the unique values in the np arrays - the original worm indices
        uniques_original = list(np.unique(stacked_array))[1:]  # [1:] to omit values == '0'
        print('unique_worm_id: ', uniques_original)
        sequential_ids = range(1, len(uniques_original)+1)
        for i, original in enumerate(uniques_original):
            stacked_array[stacked_array == uniques_original[i]] = sequential_ids[i]  # Update stacked_array with sequential worm_ids

    np.save(output_filename, stacked_array)

    return stacked_array


# Function to make all masks at once, with truncated videos. Each video starts at a new worm's first appearance
def make_well_masks(well, traj, dorsal, ventral, well_dict, down_sampling, file_dir="../22956814/", sequential=False):

    pd= traj.loc[well_dict[well], :]
    worm_ids = pd['worm_index_joined']
    unique_worm_ids = list(np.unique(worm_ids))
    print(unique_worm_ids)

    # Find the first frame for the above worm to appear:
    frame_starts = []
    for worm in unique_worm_ids:
        frame_starts.append(list(pd[pd['worm_index_joined'] == worm]['frame_number'])[0])
    print(frame_starts)
        
    # Also create random.randint between 1,10 for down_sampling:
    # random_down_sampling = [random.randint(1, 10) for x in range(len(unique_worm_ids))]
    #random_down_sampling = [down_sampling for x in range(len(unique_worm_ids))]

    not_empty = []
    rename_flag = 1

    for i, start in enumerate(frame_starts):
        frame_start = start
        down_sampling = down_sampling
        frame_end = start + 100*down_sampling - 1
        fn = file_dir + str(well) + ("_mask_%d.npy" % (i+1))
            #fn = '../22956814/a4_mask_%d.npy' % (i+1)  # '+1' to avoid rewriting the next file!!!!

        mask_array = make_well_mask(well=well, traj=traj, dorsal=dorsal, ventral=ventral, well_dict=well_dict, down_sampling=down_sampling, frame_start=frame_start, frame_end=frame_end, filename=fn, sequential=sequential)
        if mask_array.size == 0:
            os.remove(fn)
        else:
            start_end_sampling = [frame_start, frame_end, down_sampling]  # For sampling raw video
            not_empty.append(start_end_sampling)
            if sequential == False:
                os.rename(fn, file_dir+str(well)+("_mask_%d.npy" % rename_flag))  # Rename the file so that 1,2....n
            elif sequential == True:
                os.rename(fn, file_dir+str(well)+("_mask_seq_%d.npy" % rename_flag))
            rename_flag += 1

    txt_fn = file_dir+str(well)+"_not_empty.txt"
    with open(txt_fn, 'w') as f:
        for each in not_empty[0:-1]:
            f.write(str(each[0]) + ',' + str(each[1]) + ',' + str(each[2]) + '\n')
        f.write(str(not_empty[-1][0]) + ',' + str(not_empty[-1][1]) + ',' + str(not_empty[-1][2]))
