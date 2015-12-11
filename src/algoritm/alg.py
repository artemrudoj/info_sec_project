#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import operator
import itertools
from collections import OrderedDict
import enchant
d = enchant.Dict("en_US")
# >>> d.check("Hello")
# True
# >>> d.check("Helo")
# False
# >>> d.suggest("Helo")
# ['He lo', 'He-lo', 'Hello', 'Helot', 'Help', 'Halo', 'Hell', 'Held', 'Helm', 'Hero', "He'll"]
# >>>
pattern = re.compile("([A-Z])")
pattern = re.compile("([A-Z])$")
patternQuots = re.compile("[\"]")
patternNewLine = re.compile("[\n]")

def deleteChangeBadSymbols(text):
    text = text.upper()
    text = re.sub(patternQuots, '', text)
    text = re.sub(patternNewLine, ' ', text)
    return text

# this is letter frequency in usual english
usualEnglishLettersRate = u"etaoinshrdlcumwfgypbvkjxqz"
usualEnglishLettersRate = usualEnglishLettersRate.upper()







def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b.

    Unless b==0, the result will have the same sign as b (so that when
    b is divided by it, the result comes out positive).
    """
    while b:
        a, b = b, a%b
    return a

def keyCount(cipher):
    global nl, N
    print cipher

    cipherLetters = u""
    for i in range(cipher.__len__()):
         if pattern.match(cipher[i]):
             cipherLetters += cipher[i]

    print cipherLetters
    for i in range(cipherLetters.__len__() - N):
        print "for " + str(i)
        str1 = cipherLetters[i:i + N]
        for j in range(i + 1, cipherLetters.__len__() - N, 1):
            str2 = cipherLetters[j:j + N]
            if str2 == str1:
                print(i)
                print(j)
                print(cipherLetters[i:i + N])
                print(cipherLetters[j:j + N])
                l[nl] = j - 1
                nl += 1

    print l
    print nl

    i = 0
    while i < nl:
        j = i + 1
        while j < nl:
            a = int(l[i])
            b = int(l[j])
            a = gcd(a, b)
            index = int(a)
            if index < 500:
                nods[index] += 1
            j += 1
        i += 1

    keylen = 3

    for i in range(3, 500):
        if nods[keylen] < nods[i]:
            keylen = i
    print nods
    print "keylen: " + str(keylen)
    return keylen





def frequencyAnalysis(cipher, keyLen):
    cipherLetters = u""
    for i in range(cipher.__len__()):
         if pattern.match(cipher[i]):
             cipherLetters += cipher[i]


    lettersCount = []

    for j in range(keyLen):
        lettersCount.append({})
        for i in range(ord('A'), ord('Z') + 1, 1):
            lettersCount[j][chr(i)] = 0


    for i in range(cipherLetters.__len__()):
        lettersCount[i % keyLen][cipherLetters[i]] += 1


    sorted_lettersCount = []
    arrayOfletters = []
    for j in range(keyLen):
        sorted_lettersCount.append(sorted(lettersCount[j].items(), key=operator.itemgetter(1)))
        arrayOfletters.append(sorted(lettersCount[j], key=lettersCount[j].__getitem__, reverse=True))
    print (sorted_lettersCount)
    print "qdqd"
    print(arrayOfletters)

    confirmWords = possibleTheWord(cipher,arrayOfletters,keyLen)
    aWords = possibleAWord(cipher, arrayOfletters, keyLen)
    andWords = possibleAndWord(cipher, arrayOfletters, keyLen)
    mapiingFunction = performPossibleAandAndandThe(cipher,aWords, andWords, confirmWords,keyLen, arrayOfletters)
    # formMappingTheAndA("THE", confirmWords, keyLen, aWords)
    # #считаем , что букву е мы знаем
    # firstPartOfMappingFunctions = wordsFromMostPopularLetter(cipher, arrayOfletters, 1, 11, keyLen)
    # print "nextStep"
    # secondPartOfMappingFunctions = secondPopularLettersWord(cipher, firstPartOfMappingFunctions, arrayOfletters, 11, 20, usualEnglishLettersRate[11:20], keyLen)
    # #
    # # # print secondPartOfMappingFunctions
    # for i in range(keyLen):
    #        firstPartOfMappingFunctions[i].update(secondPartOfMappingFunctions[i])
    # print firstPartOfMappingFunctions
    chiper1 = decodeText(cipher, mapiingFunction,keyLen)
    print chiper1
    # return chiper1


def decodeText(text, mappingFunctions,  keyLen):
    indexInText = 0
    indexInMappers = 0
    newText = ""
    for i in range(text.__len__()):
        if ord(text[i]) in range(ord('A'), ord('Z') + 1, 1):
            index = ord(text[i])
            a = mappingFunctions[indexInMappers % keyLen].get(index)
            if (a == None):
                a = text[i]
            indexInMappers = indexInMappers + 1
            newText = newText + a
            indexInText + 1
        else:
            newText = newText + text[i]
            indexInText + 1
    return newText


def wordsFromMostPopularLetter(text, lettersRate, begin, end, keyLen):
    shortArrayOfLetters = []
    forLetterE = []
    for j in range(keyLen):
        shortArrayOfLetters.append(lettersRate[j][begin:end])
        forLetterE.append({ord(lettersRate[j][0]):u"E"})
    print forLetterE
    print "Cutted version of letters arrays"
    print shortArrayOfLetters
    newInglishLetter = usualEnglishLettersRate[begin:end]
    print newInglishLetter
    decoder = Decoder(shortArrayOfLetters, keyLen, newInglishLetter, forLetterE)
    for word in text.split():
        decoder.isCorrectWord(word, forLetterE)
    return  decoder.decodeConfirmWords()

def possibleTheWord(text, lettersRate, keyLen):
    currentIndex = 0
    confirmWords = {}
    tmp = 0
    for word in re.split("[^A-Z]+",text):
        tmp = currentIndex
        if len(word) == 3:
            if(word[2] == lettersRate[(currentIndex + 2) % keyLen][0]):
                print word
                if (word[0] in lettersRate[(currentIndex + 0) % keyLen][1:5]):
                    if (word[1] in lettersRate[(currentIndex + 1)  % keyLen][2:12]):
                        confirmWords[tmp] = word
            currentIndex = currentIndex + 3
        else:
            currentIndex = currentIndex + len(word)
    print confirmWords
    return confirmWords

def possibleAndWord(text, lettersRate, keyLen):
    currentIndex = 0
    confirmWords = {}
    tmp = 0
    for word in re.split("[^A-Z]+",text):
        tmp = currentIndex
        if len(word) == 3:
            c1 = searchInArrayOfChar(word[0], lettersRate[currentIndex % keyLen], 1,8)
            if(c1 != None):
                c2 = searchInArrayOfChar(word[1], lettersRate[(currentIndex + 1) % keyLen], 1,8)
                if (c2 != None):
                    c3 = searchInArrayOfChar(word[2], lettersRate[(currentIndex + 2) % keyLen], 8,12)
                    if (c3 != None):
                        if (c3 > c2) and ( c2 > c1):
                            confirmWords[tmp] = word
            currentIndex = currentIndex + 3
        else:
            currentIndex = currentIndex + len(word)
    print confirmWords
    return confirmWords

def searchInArrayOfChar(c, array, begin, end):
    for i in range(begin,end,1):
        if (c == array[i]):
            return i
    return  None

def possibleAWord(text, lettersRate, keyLen):
    currentIndex = 0
    confirmWords = {}
    tmp = 0
    for word in re.split("[^A-Z]+",text):
        tmp = currentIndex
        if len(word) == 1:
            if (word[0] in lettersRate[currentIndex % keyLen][1:5]):
                confirmWords[tmp] = word
            currentIndex = currentIndex + 1
        else:
            currentIndex = currentIndex + len(word)
    return confirmWords

def formMappingTheAndA(possibleWord, confirmWords, keyLen, aWords):
    mappigFunctions = [{}] * keyLen
    for key, value in confirmWords.iteritems():
        for i in range(len(possibleWord)):
            if possibleWord[i] not in mappigFunctions[(key + i ) % keyLen]:
                mappigFunctions[(key + i ) % keyLen][possibleWord[i]] = ord(value[i])
            else:
                if mappigFunctions[(key + i ) % keyLen][possibleWord[i]] != ord(value[i]):
                    print mappigFunctions
                    print "ERROR in possible word " + possibleWord + ":" + value + ":"+ str(chr(mappigFunctions[(key + i ) % keyLen][possibleWord[i]]))
    print mappigFunctions
    return mappigFunctions


def possibleToWord(text, a3, keyLen, lettersRate):
    currentIndex = 0
    confirmWords = {}
    tmp = 0
    for word in re.split("[^A-Z]+",text):
        tmp = currentIndex
        if len(word) == 2:
            if (word[0] in a3[currentIndex % keyLen][0][0][0]):
                if (word[1] in lettersRate[(currentIndex + 1) % keyLen][1:5]):
                    confirmWords[tmp] = word
            currentIndex = currentIndex + 2
        else:
            currentIndex = currentIndex + len(word)
    print confirmWords
    return confirmWords


def possibleOfWords(text, a4, keyLen, lettersRate):
    currentIndex = 0
    confirmWords = {}
    tmp = 0
    for word in re.split("[^A-Z]+",text):
        tmp = currentIndex
        if len(word) == 2:
            if (word[0] in a4[(currentIndex + 1) % keyLen][0][0][1]):
                print word
                if (word[1] in lettersRate[(currentIndex + 1)% keyLen][9:20]):
                    confirmWords[tmp] = word
            currentIndex = currentIndex + 2
        else:
            currentIndex = currentIndex + len(word)
    print confirmWords
    return confirmWords
    pass





def performPossibleAandAndandThe(text, aWords, andWords, theWords,keyLen, lettersRate):
    print "Freq analys Words"
    mappingFunctioons = [{} for i in range(keyLen)]
    mappingFunctioonsFuckOrd = [{} for i in range(keyLen)]
    print "A:"
    a1 = frequencyAnalysisWords(aWords,keyLen)
    print "AND:"
    a2 = frequencyAnalysisWords(andWords,keyLen)
    print a2
    print "THE:"
    a3 = frequencyAnalysisWords(theWords, keyLen)
    print a3
    toWords = possibleToWord(text, a3, keyLen,lettersRate)
    print "TO:"
    a4 = frequencyAnalysisWords(toWords, keyLen)

    print "OF:"
    # ofWords = possibleOfWords(text, a4, keyLen,lettersRate)
    # a5 = frequencyAnalysisWords(ofWords, keyLen)
    for i in range(keyLen):
        mappingFunctioons[i].update({ord(a3[i][0][0][0]):u"T"})

        mappingFunctioons[(i + 1) % keyLen].update({ord(a3[i][0][0][1]):u"H"})


        mappingFunctioons[(i + 2) % keyLen].update({ord(a3[i][0][0][2]):u"E"})



        mappingFunctioons[(i + 0) % keyLen].update({ord(a2[i][0][0][0]):u"A"})

        mappingFunctioons[(i + 1) % keyLen].update({ord(a2[i][0][0][1]):u"N"})


        mappingFunctioons[(i + 2) % keyLen].update({ord(a2[i][0][0][2]):u"D"})

        # mappingFunctioonsFuckOrd[i].update({(a3[i][0][0][0]):u"T"})
        # mappingFunctioonsFuckOrd[(i + 1) % keyLen].update({(a3[i][0][0][1]):u"H"})
        # mappingFunctioonsFuckOrd[(i + 2) % keyLen].update({(a3[i][0][0][2]):u"E"})
        # mappingFunctioonsFuckOrd[(i + 0) % keyLen].update({(a2[i][0][0][0]):u"A"})
        # mappingFunctioonsFuckOrd[(i + 1) % keyLen].update({(a2[i][0][0][1]):u"N"})
        # mappingFunctioonsFuckOrd[(i + 2) % keyLen].update({(a2[i][0][0][2]):u"D"})
        # mappingFunctioons[(i + 1) % keyLen].update({ord(a4[i][0][0][1]):u"O"})
        # mappingFunctioons[(i + 1) % keyLen].update({ord(a5[i][0][0][1]):u"F"})




        # mappingFunctioons[(i + 1) % keyLen].update({ord(u"O"):a4[i][0][0][1]})
        # mappingFunctioons[(i + 1) % keyLen].update({ord(u"F"):a5[i][0][0][1]})
    #correctMappingFucntions = correctingOfFunction(mappingFunctioons, keyLen,"THEAND")
    print mappingFunctioons
    return mappingFunctioons


def foundKeyByVale(dict, value):
    for key in dict.keys():
        if dict[key] == value:
            return key



def frequencyAnalysisWords(aWord, keyLen):
    words =  [{} for i in range(keyLen)]
    for key, value in aWord.iteritems():
        if value not in words[key % keyLen]:
            elem = {}
            elem[value] = 1
            words[key % keyLen].update(elem.copy())
        else:
            words[key % keyLen][value] = words[key % keyLen][value] + 1
    for i in range(keyLen):
        #FIXME
        words[i] = sorted(words[i].items(), key=operator.itemgetter(1), reverse=True)
        print str(i) + ": " + str(words[i])
    return  words