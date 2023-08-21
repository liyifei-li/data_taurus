import os

# 指定目录路径
path = "./tom61"

# 获取目录下所有文件名
file_list = os.listdir(path)

# 遍历文件名列表，移动文件
for file_name in file_list:
    if "_" in file_name:
        src_path = os.path.join(path, file_name)
        print(file_name)
        dst_path = os.path.join("./maydup", file_name)
        os.rename(src_path, dst_path)