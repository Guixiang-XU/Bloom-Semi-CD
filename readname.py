'''
LastEditor: Junjie Lin
Date: 2023-04-30 16:08:04
LastEditTime: 2023-09-26 22:03:29
FilePath: \预处理\readname.py
Description: 
'''
import os

# 设置文件夹路径和输出txt文件路径
folder_path = r"D:\2023大创\森林火灾中期\dataset\label"
output_file = r"D:\2023大创\森林火灾中期\dataset\label.txt"

# 获取文件夹中的所有文件名
files = os.listdir(folder_path)

# 将文件名写入txt文件
with open(output_file, "w") as f:
    for file in files:
        f.write(file + "\n")
