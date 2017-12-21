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

lib.dictionary_add.argtypes = (POINTER(DictionaryS), c_char_p, c_char_p, )

lib.dictionary_contains.argtypes = (POINTER(DictionaryS), c_char_p)
lib.dictionary_contains.restype = bool

lib.dictionary_synonym.argtypes = (POINTER(DictionaryS), c_char_p)
lib.dictionary_synonym.restype = c_char_p


class Dictionary:
    def __init__(self):
        self.obj = lib.dictionary_new()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        lib.dictionary_free(self.obj)

    def add(self, keyword, synonym):
        lib.dictionary_add(self.obj, keyword.encode("utf-8"), synonym.encode("utf-8"))

    def contains(self, keyword):
        return lib.dictionary_contains(self.obj, keyword.encode("utf-8"))

    def synonym(self, keyword):
        return lib.dictionary_synonym(self.obj, keyword.encode("utf-8"))


with Dictionary() as dictionary:
    dictionary.add("hello", "world")
    print("{}".format(dictionary.contains("hello")))
    print("{}".format(dictionary.contains("hllo")))
    print("{}".format(dictionary.synonym("hello")))
    print("{}".format(dictionary.synonym("hllo")))
