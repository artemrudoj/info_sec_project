# -*- coding: utf-8 -*-
__author__ = 'artem'
from random import shuffle
import algGerman


def countOfSymbolsOnText(text):
    return text.__len__


def shuffle_word(word):
    list = []
    for letter in word:
        # print letter
        list.append(letter)
    print u''.join(list)
    shuffle(list)
    print(u''.join(list))
    return ''.join(list)

def superEncrytor(text, keyLen, alphabet):
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
            chipherText += letter


    print(u''.join(chipherText))
    print(chipherLetters)
    return chipherText



def main ():
    print algGerman.usualGermanLettersRate
    superEncrytor(algGerman.usualGermanLettersRate, 1,algGerman.usualGermanLettersRate)



def deleteE(text):
    text = text.replace(u'ё', u'Е')
    return text.replace(u'Ё', u'Е')

if __name__ == '__main__':
    main()



