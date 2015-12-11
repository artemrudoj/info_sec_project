#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
pattern = re.compile("^([A-Z])$")

def main(text, key):
    global pattern
    text = text.upper()
    key = key.upper()
    cipherText = u""
    keyLen = key.__len__()
    keyInt = []
    for i in range(keyLen):
        keyInt.append(ord(key[i]) - ord(u'A'))
    print keyInt

    ordOfZChar = ord(u'Z')
    offset = 0

    for i in range(text.__len__()):
        j = (i - offset) % keyLen
        if pattern.match(text[i]):
            newOrd = ord(text[i]) + keyInt[j]
            if newOrd > ordOfZChar:
                newOrd -= 26
            cipherText += chr(newOrd)
        else:
            offset += 1
            cipherText += text[i]

    print(text)
    print(cipherText)
    return cipherText