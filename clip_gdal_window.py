'''
LastEditor: Junjie Lin
Date: 2023-04-30 15:20:53
LastEditTime: 2023-09-27 15:35:42
FilePath: \预处理\clip_gdal_window.py
Description: 
'''
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 13:39:40 2022

@author: dongzhen
"""
####切256 注意tif和png要改
import os
from osgeo import gdal, gdalnumeric, gdal_array
import numpy as np

def OpenArray(array, prototype_ds = None, xoff=0, yoff=0):
    # array->gdal dataset
    #ds = gdal.Open( gdalnumeric.GetArrayFilename(array) )
    ds = gdal_array.OpenArray(array)
    if ds is not None and prototype_ds is not None:
        if type(prototype_ds).__name__ == 'str':
            prototype_ds = gdal.Open( prototype_ds )
        if prototype_ds is not None:
            # copy geoinfo (gdal dataset)
            gdal_array.CopyDatasetInfo( prototype_ds, ds, xoff=xoff, yoff=yoff )
    return ds


def clip(imagefolder, inputform, subXsize, subYsize, overlap):
    for file in os.listdir(imagefolder):
        file = os.path.join(imagefolder, file)
        fileForm = os.path.splitext(file)[1][1:]
        
        if fileForm == inputform:
            srcArray = gdal_array.LoadFile(file)
            srcImage = gdal.Open(file)
            oriH = srcImage.RasterYSize
            oriW = srcImage.RasterXSize
            
            newSaveFolder = os.path.splitext(file)[0][0:]  # subimages save in new folder
            #newSaveFolder = r'D:\0dongzhen\2019年预测图像稀疏表征智能分析竞赛\label\label'
            os.makedirs(newSaveFolder, exist_ok = True)
            
            # lists for saving subimages and corresponding positions
            subImages = []
            subImagesPos = []
            
            # acquire subimage_array by window
            for i in range(0, oriH, subYsize - overlap):
                i = np.minimum(i, oriH-subYsize)
                for j in range(0, oriW, subXsize - overlap):
                    j = np.minimum(j, oriW-subXsize)
                    # bands
                    if srcImage.RasterCount == 1:
                        clip = srcArray[i:i + subXsize, j:j + subYsize]
                        # Create a three-channel image with the same data for R, G, and B channels
                        # clip = np.repeat(clip[np.newaxis, :, :], 3, axis=0)
                    else:
                        clip = srcArray[:, i:i+subXsize, j:j+subYsize]
                        sw = srcArray[0, i:i + subXsize, j:j + subYsize]
                        n = srcArray[1, i:i + subXsize, j:j + subYsize]
                        r = srcArray[2, i:i + subXsize, j:j + subYsize]
                        g = srcArray[3, i:i + subXsize, j:j + subYsize]
                        b = srcArray[4, i:i + subXsize, j:j + subYsize]
                        clip = np.array([sw,n,r,g,b])
                        print(clip.shape)
                    subImages.append(clip)
                    subImagesPos.append([j, i])
            
            # write subimage by window  (gdal dataset)
            for k in range(len(subImages)):
                print("begin to write:", k+1, "th subimage of", file)
                subimage = newSaveFolder + '\\' + file.split('\\')[-1].split('.')[0] + '_' + str(k+1) + '.' + fileForm
                #driver = gdal.GetDriverByName("GTiff")
                #第一处修改
                driver = gdal.GetDriverByName("PNG")
                # copy gdal dataset
                driver.CreateCopy(subimage, 
                                  OpenArray(subImages[k], 
                                            prototype_ds = file, 
                                            xoff = subImagesPos[k][0], 
                                            yoff = subImagesPos[k][1]))
    
if __name__ == '__main__':
    imagefolder = r"D:\2023大创\test"#第二处修改
    inputform = 'png'#第三处
    subXsize = 256
    subYsize = 256
    overlap = 0
    clip(imagefolder, inputform, subXsize, subYsize, overlap)