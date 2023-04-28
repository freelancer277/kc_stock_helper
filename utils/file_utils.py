
import os

#获取工程文件夹的路径
def get_project_path():
    p_name = "kc_stock_helper"
    p_path =  os.path.abspath(os.path.dirname(__file__))
    return p_path.split(p_name)[0] + p_name


#获取data文件夹的路径
def get_data_path():
    return get_project_path() + "/data/"


#判断当前文件是否存在
def is_file_exist(file_path):
    return os.path.exists(file_path)

#修改文件名
def rename_file(old_file_name,new_file_name):
    os.rename(old_file_name,new_file_name)
#批量修改某个文件夹下的文件名,取前10位字符
def batch_rename_file(file_path):
    file_list = os.listdir(file_path)
    for file in file_list:
        print(file)

        newfile_name = file[0:10]+".csv"
        print(newfile_name)
        rename_file(file_path + file,file_path+newfile_name)


if __name__ == "__main__":
    pass
