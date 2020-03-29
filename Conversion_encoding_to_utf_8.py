# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:48:51 2020

@author: ChenghaoAdmin
"""

import os
import codecs
import chardet

def list_folders_files(path):
    """
    :param path: path of folder and file
    :return:  (list_folders, list_files)

    """
    list_folders = []
    list_files = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            list_folders.append(file)
        else:
            list_files.append(file)
    return (list_folders, list_files)

def convert(file, in_enc="GBK", out_enc="UTF-8"):
    """
    :param file:    file path
    :param in_enc:  input file encode-form
    :param out_enc: output file encode-form
    :return:
    """
    in_enc = in_enc.upper()
    out_enc = out_enc.upper()
    try:
        print("convert [ " + file.split('\\')[-1] + " ].....From " + in_enc + " --> " + out_enc)
        f = codecs.open(file, 'r', in_enc, "ignore")
        new_content = f.read()
        codecs.open(file, 'w', out_enc).write(new_content)
    except IOError as err:
        print("I/O error: {0}".format(err))

if __name__ == "__main__":
    path = r'C:\\xxx\\newdata' #path of dataset
    (list_folders, list_files) = list_folders_files(path)

    print("Path: " + path)
    for fileName in list_files:
        filePath = path + '\\' + fileName
        with open(filePath, "rb") as f:
            data = f.read()
            codeType = chardet.detect(data)['encoding']
            convert(filePath, codeType, 'UTF-8')