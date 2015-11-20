from django.db import models
from enum import Enum

class Lang(Enum):
    ru = 0
    en = 1
    fr = 2

class SourceText():
    text = ""
    lang = Lang.ru
    def __init__(self, text, lang):
        self.text = text
        self.lang = lang



