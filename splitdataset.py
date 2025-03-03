'''
LastEditor: Junjie Lin
Date: 2023-04-30 16:13:17
LastEditTime: 2023-09-27 16:06:19
FilePath: \预处理\splitdataset.py
Description: 
'''
import random

# 读取label.txt文件
with open(r"D:\2023大创\森林火灾中期\dataset\label.txt", "r") as f:
    files = f.read().splitlines()

# 打乱文件名顺序
random.shuffle(files)

# 计算训练集、验证集和测试集的大小
num_files = len(files)
train_size = int(num_files * 0.8)
val_size = int(num_files * 0.1)
test_size = num_files - train_size - val_size

# 将文件名写入train.txt
with open(r"D:\2023大创\森林火灾中期\dataset\train.txt", "w") as f:
    for file in files[:train_size]:
        f.write(file + "\n")

# 将文件名写入val.txt
with open(r"D:\2023大创\森林火灾中期\dataset\val.txt", "w") as f:
    for file in files[train_size:train_size+val_size]:
        f.write(file + "\n")

# 将文件名写入test.txt
with open(r"D:\2023大创\森林火灾中期\dataset\test.txt", "w") as f:
    for file in files[train_size+val_size:]:
        f.write(file + "\n")
