__author__ = 'artem'
from random import shuffle
import algGerman

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
    return text

def main ():
    print algGerman.usualGermanLettersRate
    superEncrytor(algGerman.usualGermanLettersRate, 1,algGerman.usualGermanLettersRate)


if __name__ == '__main__':
    main()



