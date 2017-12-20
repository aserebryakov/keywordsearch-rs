#!/usr/bin/env python3

import sys, ctypes
from ctypes import c_char_p, c_uint32, Structure, POINTER

# Object stub
class DictionaryS(Structure):
    pass

# Preparations
prefix = {'win32': ''}.get(sys.platform, 'lib')
extension = {'darwin': '.dylib', 'win32': '.dll'}.get(sys.platform, '.so')
lib = ctypes.cdll.LoadLibrary(prefix + "kwrd" + extension)

lib.dictionary_new.restype = POINTER(DictionaryS)

lib.dictionary_free.argtypes = (POINTER(DictionaryS), )

lib.add_keyword.argtypes = (POINTER(DictionaryS), c_char_p, c_char_p, )

lib.contains_keyword.argtypes = (POINTER(DictionaryS), c_char_p)
lib.contains_keyword.restype = bool


class Dictionary:
    def __init__(self):
        self.obj = lib.dictionary_new()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        lib.dictionary_free(self.obj)

    def add_keyword(self, keyword, synonym):
        lib.add_keyword(self.obj, keyword.encode("utf-8"), synonym.encode("utf-8"))

    def contains_keyword(self, keyword):
        return lib.contains_keyword(self.obj, keyword.encode("utf-8"))


with Dictionary() as dictionary:
    dictionary.add_keyword("hello", "world")
    print("{}".format(dictionary.contains_keyword("hello")))
    print("{}".format(dictionary.contains_keyword("hllo")))
