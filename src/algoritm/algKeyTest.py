#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
pattern = re.compile("([A-Z])$")
patternQuots = re.compile("[\"]")
patternNewLine = re.compile("[\n]")

pattern = re.compile("([A-Z])")

my_final_words = []
my_final_diff = []
my_search_word = []
my_wrd_arr = []
my_dif_arr = []
index_arr = []
str = u""
myindex = 0

def key_count(cipher):
    global nl, N
    print cipher
    global my_final_diff
    global my_search_word
    global my_wrd_arr
    global my_dif_arr
    global index_arr
    global str
    global myindex
    cipherLetters = u""
    for i in range(cipher.__len__()):
        if i > 4000:
            break
        if pattern.match(cipher[i]):
             cipherLetters += cipher[i]
    print cipherLetters
    arr_index = 0
    word_lenght = 3
    for i in range(cipherLetters.__len__() - word_lenght):
        my_search_word.append(cipherLetters[i:i + word_lenght])
        if i == cipherLetters.__len__() - word_lenght:
            i = 0
            word_lenght += 1
        arr_index += 1
        if word_lenght > 5:
            break

    for i in range(my_search_word.__len__()):
        index_arr.append([])
        str = my_search_word[i]
        myindex = cipherLetters.find(str)
        while myindex != -1:
            index_arr[i].append(myindex)
            myindex += 1
            myindex = cipherLetters.find(str, myindex)
    # for i in range(index_arr.__len__()):
    #     if index_arr[i] == -1:
    #         continue
    #     for j in range(index_arr[i].__len__() - 1):
    #         index_arr[index_arr[i][j + 1]] = -1
    # for i in range(index_arr.__len__()):
    #     if index_arr[i] == -1:
    #         continue
    #     if index_arr[i].__len__() == 1:
    #         index_arr[i][0] = -1
    wrd = 0
    for i in range(index_arr.__len__()):
        if index_arr[i] != -1:
            my_dif_arr.append([])
            my_wrd_arr.append(my_search_word[i])
            for z in range(index_arr[i].__len__() - 1):
                ind1 = index_arr[i][z]
                ind2 = index_arr[i][z + 1]
                diff = ind2 - ind1
                my_dif_arr[wrd].append(diff)
            wrd += 1

    for i in range(my_wrd_arr.__len__()):
        if my_wrd_arr[i] != -1:
            if my_dif_arr[i].__len__() != 0:
                my_final_diff.append(my_dif_arr[i])
    # print my_final_diff
    my_factor = []
    for j in range(my_final_diff.__len__()):
        for k in range(my_final_diff[j].__len__()):
            num = my_final_diff[j][k]
            c_num = 20
            if num > 20:
                c_num = num
            for i in range(2, c_num):
                if num % i == 0:
                    try:
                        my_factor[i] += 1
                    except IndexError:
                        for _ in range (i - len(my_factor) + 1):
                            my_factor.append(0)
                        my_factor[i] += 1
    print my_factor
    first_max = max(my_factor)
    first_max_i = my_factor.index(first_max)
    current_i = first_max_i
    i = 2
    prev_max = first_max
    next_max = sorted(my_factor)[-i]
    next_max_i = my_factor.index(next_max)
    while i != -1:
        if float(next_max) / float(prev_max) >= 0.8 and (next_max_i > current_i or float(next_max) / float(prev_max) >= 0.95):
            i += 1
            current_i = next_max_i
            prev_max = next_max
            next_max = sorted(my_factor)[-i]
            next_max_i = my_factor.index(next_max)
        else:
            i = -1
    print current_i
    sorted_indexes = []
    sorted_indexes.append(current_i)
    sorted_indexes.append(first_max_i)
    prev_max = first_max
    prev_max_i = first_max_i
    for i in range(2, len(my_factor)):
        next_max = sorted(my_factor)[-i]
        next_max_i = my_factor.index(next_max)
        print next_max
        print prev_max
        if float(next_max) / float(prev_max) >= 0.5 and (next_max_i > prev_max_i or float(next_max) / float(prev_max) >= 0.95):
            prev_max = next_max
            prev_max_i = next_max_i
            sorted_indexes.append(next_max_i)
        else:
            break
    print sorted_indexes
    if sorted_indexes[0] == sorted_indexes[-1]:
        print [sorted_indexes[0]]
        return [sorted_indexes[0]]
    else:
        print sorted_indexes[1:sorted_indexes.__len__()]
        return sorted_indexes[1:sorted_indexes.__len__()]

def deleteChangeBadSymbols(text):
    text = re.sub(patternQuots, '', text)
    text = re.sub(patternNewLine, ' ', text)
    return text


def cipher(text, key):
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

    # print(text)
    print(cipherText)
    return cipherText

def calculateLettersRate(cipher, keyLen):
    print cipher
    cipherLetters = u""
    for i in range(cipher.__len__()):
         if pattern.match(cipher[i]):
             cipherLetters += cipher[i]


    print cipherLetters
    lettersCount = []
    for j in range(keyLen):
        lettersCount.append({})
        for i in range(ord('A'), ord('Z') + 1, 1):
            lettersCount[j][chr(i)] = 0



    for i in range(cipherLetters.__len__()):
        lettersCount[i % keyLen][cipherLetters[i]] += 1
        # print(cipherLetters[i])
        # print i

    print(lettersCount)
    lettersRate =  []
    for i in range(keyLen):
        temp = sorted(lettersCount[i], key=lettersCount[i].__getitem__, reverse=True)
        letters = u""
        for i in range(len(temp)):
            letters += temp[i]
        lettersRate.append(letters)

    return lettersRate