#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import enchant
import time
import algArtem

# ДАНЯ
d = enchant.Dict("en_US")
# >>> d.check("Hello")
# True
# >>> d.check("Helo")
# False
# >>> d.suggest("Helo")
# ['He lo', 'He-lo', 'Hello', 'Helot', 'Help', 'Halo', 'Hell', 'Held', 'Helm', 'Hero', "He'll"]
# >>>
pattern = re.compile("([A-Z])")

# this is letter frequency in usual english
usualEnglishLettersRate = u"etaoinshrdlcumwfgypbvkjxqz"
usualEnglishLettersRate = usualEnglishLettersRate.upper()


def calculateLettersRate(cipher, keyLen):
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

    # print(lettersCount)
    lettersRate =  []
    for i in range(keyLen):
        temp = sorted(lettersCount[i], key=lettersCount[i].__getitem__, reverse=True)
        letters = u""
        for i in range(len(temp)):
            letters += temp[i]
        lettersRate.append(letters)

    return lettersRate


def frequencyAnalysis(cipher, keyLen, currentRate, lettersRate):
    cipherLetters = u""
    for i in range(cipher.__len__()):
         if pattern.match(cipher[i]):
             cipherLetters += cipher[i]

    text = u""
    for i in range(cipherLetters.__len__()):
        j = i % keyLen
        text += currentRate[j][lettersRate[j].index(cipherLetters[i])]

    for i in range(cipher.__len__()):
        if not pattern.match(cipher[i]):
            text = text[:i] + cipher[i] + text[i:]

    return text



def swapAtIndexes(s, i, j):
    s = list(s)
    s[i], s[j] = s[j], s[i]
    return ''.join(s)


def swap(s, c1, c2):
    print(c1 + c2)
    i = s.index(c1)
    j = s.index(c2)
    return swapAtIndexes(s, i, j)

def calculateOffsetArray(text):
    keyLenOffsetArray = []
    words = re.split("[^A-Z]+", text)
    # words = re.split(" ", text)
    offset = 0 # index of the first letter of the current word| (offset + 1) % keyLen - number of alphabet
    for i in range(words.__len__()):
        keyLenOffsetArray.append(offset)
        for j in range(words[i].__len__()):
            if pattern.match(words[i][j]):
                offset += 1
        # offset += words[i].__len__()

    return keyLenOffsetArray



def suggest(letterList, starIndex):
    candidates = []
    for i in range(ord(u"A"), ord(u"Z")):
        letterList[starIndex] = chr(i)
        word = u"".join(letterList)
        if d.check(word):
            candidates.append(word)

    return candidates


def decipherEnglish(text, keyLen):
    start = time.time()

    lettetsRate = calculateLettersRate(text, keyLen)
    keyLetterRate = []
    for i in range(keyLen):
        keyLetterRate.append(usualEnglishLettersRate)

    # text = frequencyAnalysis(text, keyLen, keyLetterRate, lettetsRate)
    map = algArtem.frequencyAnalysis(text, keyLen)
    offsetArray = calculateOffsetArray(text)

    overal = 0
    words = re.split("[^A-Z]+", text)
    wordsLen = words.__len__()
    for j in range(3):
        for i in range(wordsLen):
            # print(i)
            index = 0
            if words[i].__contains__(u"'") or words[i].__contains__(u'’') or words[i].__len__() < 3:
                continue
            # create word
            word = u""
            unknownLettersInWordCount = 0
            for jndex in range(words[i].__len__()):
                cipherLetter = words[i][jndex]
                keyLetterNumber = (offsetArray[i] + jndex) % keyLen
                letter = map[keyLetterNumber].get(cipherLetter, None)
                if letter == None:
                    word += u"*"
                    unknownLettersInWordCount += 1
                    if unknownLettersInWordCount > 1:
                        break
                    index = jndex
                else:
                    word += letter

            if unknownLettersInWordCount == 1:
                winner = u""
                # print(word)
                candidates = suggest(list(word), index)
                # print(time.time() - start)
                suggestWordsCount = 0
                winnerIndex = 0
                for jndex in range(candidates.__len__()):
                    if suggestWordsCount > 1:
                        break
                    if candidates[jndex].__len__() != words[i].__len__():
                        continue
                    if not usualEnglishLettersRate.__contains__(candidates[jndex][index]):
                        continue
                    letter = candidates[jndex][index]
                    temp = word.replace(u"*", letter)
                    if temp == candidates[jndex]:
                        suggestWordsCount += 1
                        winnerIndex = jndex

                if suggestWordsCount == 1:
                    winner = candidates[winnerIndex]

                if winner != u"":
                    keyLetterNumber = (offsetArray[i] + index) % keyLen
                    cipherLetter = words[i][index]
                    values = map[keyLetterNumber].values()
                    if letter not in values:
                        map[keyLetterNumber].update({words[i][index] : letter})
                    # print winner


    #todo temp hack
    mapOrd = [{} for i in range(keyLen)]
    for i in range(keyLen):
        for key, value in map[i].iteritems():
            mapOrd[i].update({ord(key): value})
    text4 = algArtem.decodeText(text, mapOrd, keyLen)
    print map
    performingTime =  time.time() - start
    print overal
    answerList = []
    answerList.append(text4)
    answerList.append(map)
    answerList.append(performingTime)
    return answerList