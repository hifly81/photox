# coding: latin-1

'''
Created on Aug 21, 2014

@author: hifly
'''

import os.path

def extract_extension(path):
    extension = os.path.splitext(path)[1]
    return extension
