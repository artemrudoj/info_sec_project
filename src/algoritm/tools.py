# -*- coding: utf-8 -*-
__author__ = 'artem'
from random import shuffle
import algGerman
import cipherGerman
import re

def countOfSymbolsOnText(text):
    return text.__len__


def shuffle_word(word):
    list = []
    for letter in word:
        print letter
        list.append(unichr(ord(letter)))
    print list
    shuffle(list)
    return ''.join(list)

def superEncrytor(text, keyLen, lang, alphabet):
    if lang == 0:
        pattern = re.compile("([А-Я])")
    elif lang == 1:
        pattern = re.compile("([A-Z])")
    elif lang == 2:
        pattern = re.compile("([A-ZÄÖÜß])")
    chipherLetters = [u"" for i in range(keyLen)]
    for i in range(keyLen):
        chipherLetters[i] = shuffle_word(alphabet)

    print chipherLetters
    index = 0
    chipherText = u""
    for letter in text:
        if letter in alphabet:
            indexInArray = alphabet.index(letter)
            chipherText = chipherText + chipherLetters[index % keyLen][indexInArray]
            index = index + 1
        else:
            chipherText = chipherText + letter
    return chipherText

def main ():
    print algGerman.usualGermanLettersRate
    print superEncrytor(cipherGerman.textGerman, 6, 2, algGerman.usualGermanLettersRate)


if __name__ == '__main__':
    main()



