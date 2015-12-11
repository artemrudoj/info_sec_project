#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import enchant
d = enchant.Dict("en_US")
# >>> d.check("Hello")
# True
# >>> d.check("Helo")
# False
# >>> d.suggest("Helo")
# ['He lo', 'He-lo', 'Hello', 'Helot', 'Help', 'Halo', 'Hell', 'Held', 'Helm', 'Hero', "He'll"]
# >>>А
pattern = re.compile("([A-Z])")

# this is letter frequency in usual english
usualEnglishLettersRate = u"etaoinshrdlcumwfgypbvkjxqz"
usualEnglishLettersRate = usualEnglishLettersRate.upper()



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
            print i
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
    # print my_factor
    first_max = max(my_factor)
    current_i = my_factor.index(first_max)
    i = 2
    prev_max = first_max
    next_max = sorted(my_factor)[-i]
    next_max_i = my_factor.index(next_max)
    while i != -1:
        if float(next_max) / float(prev_max) >= 0.8 and next_max_i > current_i:
            i += 1
            current_i = next_max_i
            prev_max = next_max
            next_max = sorted(my_factor)[-i]
            next_max_i = my_factor.index(next_max)
        else:
            i = -1
    # print current_i
    return current_i