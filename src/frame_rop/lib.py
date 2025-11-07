'''
    Shared object loader
'''
import os
from ctypes import cdll

TARGET_DIR = "c_lib"
TARGET_SO = "frame_rop.so"

lib_path = os.path.dirname(__file__)
so_path = f'{lib_path}/{TARGET_DIR}/{TARGET_SO}'

lib_redirect = cdll.LoadLibrary(so_path)
