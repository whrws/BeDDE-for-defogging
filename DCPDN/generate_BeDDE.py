#coding=utf-8
from __future__ import division

import sys
sys.path.append("./mingqingscript")

import os
import glob
import h5py

import numpy as np
from scipy import misc


def array2PIL(arr, size):
    mode = 'RGBA'
    arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
    if len(arr[0]) == 3:
        arr = np.c_[arr, 255*numpy.ones((len(arr),1), numpy.uint8)]
        return Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)

# ------------------
test_image_root = '../my_testset/resized'
save_root = '../my_testset/for_DCPDN'

save_size = 1024 # 512 is default
# ------------------

cityFolderNames = list()
allRootFiles = os.listdir(test_image_root)

for folderName in allRootFiles:
    if '.' != folderName and '..' != folderName and ('.' not in folderName):
        cityFolderNames.append(folderName)

    for cityName in cityFolderNames:
        curImgFolder = os.path.join(test_image_root, cityName, 'fog')
        curSaveFolder = os.path.join(save_root, cityName, 'fog')
        if not os.path.exists(curSaveFolder):
            os.makedirs(curSaveFolder, mode=0o777)

        curImageNames = glob.glob(os.path.join(curImgFolder,'*.png'))

        for imgName in curImageNames:
            print('process %s'%imgName)
            img = misc.imread(imgName)

            img_rs = misc.imresize(img, (save_size,save_size), 'bilinear').astype(float)
            haze_image=img_rs
            # gt_img=img_rs

            # img = img/255

            haze_image=haze_image/255
            # gt_img=gt_img/255

            prefix = imgName.split('/')[-1][:-4]
            saveFilePath = os.path.join(curSaveFolder, prefix+'.h5')
            h5f=h5py.File( saveFilePath,'w')

            h5f.create_dataset('haze',data=haze_image)
            h5f.create_dataset('trans',data=0)
            h5f.create_dataset('ato',data=0)
            h5f.create_dataset('gt',data=0)
