#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 20:19:08 2019

@author: nyakov
"""

import os
import sys
import glob
import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
plt.switch_backend("agg")

args = sys.argv
dirpath = args[1]
file_list = glob.glob(dirpath + "/*.h5")

error_dn = 65535
slope = 0.02
map_shape = (4320, 8640)
image_array_list = []
valid_array_list = []
for filepath in file_list:
    print(filepath)
    hdf = h5py.File(filepath,'r')
    tmp_array = np.array(hdf["/Image_data/LST_AVE"])
    image_array = np.where(tmp_array == error_dn, 0, tmp_array) * slope
    image_array_list.append(image_array)
    valid_array_list.append(np.where(tmp_array == error_dn, False, True))

sum_array = np.zeros(map_shape)
num_array = np.zeros(map_shape)
for image_array, valid_array in zip(image_array_list, valid_array_list):
    sum_array += image_array
    num_array += np.where(valid_array == True, 1, 0)

num_array = np.where(num_array == 0, 1, num_array)

ave_array = sum_array / num_array.astype(np.float32)

celsius_array = ave_array - 273.15
celsius_array = np.where(celsius_array < 0, 0, celsius_array)

filename = os.path.basename(file_list[0])
title_str = "Land surface temperature({0})[°C]\n{1}/08/09,10,11".format(filename[15:16], filename[7:11])
out_name = "LST_{0}_{1}.png".format(filename[15:16], filename[7:11])

fig = plt.figure()
plt.imshow(celsius_array[1000:1500,7400:7900], cmap="hot", norm=Normalize(vmin=0, vmax=55))
plt.title(title_str)
plt.colorbar()
plt.savefig(out_name, format="png", dpi=300)
plt.close(fig)
