#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import operator
import itertools
from collections import OrderedDict
from django.utils.encoding import smart_str
import enchant

# d = enchant.Dict("de_DE")
# >>> d.check("Hello")
# True
# >>> d.check("Helo")
# False
# >>> d.suggest("Helo")
# ['He lo', 'He-lo', 'Hello', 'Helot', 'Help', 'Halo', 'Hell', 'Held', 'Helm', 'Hero', "He'll"]
# >>>
pattern = re.compile(u"([А-Я])")
pattern = re.compile(u"([А-Я])$")
patternQuots = re.compile("[\"]")
patternNewLine = re.compile("[\n]")

def deleteChangeBadSymbols(text):
    text = text.upper()
    text = re.sub(patternQuots, '', text)
    text = re.sub(patternNewLine, ' ', text)
    return text

# this is letter frequency in usual english
# ДАНЯ менять
usualRussianLettersRate  = u"оеаинтслвркмдпыубяьгзчйжхшюцэщфёъ"
# usualEnglishLettersRate = usualEnglishLettersRate.upper()
usualRussianLettersRate  = usualRussianLettersRate.upper()




def frequencyAnalysis(cipher, keyLen):
    cipherLetters = u""
    for i in range(cipher.__len__()):
         if pattern.match(cipher[i]):
             cipherLetters += cipher[i]

    lettersCount = []

    for j in range(keyLen):
        lettersCount.append({})
        for i in range(ord(u'А'), ord(u'Я') + 1, 1):
            lettersCount[j][unichr(i)] = 0


    for i in range(cipherLetters.__len__()):
        lettersCount[i % keyLen][cipherLetters[i]] += 1

    print lettersCount

    sorted_lettersCount = []
    arrayOfletters = []
    for j in range(keyLen):
        sorted_lettersCount.append(sorted(lettersCount[j].items(), key=operator.itemgetter(1)))
        arrayOfletters.append(sorted(lettersCount[j], key=lettersCount[j].__getitem__, reverse=True))
    print (sorted_lettersCount)
    print "qdqd"
    print(arrayOfletters)

    #ДАНЯ переписать
    chtoWords = possibleChtoWord(cipher,arrayOfletters,keyLen)
    kakWords = possibleKakWord(cipher, arrayOfletters, keyLen)
    # neWords = possibleNeWord(cipher, arrayOfletters, keyLen)
    neWords =[]
    mapiingFunction = performPossibleChtoAndKakAndNe(cipher, chtoWords, kakWords, neWords, keyLen, arrayOfletters)
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
    # chiper1 = decodeText(cipher, mapiingFunction,keyLen)


    #todo temp hack
    map = [{} for i in range(keyLen)]
    for i in range(keyLen):
        for key, value in mapiingFunction[i].iteritems():
            map[i].update({unichr(key): value})
    # print chiper1
    # return chiper1
    return map


def decodeText(text, mappingFunctions,  keyLen):
    indexInText = 0
    indexInMappers = 0
    newText = ""
    for i in range(text.__len__()):
        if text[i] in usualRussianLettersRate:
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



# Russian
def possibleChtoWord(text, lettersRate, keyLen):
    currentIndex = 0
    confirmWords = {}
    tmp = 0
    print "что:"
    for word in re.split(u"[^А-Я]+",text):
        tmp = currentIndex
        if len(word) == 3:
            # print word
            # print smart_str(u"".join(lettersRate[(currentIndex + 2) % keyLen]))
            if(word[2] in lettersRate[(currentIndex + 2) % keyLen][0:1]): # о
                # print word
                if (word[1] in lettersRate[(currentIndex + 1) % keyLen][2:8]): #т
                    print word
                    if (word[0] in lettersRate[(currentIndex + 0)  % keyLen][13:25]): #ч
                        confirmWords[tmp] = word
            currentIndex = currentIndex + 3
        else:
            currentIndex = currentIndex + len(word)
    print confirmWords
    return confirmWords

def possibleKakWord(text, lettersRate, keyLen):
    currentIndex = 0
    confirmWords = {}
    tmp = 0
    print "как:"
    for word in re.split(u"[^А-Я]+",text):
        tmp = currentIndex
        if len(word) == 3:
            if(word[1] in lettersRate[(currentIndex + 1) % keyLen][1:7]): #а

                if (word[0] in lettersRate[(currentIndex + 0) % keyLen][7:15]): #к
                    if (word[2] in lettersRate[(currentIndex + 2)  % keyLen][7:15]): #к
                        confirmWords[tmp] = word
            currentIndex = currentIndex + 3
        else:
            currentIndex = currentIndex + len(word)
    print confirmWords
    return confirmWords

def possibleNeWord(text, lettersRate, keyLen):
    currentIndex = 0
    confirmWords = {}
    tmp = 0
    print "как:"
    for word in re.split(u"[^А-Я]+",text):
        tmp = currentIndex
        if len(word) == 2:
            if(word[1] in lettersRate[(currentIndex + 1) % keyLen][0:2]): #e
                if (word[0] in lettersRate[(currentIndex + 0) % keyLen][2:7]): #н
                    confirmWords[tmp] = word
            currentIndex = currentIndex + 3
        else:
            currentIndex = currentIndex + len(word)
    print confirmWords
    return confirmWords

def performPossibleChtoAndKakAndNe(text, chtoWords, kakWords, neWords, keyLen, lettersRate):
    print u"Freq analys Words"
    mappingFunctioons = [{} for i in range(keyLen)]
    mappingFunctioonsFuckOrd = [{} for i in range(keyLen)]
    print u"Что:"
    a1 = frequencyAnalysisWords(chtoWords, keyLen)
    print a1
    print u"Как:"
    a2 = frequencyAnalysisWords(kakWords, keyLen)
    print a2
    # print u"Не:"
    # a3 = frequencyAnalysisWords(neWords, keyLen)
    # print a3

    for i in range(keyLen):
        # переписать
        if (a1[i] != []):
            mappingFunctioons[(i + 0) % keyLen].update({ord(a1[i][0][0][0]):u"Ч"})

            mappingFunctioons[(i + 1) % keyLen].update({ord(a1[i][0][0][1]):u"Т"})

            mappingFunctioons[(i + 2) % keyLen].update({ord(a1[i][0][0][2]):u"О"})

        if (a2[i] != []):
            mappingFunctioons[(i + 0) % keyLen].update({ord(a2[i][0][0][0]):u"К"})

            mappingFunctioons[(i + 1) % keyLen].update({ord(a2[i][0][0][1]):u"А"})

        # if (a3[i] != []):
        #     mappingFunctioons[(i + 0) % keyLen].update({ord(a3[i][0][0][0]):u"Н"})
        #
        #     mappingFunctioons[(i + 1) % keyLen].update({ord(a3[i][0][0][1]):u"Е"})

    return mappingFunctioons


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
    return  words


# if __name__ == '__main__':

    # keyLen not always good
    # keyLen = 6
    # # frequencyAnalysis(cipherForGerman1, keyLen)
    #
    # frequencyAnalysis(sourceTextForGerman1.upper(), keyLen)
    # print cipherForGerman1
    # print sourceTextForGerman1
