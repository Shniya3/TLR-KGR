import re
import nltk
import os
import csv

from pip._vendor import chardet

import openTxt


def comment_extractt(dir, class_list):
    object2comment_dict = {}
    with open(dir, encoding="ISO-8859-1") as file:
        lines = file.readlines()
    break_flag_1 = False
    break_flag_2 = False
    ###存/* */
    record_list_2 = []
    record_1 = 0
    for record_index, line in enumerate(lines):
        if line.find("/*") is not -1:
            record_list_2.append(record_index)
            record_1 = record_index
        if line.find("*/") is not -1:
            record_list_2.append(record_index)
            record_2 = record_index
            if record_2 > record_1:
                for index, line_2 in enumerate(lines):
                    if break_flag_1 is True:
                        break_flag_1 = False
                        break
                    if index > record_2 :
                        for class_object in class_list:
                            if line_2.find(class_object) is not -1:
                                if class_object in object2comment_dict.keys():
                                    for text in lines[record_1:(record_2+1)]:
                                        object2comment_dict[class_object] += text
                                else:
                                    object2comment_dict[class_object] = ""
                                    for text in lines[record_1:(record_2+1)]:
                                        object2comment_dict[class_object] += text
                                break_flag_1 = True
                                break

        if line.find("//") is not -1:
            record_3 = record_index
            for index, line_3 in enumerate(lines):
                if break_flag_2 is True:
                    break_flag_2 = False
                    break
                if index < record_3:
                    for class_object in class_list:
                        if line_3.find(class_object) is not -1:
                            if class_object in object2comment_dict.keys():
                                object2comment_dict[class_object] += line_3
                            else:
                                object2comment_dict[class_object] = ""
                                object2comment_dict[class_object] += line_3
                            break_flag_2 = True
                            break
                            
    if len(record_list_2) % 2 is not 0:
        return False

    return object2comment_dict


def file_path(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root, end=' ')  # 当前目录路径
        # print(dirs, end=' ')    # 当前路径下的所有子目录
        # print(files)            # 当前目录下的所有非目录子文件
    print(os.walk(file_dir))
    return root, dirs, files



if __name__ == '__main__':

    # with open('./data/CC/EA140.txt', 'rb') as file:
    #     print(chardet.detect(file.read())) # {'encoding': 'utf-8', 'confidence': 0.87625, 'language': ''}
    #     a=file.readlines()
    #     print(a)

    root, dirs, files = file_path("./data/eTour/CC/")
    record = []
    class_num,ea2class = openTxt.ea2class_open("./data/ea2class.txt")
    comment_dict = {}
    for file in files:
        print(file)
        class2comment_dict = comment_extractt((root+file), ea2class[file.replace(".txt","")])
        for key in class2comment_dict.keys():
            if key not in comment_dict:
                comment_dict[key] = class2comment_dict[key]
            else:
                comment_dict[key] += class2comment_dict[key]
    with open("./data/class2comment.txt","w",encoding="utf-8") as file:
        for key in comment_dict:
            file.write(key+"\t"+(comment_dict[key].replace("\t","").replace("\n","").replace("/*","").replace("*/","").replace("//","").replace("*","").replace("@",""))+"\n")



