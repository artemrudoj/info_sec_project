#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import operator
import itertools
from collections import OrderedDict
import enchant
d = enchant.Dict("en_US")

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
# ДАНЯ менять
usualEnglishLettersRate = u"etaoinshrdlcumwfgypbvkjxqz"
usualEnglishLettersRate = usualEnglishLettersRate.upper()



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

    confirmWords = possibleTheWord(cipher,arrayOfletters,keyLen)
    aWords = possibleAWord(cipher, arrayOfletters, keyLen)
    andWords = possibleAndWord(cipher, arrayOfletters, keyLen)
    mapiingFunction = performPossibleAandAndandThe(cipher,aWords, andWords, confirmWords,keyLen, arrayOfletters)

    #todo temp hack
    map = [{} for i in range(keyLen)]
    for i in range(keyLen):
        for key, value in mapiingFunction[i].iteritems():
            map[i].update({chr(key): value})
    # print chiper1
    # return chiper1
    return map


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

def possibleTheWord(text, lettersRate, keyLen):
    currentIndex = 0
    confirmWords = {}
    tmp = 0
    for word in re.split("[^A-Z]+",text):
        tmp = currentIndex
        if len(word) == 3:
            if(word[2] == lettersRate[(currentIndex + 2) % keyLen][0]):
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
    # toWords = possibleToWord(text, a3, keyLen,lettersRate)
    print "TO:"
    # a4 = frequencyAnalysisWords(toWords, keyLen)

    print "OF:"
    # ofWords = possibleOfWords(text, a4, keyLen,lettersRate)
    # a5 = frequencyAnalysisWords(ofWords, keyLen)
    for i in range(keyLen):
        # переписать
        mappingFunctioons[i].update({ord(a3[i][0][0][0]):u"T"})

        mappingFunctioons[(i + 1) % keyLen].update({ord(a3[i][0][0][1]):u"H"})


        mappingFunctioons[(i + 2) % keyLen].update({ord(a3[i][0][0][2]):u"E"})



        mappingFunctioons[(i + 0) % keyLen].update({ord(a2[i][0][0][0]):u"A"})

        mappingFunctioons[(i + 1) % keyLen].update({ord(a2[i][0][0][1]):u"N"})


        mappingFunctioons[(i + 2) % keyLen].update({ord(a2[i][0][0][2]):u"D"})
    print mappingFunctioons
    return mappingFunctioons

def correctingOfFunction(mappingFunctioons, keyLen, arrayOfLetters):
    map = [{} for i in range(keyLen)]
    usedKeys = []
    for i in range(map.__len__()):
        map[i].update(mappingFunctioons[i])

    for i in range(keyLen):
        usedKeys.append([])
        frequentElementsFlag = True
        while usedKeys[i].__len__() < map[i].__len__():
            for key, value in map[i].iteritems():
                if chr(key) in usedKeys[i]:
                    continue
                temp = value
                if frequentElementsFlag:
                    govnoFlag = False
                    key = chr(key)
                    while key in arrayOfLetters and key not in usedKeys[i]:
                        usedKeys[i].append(key)
                        key = foundKeyByValue(mappingFunctioons[i], key)
                        key = chr(key)
                        govnoFlag = True
                    if govnoFlag:
                        usedKeys[i].append((key))
                        mappingFunctioons[i].update({ord(temp) : key})
                        continue

                usedKeys[i].append(key)
                o = ord(temp)
                mappingFunctioons[i].update({ord(temp):key})

            frequentElementsFlag = False

    pass


def foundKeyByValue(dict, value):
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


def checkAndTranslateWords(words, newMap):

    i = 0
    translatedWords = []
    for word in words:
        newWord = word.translate(newMap)
        if d.check(newWord):
            translatedWords.append(newWord)
            i = i + 1
        else:
            return None

    return translatedWords

def getCountOfTranslatedWords(words, newMap):
    i = 0
    translatedWords = []
    for word in words:
        newWord = word.translate(newMap)
        if d.check(newWord):
            translatedWords.append(newWord)
            i = i + 1
        else:
            return False
    rate = float(i)/float(len(words))
    return True

