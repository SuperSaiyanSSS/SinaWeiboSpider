# coding=utf-8
from __future__ import unicode_literals, print_function
import os


class LoadFolders(object):   # 迭代器
    def __init__(self, par_path):
        self.par_path = par_path

    def __iter__(self):

        for file in os.listdir(self.par_path):
            file_abspath = os.path.join(self.par_path, file)
            if os.path.isdir(file_abspath): # if file is a folder
                yield file_abspath


class LoadFiles(object):
    def __init__(self, par_path):
        self.par_path = par_path

    def __iter__(self):
        folders = LoadFolders(self.par_path)
        for folder in folders:              # level directory
            catg = folder.split(os.sep)[-1]
            for file in os.listdir(folder):     # secondary directory
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path):
                    this_file = open(file_path, 'rb')
                    content = this_file.read()
                    yield catg, content
                    this_file.close()