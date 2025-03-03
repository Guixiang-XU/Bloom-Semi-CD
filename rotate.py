import os
import numpy as np
from osgeo import gdal
from PIL import Image

def rotate_image(input_path, output_folder):
    # 检查图像格式并相应处理
    file_extension = os.path.splitext(input_path)[1].lower()
    
    if file_extension == '.tif':
        # 使用GDAL处理TIFF文件
        dataset = gdal.Open(input_path)
        if dataset is None:
            print(f"Failed to open file {input_path}")
            return

        band_data = []
        for i in range(1, dataset.RasterCount + 1):
            band = dataset.GetRasterBand(i)
            data = band.ReadAsArray()
            #rotated_data = np.rot90(data, -1)  # 顺时针旋转90度
            #rotated_data = np.rot90(data, -2)  # 顺时针旋转180度
            rotated_data = np.rot90(data, -3)  # 顺时针旋转270度
            band_data.append(rotated_data)

        geotransform = dataset.GetGeoTransform()
        projection = dataset.GetProjection()

        driver = gdal.GetDriverByName('GTiff')
        output_filename = os.path.splitext(os.path.basename(input_path))[0] + "_270.tif"
        output_path = os.path.join(output_folder, output_filename)
        out_dataset = driver.Create(output_path, rotated_data.shape[1], rotated_data.shape[0], dataset.RasterCount, band.DataType)
        out_dataset.SetGeoTransform(geotransform)
        out_dataset.SetProjection(projection)

        for i in range(dataset.RasterCount):
            out_band = out_dataset.GetRasterBand(i + 1)
            out_band.WriteArray(band_data[i])

        out_band.FlushCache()
        out_dataset = None
        dataset = None

    elif file_extension == '.png':
        # 使用Pillow处理PNG文件
        image = Image.open(input_path)
        rotated_image = image.rotate(-90, expand=True)  # 顺时针旋转90度
        #rotated_image = image.rotate(-180, expand=True)  # 顺时针旋转180度
        #rotated_image = image.rotate(-270, expand=True)  # 顺时针旋转270度
        output_filename = os.path.splitext(os.path.basename(input_path))[0] + "_90.png"
        output_path = os.path.join(output_folder, output_filename)
        rotated_image.save(output_path)

    print(f"Rotated image saved to {output_path}")

def process_folder(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.tif') or filename.endswith('.png'):
            input_path = os.path.join(input_folder, filename)
            rotate_image(input_path, output_folder)

# 调用函数
input_folder = r"D:\Bloom labels\label"
output_folder = r"D:\Bloom labels\label_90"
process_folder(input_folder, output_folder)
