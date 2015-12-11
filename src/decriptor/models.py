# -*- coding: utf-8 -*-
from enum import Enum
from algoritm import tools
class Lang(Enum):
    ru = 0
    en = 1
    de = 2

class SourceText():
    text = ""
    lang = Lang.ru
    keyLen = []
    mappingFunctions = []
    textLen = 0
    def __init__(self, text, lang):
        self.text = text
        self.lang = lang
        self.textLen = tools.countOfSymbolsOnText(text)
        self.keyLen = []
        self.mappingFunctions = []



