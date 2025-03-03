'''
LastEditor: Junjie Lin
Date: 2023-04-30 17:10:14
LastEditTime: 2023-09-27 15:34:13
FilePath: \预处理\rgb2gray.py
Description: 
'''
from PIL import Image

# 打开PNG文件
img = Image.open(r"D:\小美赛\2023第十二届认证杯数学中国数学建模国际赛（小美赛）赛题\B题的缺陷数据集\kos01_label\Part0.bmp")

# 将图像转换为灰度图像
gray_img = img.convert('L')

# 保存灰度图像
gray_img.save("A.png")
