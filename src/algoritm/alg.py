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


# вот эту фигню варьировать
N = 4
frequentAnalysisError = 4

l = []
nods = []
for i in range(1000):
    nods.append(0)
    l.append(0)
nl = 0

print l




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
    print mappingFunctioonsFuckOrd
    return mappingFunctioons

def correctingOfFunction(mappingFunctioons, keyLen, arrayOfLetters):
    letter = ""
    valueExch = ""
    keyExch = ""
    for i in range(keyLen):
        for key, value in mappingFunctioons[i].iteritems():
            if key in arrayOfLetters:
                valueExch = value
                newValue = foundKeyByVale(mappingFunctioons[i], value)


    pass

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

def secondPopularLettersWord(text, alreadyknowingMapping, arrayOfletters, begin, end, englishLetters, keyLen):
    shortArrayOfLetters = []
    forLetterE = []
    for j in range(keyLen):
        shortArrayOfLetters.append(arrayOfletters[j][begin:end])
    decoder = Decoder(shortArrayOfLetters, keyLen, englishLetters, alreadyknowingMapping)
    for word in text.split():
        decoder.isCorrectWord(word, alreadyknowingMapping)
    return  decoder.decodeConfirmWords()

class Decoder:
    newInglishLetter = []
    keyLen = 0
    mappingsFunction = []
    mappings = []
    confirmWords = []
    currentIndex = 0
    alreadyKnowingLetters = []
    correctMapFunction = []
    def __init__(self, shortArrayOfLetters, keyLen, newInglishLetter, alreadyKnowingLetters):
        self.currentIndex = 0
        self.mappings = shortArrayOfLetters
        self.confirmWords = {}
        self.keyLen = keyLen
        self.newInglishLetter = newInglishLetter
        self.alreadyKnowingLetters = alreadyKnowingLetters
    def isCorrectWord(self, word, additionalsLetters):
        tmp = self.currentIndex
        countAdditionalLetters = 0
        isOneLetterFromRequired = False
        isCorrect = True
        minRequredLetters = 3
        for i in range(word.__len__()):
            if ord(word[i]) in range(ord('A'), ord('Z') + 1, 1):
                if isCorrect:
                    if word[i] in self.mappings[self.currentIndex % self.keyLen]:
                        countAdditionalLetters = countAdditionalLetters + 1
                        if countAdditionalLetters > minRequredLetters:
                            isOneLetterFromRequired = True
                    else :
                        isCorrect = False
                    if ord(word[i]) in additionalsLetters[self.currentIndex % self.keyLen].keys():
                        isCorrect = True
                self.currentIndex = self.currentIndex + 1
            else:
                isCorrect = False
        if isCorrect and isOneLetterFromRequired:
            self.confirmWords.update({word:tmp})
            return True
        else:
            return False

    #нужно сделать поумнее
    def decodeConfirmWords(self):
        countOfDecodeWords = 0
        countOfTryedWords = 0
        bijection = BijectionOfAlphabet(self.keyLen, self.newInglishLetter, self.mappings, self.alreadyKnowingLetters)
        print "keylen" + str(self.keyLen)
        print "count of confirm words: " + str(len(self.confirmWords))
        print self.confirmWords
        while(True):
            mappingFunctions = bijection.generateMappingFunctions()
            if (bijection.iterator.isFinished == True):
                break
            for word, position in self.confirmWords.iteritems():
                decodedWord = self.decodeWord(word, position, mappingFunctions)
                if self.checkWord(decodedWord):
                    countOfDecodeWords = countOfDecodeWords + 1
                countOfTryedWords = countOfTryedWords + 1
                ret = self.isShouldStop(countOfDecodeWords, countOfTryedWords)
                if (ret == 0):
                    break
                elif (ret == 1):
                    print bijection.iterator.indexesForMappingFunction
                    print 'bla bla bla'
                    self.correctMapFunction = bijection.iterator.indexesForMappingFunction
                    return mappingFunctions
            countOfTryedWords = 0
            countOfDecodeWords = 0
        return mappingFunctions


    def isShouldStop(self, countOfDecodeWords, countOfTryedWords):
        countOfAllWords = len(self.confirmWords)
        rate = float(countOfTryedWords)/float(countOfAllWords)
        # Нужно подгонять эти штуки
        if (rate) < 0.3:
            return -1
        else:
            rate = float(countOfDecodeWords)/float(countOfTryedWords)
            if (rate) < 0.5:
                return 0
            elif (rate) > 0.9:
                print rate
                print self.confirmWords
                return 1
            else:
                return -1


    def decodeWord(self, word, position, bijection):
        decodeWord = ""
        for letter in word:
            #получаю нужную букву из нужного столбца преобразования
            index = position % self.keyLen
            decodeLetter = bijection[index].get(ord(letter))
            decodeWord = decodeWord + decodeLetter
            position = position + 1
        return decodeWord

    def checkWord(self, word):
        if d.check(word):
            return True
        return False

class BijectionOfAlphabet:
    keyLen = 0
    currentStateOfAllMappingFunctions = []
    iterator = []
    allCombinationOfEnglishLetters = []
    mappings = []
    alreadyKnowingLetters = []
    def __init__(self, keyLen, englishLetters, mappings, alreadyKnowingLetters):
        self.currentStateOfAllMappingFunctions = [None] * keyLen
        self.keyLen = keyLen
        self.allCombinationOfEnglishLetters = list(itertools.permutations(englishLetters))
        #чтобы охватить все комбинации тут нужно что-нибудь придумать!!! а то дофига раз придется итерироваться
        self.iterator = BossOfAllIterators(keyLen, len(self.allCombinationOfEnglishLetters))
        self.mappings = mappings
        self.alreadyKnowingLetters = alreadyKnowingLetters

        print "in BijectionOfAlphabet alreadyKnowingLetters" + str(alreadyKnowingLetters)
        print "in BijectionOfAlphabet " + str(self.alreadyKnowingLetters)
        print "Bijection vreated"

    def generateMappingFunctions(self):
        arrayOfIndexes = self.iterator.indexesForMappingFunction
        if (self.iterator.isFinished == True):
            return self.currentStateOfAllMappingFunctions
        for i in range(self.keyLen):
            map = zip(self.mappings[i], self.allCombinationOfEnglishLetters[arrayOfIndexes[i]])
            self.currentStateOfAllMappingFunctions[i] = fromListToMap(map)
            if (self.alreadyKnowingLetters != None):
                self.currentStateOfAllMappingFunctions[i].update(self.alreadyKnowingLetters[i])
        self.iterator.iterate()
        return self.currentStateOfAllMappingFunctions

class BossOfAllIterators:
    indexesForMappingFunction = []
    keyLen = 0
    arrayLengths = 0
    isFinished = False
    def __init__(self, keyLen, arrayLength):
        self.keyLen = keyLen
        self.indexesForMappingFunction = [0]*self.keyLen
        self.arrayLengths = arrayLength
    #итерируемся начиная из самого последнего массива
    def iterate(self):
        if (self.indexesForMappingFunction[self.keyLen - 1] == (self.arrayLengths - 1)):
            self.isFinished = True
            return None
        self.indexesForMappingFunction[0] = self.indexesForMappingFunction[0] + 1
        for i in range(self.keyLen - 1):
            if self.indexesForMappingFunction[i] == self.arrayLengths - 1:
                self.indexesForMappingFunction[i + 1] = self.indexesForMappingFunction[i + 1] + 1
                self.indexesForMappingFunction[i] = 0
        return self.indexesForMappingFunction

def isCorrectWordWithRequired(word, arrayOfLetters, requiredLetters):
    HaveRequredLettersCount = 0
    if (len(word) > 4):
        return False
    for letter in word:
        if letter in arrayOfLetters:
            if letter in requiredLetters:
                HaveRequredLettersCount = HaveRequredLettersCount + 1
            continue
        else:
            return False
    if (HaveRequredLettersCount >= 2):
        return True
    else:
        return False


def checkFullnessOfLettersArray(newLettersRate, confirmWords):
    array = "".join(confirmWords)
    array2 = ''.join(sorted(array))
    newarray = ''.join(OrderedDict.fromkeys(array2))
    array = "".join(newLettersRate)
    newarray2 = ''.join(sorted(array))
    newarray3 = ''.join(OrderedDict.fromkeys(newarray2))
    print "old:"
    print newarray
    print "new:"
    print newarray3


def fromListToMap(map):
    newMap  = {}
    for a in map:
        indx = ord(a[0])
        newMap[indx] = a[1]
    return newMap

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

def isCorrectWord(word, letters):
    for letter in word:
        if letter in letters:
            continue
        else:
            return False
    return True

# returns true if  currenIndex lessthan endIndex and false otherwise
def compareComplexIndexes(currentIndex, endIndex):
    for i in range(len(currentIndex)):
        if currentIndex[i] > endIndex[i]:
            return False

    return True



def increaseComplexIndex(currentIndex, endIndex, permanentIndex):
    firstVarLetterIndex = -1
    for i in range(len(permanentIndex)):
        if permanentIndex[i] == -1:
            firstVarLetterIndex = i
            break


    if firstVarLetterIndex == -1:
        currentIndex = endIndex[:]
        currentIndex[0] = endIndex[0] + 1
        return currentIndex
    else:
        secondVarLetterIndex = permanentIndex.__len__() - 1
        for i in range(firstVarLetterIndex + 1, len(permanentIndex)):
             if permanentIndex[i] == -1:
                secondVarLetterIndex = i
                break

    currentIndex[secondVarLetterIndex] += 1

    for i in range(len(currentIndex) - 1):
        if currentIndex[i] > endIndex[i]:
            currentIndex[i] -= 2 * frequentAnalysisError - 1
            if currentIndex[i] < 0:
                currentIndex[i] = 0
            # currentIndex[i + 1] += 1
            for j in range(i + 1, permanentIndex.__len__()):
                if permanentIndex[j] == -1:
                    currentIndex[j] += 1
                    break
    return currentIndex



if __name__ == '__main__':
    sourceTextForCipher3 ="HE STOPPED TO DINNER THAT EVENING, AND, MUCH TO RUTH’S SATISFACTION, MADE A FAVORABLE IMPRESSION ON HER FATHER. THEY TALKED ABOUT THE SEA AS A CAREER, A SUBJECT WHICH MARTIN HAD AT HIS FINGER-ENDS, AND MR. MORSE REMARKED AFTERWARD THAT HE SEEMED A VERY CLEAR-HEADED YOUNG MAN. IN HIS AVOIDANCE OF SLANG AND HIS SEARCH AFTER RIGHT WORDS, MARTIN WAS COMPELLED TO TALK SLOWLY, WHICH ENABLED HIM TO FIND THE BEST THOUGHTS THAT WERE IN HIM. HE WAS MORE AT EASE THAN THAT FIRST NIGHT AT DINNER, NEARLY A YEAR BEFORE, AND HIS SHYNESS AND MODESTY EVEN COMMENDED HIM TO MRS. MORSE, WHO WAS PLEASED AT HIS MANIFEST IMPROVEMENT. HE IS THE FIRST MAN THAT EVER DREW PASSING NOTICE FROM RUTH,SHE TOLD HER HUSBAND. SHE HAS BEEN SO SINGULARLY BACKWARD WHERE MEN ARE CONCERNED THAT I HAVE BEEN WORRIED GREATLY.  MR. MORSE LOOKED AT HIS WIFE CURIOUSLY.   YOU MEAN TO USE THIS YOUNG SAILOR TO WAKE HER UP? HE QUESTIONED.   I MEAN THAT SHE IS NOT TO DIE AN OLD MAID IF I CAN HELP IT, WAS THE ANSWER. IF THIS YOUNG EDEN CAN AROUSE HER INTEREST IN MANKIND IN GENERAL, IT WILL BE A GOOD THING.   A VERY GOOD THING, HE COMMENTED. BUT SUPPOSE,-AND WE MUST SUPPOSE, SOMETIMES, MY DEAR,-SUPPOSE HE AROUSES HER INTEREST TOO PARTICULARLY IN HIM? IMPOSSIBLE, MRS. MORSE LAUGHED. SHE IS THREE YEARS OLDER THAN HE, AND, BESIDES, IT IS IMPOSSIBLE. NOTHING WILL EVER COME OF IT. TRUST THAT TO ME.   AND SO MARTIN’S  WAS ARRANGED FOR HIM, WHILE HE, LED ON BY ARTHUR AND NORMAN, WAS MEDITATING AN EXTRAVAGANCE. THEY WERE GOING OUT FOR A RIDE INTO THE HILLS SUNDAY MORNING ON THEIR WHEELS, WHICH DID NOT INTEREST MARTIN UNTIL HE LEARNED THAT RUTH, TOO, RODE A WHEEL AND WAS GOING ALONG. HE DID NOT RIDE, NOR OWN A WHEEL, BUT IF RUTH RODE, IT WAS UP TO HIM TO BEGIN, WAS HIS DECISION; AND WHEN HE SAID GOOD NIGHT, HE STOPPED IN AT A CYCLERY ON HIS WAY HOME AND SPENT FORTY DOLLARS FOR A WHEEL. IT WAS MORE THAN A MONTH’S HARD-EARNED WAGES, AND IT REDUCED HIS STOCK OF MONEY AMAZINGLY; BUT WHEN HE ADDED THE HUNDRED DOLLARS HE WAS TO RECEIVE FROM THE EXAMINER TO THE FOUR HUNDRED AND TWENTY DOLLARS THAT WAS THE LEAST THE YOUTH’S COMPANION COULD PAY HIM, HE FELT THAT HE HAD REDUCED THE PERPLEXITY THE UNWONTED AMOUNT OF MONEY HAD CAUSED HIM. NOR DID HE MIND, IN THE COURSE OF LEARNING TO RIDE THE WHEEL HOME, THE FACT THAT HE RUINED HIS SUIT OF CLOTHES. HE CAUGHT THE TAILOR BY TELEPHONE THAT NIGHT FROM MR. HIGGINBOTHAM’S STORE AND ORDERED ANOTHER SUIT. THEN HE CARRIED THE WHEEL UP THE NARROW STAIRWAY THAT CLUNG LIKE A FIRE-ESCAPE TO THE REAR WALL OF THE BUILDING, AND WHEN HE HAD MOVED HIS BED OUT FROM THE WALL, FOUND THERE WAS JUST SPACE ENOUGH IN THE SMALL ROOM FOR HIMSELF AND THE WHEEL.   SUNDAY HE HAD INTENDED TO DEVOTE TO STUDYING FOR THE HIGH SCHOOL EXAMINATION, BUT THE PEARL-DIVING ARTICLE LURED HIM AWAY, AND HE SPENT THE DAY IN THE WHITE-HOT FEVER OF RE-CREATING THE BEAUTY AND ROMANCE THAT BURNED IN HIM. THE FACT THAT THE EXAMINER OF THAT MORNING HAD FAILED TO PUBLISH HIS TREASURE-HUNTING ARTICLE DID NOT DASH HIS SPIRITS. HE WAS AT TOO GREAT A HEIGHT FOR THAT, AND HAVING BEEN DEAF TO A TWICE-REPEATED SUMMONS, HE WENT WITHOUT THE HEAVY SUNDAY DINNER WITH WHICH MR. HIGGINBOTHAM INVARIABLY GRACED HIS TABLE. TO MR. HIGGINBOTHAM SUCH A DINNER WAS ADVERTISEMENT OF HIS WORLDLY ACHIEVEMENT AND PROSPERITY, AND HE HONORED IT BY DELIVERING PLATITUDINOUS SERMONETTES UPON AMERICAN INSTITUTIONS AND THE OPPORTUNITY SAID INSTITUTIONS GAVE TO ANY HARD-WORKING MAN TO RISE-THE RISE, IN HIS CASE, WHICH HE POINTED OUT UNFAILINGLY, BEING FROM A GROCER’S CLERK TO THE OWNERSHIP OF HIGGINBOTHAM’S CASH STORE.   MARTIN EDEN LOOKED WITH A SIGH AT HIS UNFINISHED PEARL-DIVING ON MONDAY MORNING, AND TOOK THE CAR DOWN TO OAKLAND TO THE HIGH SCHOOL. AND WHEN, DAYS LATER, HE APPLIED FOR THE RESULTS OF HIS EXAMINATIONS, HE LEARNED THAT HE HAD FAILED IN EVERYTHING SAVE GRAMMAR.   YOUR GRAMMAR IS EXCELLENT, PROFESSOR HILTON INFORMED HIM, STARING AT HIM THROUGH HEAVY SPECTACLES; BUT YOU KNOW NOTHING, POSITIVELY NOTHING, IN THE OTHER BRANCHES, AND YOUR UNITED STATES HISTORY IS ABOMINABLE-THERE IS NO OTHER WORD FOR IT, ABOMINABLE. I SHOULD ADVISE YOU-  PROFESSOR HILTON PAUSED AND GLARED AT HIM, UNSYMPATHETIC AND UNIMAGINATIVE AS ONE OF HIS OWN TEST-TUBES. HE WAS PROFESSOR OF PHYSICS IN THE HIGH SCHOOL, POSSESSOR OF A LARGE FAMILY, A MEAGRE SALARY, AND A SELECT FUND OF PARROT-LEARNED KNOWLEDGE.   YES, SIR, MARTIN SAID HUMBLY, WISHING SOMEHOW THAT THE MAN AT THE DESK IN THE LIBRARY WAS IN PROFESSOR HILTON’S PLACE JUST THEN.   AND I SHOULD ADVISE YOU TO GO BACK TO THE GRAMMAR SCHOOL FOR AT LEAST TWO YEARS. GOOD DAY.   MARTIN WAS NOT DEEPLY AFFECTED BY HIS FAILURE, THOUGH HE WAS SURPRISED AT RUTH’S SHOCKED EXPRESSION WHEN HE TOLD HER PROFESSOR HILTON’S ADVICE. HER DISAPPOINTMENT WAS SO EVIDENT THAT HE WAS SORRY HE HAD FAILED, BUT CHIEFLY SO FOR HER SAKE.   YOU SEE I WAS RIGHT, SHE SAID. YOU KNOW FAR MORE THAN ANY OF THE STUDENTS ENTERING HIGH SCHOOL, AND YET YOU CAN’T PASS THE EXAMINATIONS. IT IS BECAUSE WHAT EDUCATION YOU HAVE IS FRAGMENTARY, SKETCHY. YOU NEED THE DISCIPLINE OF STUDY, SUCH AS ONLY SKILLED TEACHERS CAN GIVE YOU. YOU MUST BE THOROUGHLY GROUNDED. PROFESSOR HILTON IS RIGHT, AND IF I WERE YOU, I’D GO TO NIGHT SCHOOL. A YEAR AND A HALF OF IT MIGHT ENABLE YOU TO CATCH UP THAT ADDITIONAL SIX MONTHS. BESIDES, THAT WOULD LEAVE YOU YOUR DAYS IN WHICH TO WRITE, OR, IF YOU COULD NOT MAKE YOUR LIVING BY YOUR PEN, YOU WOULD HAVE YOUR DAYS IN WHICH TO WORK IN SOME POSITION.   BUT IF MY DAYS ARE TAKEN UP WITH WORK AND MY NIGHTS WITH SCHOOL, WHEN AM I GOING TO SEE YOU?-WAS MARTIN’S FIRST THOUGHT, THOUGH HE REFRAINED FROM UTTERING IT. INSTEAD, HE SAID:-   IT SEEMS SO BABYISH FOR ME TO BE GOING TO NIGHT SCHOOL. BUT I WOULDN’T MIND THAT IF I THOUGHT IT WOULD PAY. BUT I DON’T THINK IT WILL PAY. I CAN DO THE WORK QUICKER THAN THEY CAN TEACH ME. IT WOULD BE A LOSS OF TIME- HE THOUGHT OF HER AND HIS DESIRE TO HAVE HER-AND I CAN’T AFFORD THE TIME. I HAVEN’T THE TIME TO SPARE, IN FACT.   THERE IS SO MUCH THAT IS NECESSARY. SHE LOOKED AT HIM GENTLY, AND HE WAS A BRUTE TO OPPOSE HER. PHYSICS AND CHEMISTRY-YOU CAN’T DO THEM WITHOUT LABORATORY STUDY; AND YOU’LL FIND ALGEBRA AND GEOMETRY ALMOST HOPELESS WITH INSTRUCTION. YOU NEED THE SKILLED TEACHERS, THE SPECIALISTS IN THE ART OF IMPARTING KNOWLEDGE.   HE WAS SILENT FOR A MINUTE, CASTING ABOUT FOR THE LEAST VAINGLORIOUS WAY IN WHICH TO EXPRESS HIMSELF.   PLEASE DON’T THINK I’M BRAGGING, HE BEGAN. I DON’T INTEND IT THAT WAY AT ALL. BUT I HAVE A FEELING THAT I AM WHAT I MAY CALL A NATURAL STUDENT. I CAN STUDY BY MYSELF. I TAKE TO IT KINDLY, LIKE A DUCK TO WATER. YOU SEE YOURSELF WHAT I DID WITH GRAMMAR. AND I’VE LEARNED MUCH OF OTHER THINGS-YOU WOULD NEVER DREAM HOW MUCH. AND I’M ONLY GETTING STARTED. WAIT TILL I GET- HE HESITATED AND ASSURED HIMSELF OF THE PRONUNCIATION BEFORE HE SAID MOMENTUM. I’M GETTING MY FIRST REAL FEEL OF THINGS NOW. I’M BEGINNING TO SIZE UP THE SITUATION-   PLEASE DON’T SAY ‘SIZE UP,’ SHE INTERRUPTED.   TO GET A LINE ON THINGS, HE HASTILY AMENDED.   THAT DOESN’T MEAN ANYTHING IN CORRECT ENGLISH, SHE OBJECTED.   HE FLOUNDERED FOR A FRESH START. WHAT I’M DRIVING AT IS THAT I’M BEGINNING TO GET THE LAY OF THE LAND   OUT OF PITY SHE FOREBORE, AND HE WENT ON.   KNOWLEDGE SEEMS TO ME LIKE A CHART-ROOM. WHENEVER I GO INTO THE LIBRARY, I AM IMPRESSED THAT WAY. THE PART PLAYED BY TEACHERS IS TO TEACH THE STUDENT THE CONTENTS OF THE CHART-ROOM IN A SYSTEMATIC WAY. THE TEACHERS ARE GUIDES TO THE CHART-ROOM, THAT’S ALL. IT’S NOT SOMETHING THAT THEY HAVE IN THEIR OWN HEADS. THEY DON’T MAKE IT UP, DON’T CREATE IT. IT’S ALL IN THE CHART-ROOM AND THEY KNOW THEIR WAY ABOUT IN IT, AND IT’S THEIR BUSINESS TO SHOW THE PLACE TO STRANGERS WHO MIGHT ELSE GET LOST. NOW I DON’T GET LOST EASILY. I HAVE THE BUMP OF LOCATION. I USUALLY KNOW WHERE I’M AT-WHAT’S WRONG NOW?   DON’T SAY ‘WHERE I’M AT.’   THAT’S RIGHT, HE SAID GRATEFULLY, WHERE I AM. BUT WHERE AM I AT-I MEAN, WHERE AM I? OH, YES, IN THE CHART-ROOM. WELL, SOME PEOPLE-   PERSONS, SHE CORRECTED.   SOME PERSONS NEED GUIDES, MOST PERSONS DO; BUT I THINK I CAN GET ALONG WITHOUT THEM. I’VE SPENT A LOT OF TIME IN THE CHART-ROOM NOW, AND I’M ON THE EDGE OF KNOWING MY WAY ABOUT, WHAT CHARTS I WANT TO REFER TO, WHAT COASTS I WANT TO EXPLORE. AND FROM THE WAY I LINE IT UP, I’LL EXPLORE A WHOLE LOT MORE QUICKLY BY MYSELF. THE SPEED OF A FLEET, YOU KNOW, IS THE SPEED OF THE SLOWEST SHIP, AND THE SPEED OF THE TEACHERS IS AFFECTED THE SAME WAY. THEY CAN’T GO ANY FASTER THAN THE RUCK OF THEIR SCHOLARS, AND I CAN SET A FASTER PACE FOR MYSELF THAN THEY SET FOR A WHOLE SCHOOLROOM.   ‘HE TRAVELS THE FASTEST WHO TRAVELS ALONE,’ SHE QUOTED AT HIM.   BUT I’D TRAVEL FASTER WITH YOU JUST THE SAME, WAS WHAT HE WANTED TO BLURT OUT, AS HE CAUGHT A VISION OF A WORLD WITHOUT END OF SUNLIT SPACES AND STARRY VOIDS THROUGH WHICH HE DRIFTED WITH HER, HIS ARM AROUND HER, HER PALE GOLD HAIR BLOWING ABOUT HIS FACE. IN THE SAME INSTANT HE WAS AWARE OF THE PITIFUL INADEQUACY OF SPEECH. GOD! IF HE COULD SO FRAME WORDS THAT SHE COULD SEE WHAT HE THEN SAW! AND HE FELT THE STIR IN HIM, LIKE A THROE OF YEARNING PAIN, OF THE DESIRE TO PAINT THESE VISIONS THAT FLASHED UNSUMMONED ON THE MIRROR OF HIS MIND. AH, THAT WAS IT! HE CAUGHT AT THE HEM OF THE SECRET. IT WAS THE VERY THING THAT THE GREAT WRITERS AND MASTER-POETS DID. THAT WAS WHY THEY WERE GIANTS. THEY KNEW HOW TO EXPRESS WHAT THEY THOUGHT, AND FELT, AND SAW. DOGS ASLEEP IN THE SUN OFTEN WHINED AND BARKED, BUT THEY WERE UNABLE TO TELL WHAT THEY SAW THAT MADE THEM WHINE AND BARK. HE HAD OFTEN WONDERED WHAT IT WAS. AND THAT WAS ALL HE WAS, A DOG ASLEEP IN THE SUN. HE SAW NOBLE AND BEAUTIFUL VISIONS, BUT HE COULD ONLY WHINE AND BARK AT RUTH. BUT HE WOULD CEASE SLEEPING IN THE SUN. HE WOULD STAND UP, WITH OPEN EYES, AND HE WOULD STRUGGLE AND TOIL AND LEARN UNTIL, WITH EYES UNBLINDED AND TONGUE UNTIED, HE COULD SHARE WITH HER HIS VISIONED WEALTH. OTHER MEN HAD DISCOVERED THE TRICK OF EXPRESSION, OF MAKING WORDS OBEDIENT SERVITORS, AND OF MAKING COMBINATIONS OF WORDS MEAN MORE THAN THE SUM OF THEIR SEPARATE MEANINGS. HE WAS STIRRED PROFOUNDLY BY THE PASSING GLIMPSE AT THE SECRET, AND HE WAS AGAIN CAUGHT UP IN THE VISION OF SUNLIT SPACES AND STARRY VOIDS-UNTIL IT CAME TO HIM THAT IT WAS VERY QUIET, AND HE SAW RUTH REGARDING HIM WITH AN AMUSED EXPRESSION AND A SMILE IN HER EYES.   I HAVE HAD A GREAT VISIONING, HE SAID, AND AT THE SOUND OF HIS WORDS IN HIS OWN EARS HIS HEART GAVE A LEAP. WHERE HAD THOSE WORDS COME FROM? THEY HAD ADEQUATELY EXPRESSED THE PAUSE HIS VISION HAD PUT IN THE CONVERSATION. IT WAS A MIRACLE. NEVER HAD HE SO LOFTILY FRAMED A LOFTY THOUGHT. BUT NEVER HAD HE ATTEMPTED TO FRAME LOFTY THOUGHTS IN WORDS. THAT WAS IT. THAT EXPLAINED IT. HE HAD NEVER TRIED. BUT SWINBURNE HAD, AND TENNYSON, AND KIPLING, AND ALL THE OTHER POETS. HIS MIND FLASHED ON TO HIS PEARL-DIVING. HE HAD NEVER DARED THE BIG THINGS, THE SPIRIT OF THE BEAUTY THAT WAS A FIRE IN HIM. THAT ARTICLE WOULD BE A DIFFERENT THING WHEN HE WAS DONE WITH IT. HE WAS APPALLED BY THE VASTNESS OF THE BEAUTY THAT RIGHTFULLY BELONGED IN IT, AND AGAIN HIS MIND FLASHED AND DARED, AND HE DEMANDED OF HIMSELF WHY HE COULD NOT CHANT THAT BEAUTY IN NOBLE VERSE AS THE GREAT POETS DID. AND THERE WAS ALL THE MYSTERIOUS DELIGHT AND SPIRITUAL WONDER OF HIS LOVE FOR RUTH. WHY COULD HE NOT CHANT THAT, TOO, AS THE POETS DID? THEY HAD SUNG OF LOVE. SO WOULD HE. BY GOD!-   AND IN HIS FRIGHTENED EARS HE HEARD HIS EXCLAMATION ECHOING. CARRIED AWAY, HE HAD BREATHED IT ALOUD. THE BLOOD SURGED INTO HIS FACE, WAVE UPON WAVE, MASTERING THE BRONZE OF IT TILL THE BLUSH OF SHAME FLAUNTED ITSELF FROM COLLAR-RIM TO THE ROOTS OF HIS HAIR.   I– I-BEG YOUR PARDON, HE STAMMERED. I WAS THINKING.   IT SOUNDED AS IF YOU WERE PRAYING, SHE SAID BRAVELY, BUT SHE FELT HERSELF INSIDE TO BE WITHERING AND SHRINKING. IT WAS THE FIRST TIME SHE HAD HEARD AN OATH FROM THE LIPS OF A MAN SHE KNEW, AND SHE WAS SHOCKED, NOT MERELY AS A MATTER OF PRINCIPLE AND TRAINING, BUT SHOCKED IN SPIRIT BY THIS ROUGH BLAST OF LIFE IN THE GARDEN OF HER SHELTERED MAIDENHOOD.   BUT SHE FORGAVE, AND WITH SURPRISE AT THE EASE OF HER FORGIVENESS. SOMEHOW IT WAS NOT SO DIFFICULT TO FORGIVE HIM ANYTHING. HE HAD NOT HAD A CHANCE TO BE AS OTHER MEN, AND HE WAS TRYING SO HARD, AND SUCCEEDING, TOO. IT NEVER ENTERED HER HEAD THAT THERE COULD BE ANY OTHER REASON FOR HER BEING KINDLY DISPOSED TOWARD HIM. SHE WAS TENDERLY DISPOSED TOWARD HIM, BUT SHE DID NOT KNOW IT. SHE HAD NO WAY OF KNOWING IT. THE PLACID POISE OF TWENTY-FOUR YEARS WITHOUT A SINGLE LOVE AFFAIR DID NOT FIT HER WITH A KEEN PERCEPTION OF HER OWN FEELINGS, AND SHE WHO HAD NEVER WARMED TO ACTUAL LOVE WAS UNAWARE THAT SHE WAS WARMING NOW."
    sourceText = u"SCROOGE WAS BETTER THAN HIS WORD. HE DID IT ALL, AND INFINITELY MORE; AND TO TINY TIM, WHO DID NOT DIE, HE WAS A SECOND FATHER. HE BECAME AS GOOD A FRIEND, AS GOOD A MASTER, AND AS GOOD A MAN, AS THE GOOD OLD CITY KNEW, OR ANY OTHER GOOD OLD CITY, TOWN, OR BOROUGH, IN THE GOOD OLD WORLD. SOME PEOPLE LAUGHED TO SEE THE ALTERATION IN HIM, BUT HE LET THEM LAUGH, AND LITTLE HEEDED THEM; FOR HE WAS WISE ENOUGH TO KNOW THAT NOTHING EVER HAPPENED ON THIS GLOBE, FOR GOOD, AT WHICH SOME PEOPLE DID NOT HAVE THEIR FILL OF LAUGHTER IN THE OUTSET; AND KNOWING THAT SUCH AS THESE WOULD BE BLIND ANYWAY, HE THOUGHT IT QUITE AS WELL THAT THEY SHOULD WRINKLE UP THEIR EYES IN GRINS, AS HAVE THE MALADY IN LESS ATTRACTIVE FORMS. HIS OWN HEART LAUGHED: AND THAT WAS QUITE ENOUGH FOR HIM. HE HAD NO FURTHER INTERCOURSE WITH SPIRITS, BUT LIVED UPON THE TOTAL ABSTINENCE PRINCIPLE, EVER AFTERWARDS; AND IT WAS ALWAYS SAID OF HIM, THAT HE KNEW HOW TO KEEP CHRISTMAS WELL, IF ANY MAN ALIVE POSSESSED THE KNOWLEDGE. MAY THAT BE TRULY SAID OF US, AND ALL OF US! AND SO, AS TINY TIM OBSERVED, GOD BLESS US, EVERY ONE!"
    cipher3 = u"JG UVQRRGF VQ FKPPGT VJCV GXGPKPI, CPF, OWEJ VQ TWVJ’U UCVKUHCEVKQP, OCFG C HCXQTCDNG KORTGUUKQP QP JGT HCVJGT. VJGA VCNMGF CDQWV VJG UGC CU C ECTGGT, C UWDLGEV YJKEJ OCTVKP JCF CV JKU HKPIGT-GPFU, CPF OT. OQTUG TGOCTMGF CHVGTYCTF VJCV JG UGGOGF C XGTA ENGCT-JGCFGF AQWPI OCP. KP JKU CXQKFCPEG QH UNCPI CPF JKU UGCTEJ CHVGT TKIJV YQTFU, OCTVKP YCU EQORGNNGF VQ VCNM UNQYNA, YJKEJ GPCDNGF JKO VQ HKPF VJG DGUV VJQWIJVU VJCV YGTG KP JKO. JG YCU OQTG CV GCUG VJCP VJCV HKTUV PKIJV CV FKPPGT, PGCTNA C AGCT DGHQTG, CPF JKU UJAPGUU CPF OQFGUVA GXGP EQOOGPFGF JKO VQ OTU. OQTUG, YJQ YCU RNGCUGF CV JKU OCPKHGUV KORTQXGOGPV. JG KU VJG HKTUV OCP VJCV GXGT FTGY RCUUKPI PQVKEG HTQO TWVJ,UJG VQNF JGT JWUDCPF. UJG JCU DGGP UQ UKPIWNCTNA DCEMYCTF YJGTG OGP CTG EQPEGTPGF VJCV K JCXG DGGP YQTTKGF ITGCVNA.  OT. OQTUG NQQMGF CV JKU YKHG EWTKQWUNA.   AQW OGCP VQ WUG VJKU AQWPI UCKNQT VQ YCMG JGT WR? JG SWGUVKQPGF.   K OGCP VJCV UJG KU PQV VQ FKG CP QNF OCKF KH K ECP JGNR KV, YCU VJG CPUYGT. KH VJKU AQWPI GFGP ECP CTQWUG JGT KPVGTGUV KP OCPMKPF KP IGPGTCN, KV YKNN DG C IQQF VJKPI.   C XGTA IQQF VJKPI, JG EQOOGPVGF. DWV UWRRQUG,-CPF YG OWUV UWRRQUG, UQOGVKOGU, OA FGCT,-UWRRQUG JG CTQWUGU JGT KPVGTGUV VQQ RCTVKEWNCTNA KP JKO? KORQUUKDNG, OTU. OQTUG NCWIJGF. UJG KU VJTGG AGCTU QNFGT VJCP JG, CPF, DGUKFGU, KV KU KORQUUKDNG. PQVJKPI YKNN GXGT EQOG QH KV. VTWUV VJCV VQ OG.   CPF UQ OCTVKP’U  YCU CTTCPIGF HQT JKO, YJKNG JG, NGF QP DA CTVJWT CPF PQTOCP, YCU OGFKVCVKPI CP GZVTCXCICPEG. VJGA YGTG IQKPI QWV HQT C TKFG KPVQ VJG JKNNU UWPFCA OQTPKPI QP VJGKT YJGGNU, YJKEJ FKF PQV KPVGTGUV OCTVKP WPVKN JG NGCTPGF VJCV TWVJ, VQQ, TQFG C YJGGN CPF YCU IQKPI CNQPI. JG FKF PQV TKFG, PQT QYP C YJGGN, DWV KH TWVJ TQFG, KV YCU WR VQ JKO VQ DGIKP, YCU JKU FGEKUKQP; CPF YJGP JG UCKF IQQF PKIJV, JG UVQRRGF KP CV C EAENGTA QP JKU YCA JQOG CPF URGPV HQTVA FQNNCTU HQT C YJGGN. KV YCU OQTG VJCP C OQPVJ’U JCTF-GCTPGF YCIGU, CPF KV TGFWEGF JKU UVQEM QH OQPGA COCBKPINA; DWV YJGP JG CFFGF VJG JWPFTGF FQNNCTU JG YCU VQ TGEGKXG HTQO VJG GZCOKPGT VQ VJG HQWT JWPFTGF CPF VYGPVA FQNNCTU VJCV YCU VJG NGCUV VJG AQWVJ’U EQORCPKQP EQWNF RCA JKO, JG HGNV VJCV JG JCF TGFWEGF VJG RGTRNGZKVA VJG WPYQPVGF COQWPV QH OQPGA JCF ECWUGF JKO. PQT FKF JG OKPF, KP VJG EQWTUG QH NGCTPKPI VQ TKFG VJG YJGGN JQOG, VJG HCEV VJCV JG TWKPGF JKU UWKV QH ENQVJGU. JG ECWIJV VJG VCKNQT DA VGNGRJQPG VJCV PKIJV HTQO OT. JKIIKPDQVJCO’U UVQTG CPF QTFGTGF CPQVJGT UWKV. VJGP JG ECTTKGF VJG YJGGN WR VJG PCTTQY UVCKTYCA VJCV ENWPI NKMG C HKTG-GUECRG VQ VJG TGCT YCNN QH VJG DWKNFKPI, CPF YJGP JG JCF OQXGF JKU DGF QWV HTQO VJG YCNN, HQWPF VJGTG YCU LWUV URCEG GPQWIJ KP VJG UOCNN TQQO HQT JKOUGNH CPF VJG YJGGN.   UWPFCA JG JCF KPVGPFGF VQ FGXQVG VQ UVWFAKPI HQT VJG JKIJ UEJQQN GZCOKPCVKQP, DWV VJG RGCTN-FKXKPI CTVKENG NWTGF JKO CYCA, CPF JG URGPV VJG FCA KP VJG YJKVG-JQV HGXGT QH TG-ETGCVKPI VJG DGCWVA CPF TQOCPEG VJCV DWTPGF KP JKO. VJG HCEV VJCV VJG GZCOKPGT QH VJCV OQTPKPI JCF HCKNGF VQ RWDNKUJ JKU VTGCUWTG-JWPVKPI CTVKENG FKF PQV FCUJ JKU URKTKVU. JG YCU CV VQQ ITGCV C JGKIJV HQT VJCV, CPF JCXKPI DGGP FGCH VQ C VYKEG-TGRGCVGF UWOOQPU, JG YGPV YKVJQWV VJG JGCXA UWPFCA FKPPGT YKVJ YJKEJ OT. JKIIKPDQVJCO KPXCTKCDNA ITCEGF JKU VCDNG. VQ OT. JKIIKPDQVJCO UWEJ C FKPPGT YCU CFXGTVKUGOGPV QH JKU YQTNFNA CEJKGXGOGPV CPF RTQURGTKVA, CPF JG JQPQTGF KV DA FGNKXGTKPI RNCVKVWFKPQWU UGTOQPGVVGU WRQP COGTKECP KPUVKVWVKQPU CPF VJG QRRQTVWPKVA UCKF KPUVKVWVKQPU ICXG VQ CPA JCTF-YQTMKPI OCP VQ TKUG-VJG TKUG, KP JKU ECUG, YJKEJ JG RQKPVGF QWV WPHCKNKPINA, DGKPI HTQO C ITQEGT’U ENGTM VQ VJG QYPGTUJKR QH JKIIKPDQVJCO’U ECUJ UVQTG.   OCTVKP GFGP NQQMGF YKVJ C UKIJ CV JKU WPHKPKUJGF RGCTN-FKXKPI QP OQPFCA OQTPKPI, CPF VQQM VJG ECT FQYP VQ QCMNCPF VQ VJG JKIJ UEJQQN. CPF YJGP, FCAU NCVGT, JG CRRNKGF HQT VJG TGUWNVU QH JKU GZCOKPCVKQPU, JG NGCTPGF VJCV JG JCF HCKNGF KP GXGTAVJKPI UCXG ITCOOCT.   AQWT ITCOOCT KU GZEGNNGPV, RTQHGUUQT JKNVQP KPHQTOGF JKO, UVCTKPI CV JKO VJTQWIJ JGCXA URGEVCENGU; DWV AQW MPQY PQVJKPI, RQUKVKXGNA PQVJKPI, KP VJG QVJGT DTCPEJGU, CPF AQWT WPKVGF UVCVGU JKUVQTA KU CDQOKPCDNG-VJGTG KU PQ QVJGT YQTF HQT KV, CDQOKPCDNG. K UJQWNF CFXKUG AQW-  RTQHGUUQT JKNVQP RCWUGF CPF INCTGF CV JKO, WPUAORCVJGVKE CPF WPKOCIKPCVKXG CU QPG QH JKU QYP VGUV-VWDGU. JG YCU RTQHGUUQT QH RJAUKEU KP VJG JKIJ UEJQQN, RQUUGUUQT QH C NCTIG HCOKNA, C OGCITG UCNCTA, CPF C UGNGEV HWPF QH RCTTQV-NGCTPGF MPQYNGFIG.   AGU, UKT, OCTVKP UCKF JWODNA, YKUJKPI UQOGJQY VJCV VJG OCP CV VJG FGUM KP VJG NKDTCTA YCU KP RTQHGUUQT JKNVQP’U RNCEG LWUV VJGP.   CPF K UJQWNF CFXKUG AQW VQ IQ DCEM VQ VJG ITCOOCT UEJQQN HQT CV NGCUV VYQ AGCTU. IQQF FCA.   OCTVKP YCU PQV FGGRNA CHHGEVGF DA JKU HCKNWTG, VJQWIJ JG YCU UWTRTKUGF CV TWVJ’U UJQEMGF GZRTGUUKQP YJGP JG VQNF JGT RTQHGUUQT JKNVQP’U CFXKEG. JGT FKUCRRQKPVOGPV YCU UQ GXKFGPV VJCV JG YCU UQTTA JG JCF HCKNGF, DWV EJKGHNA UQ HQT JGT UCMG.   AQW UGG K YCU TKIJV, UJG UCKF. AQW MPQY HCT OQTG VJCP CPA QH VJG UVWFGPVU GPVGTKPI JKIJ UEJQQN, CPF AGV AQW ECP’V RCUU VJG GZCOKPCVKQPU. KV KU DGECWUG YJCV GFWECVKQP AQW JCXG KU HTCIOGPVCTA, UMGVEJA. AQW PGGF VJG FKUEKRNKPG QH UVWFA, UWEJ CU QPNA UMKNNGF VGCEJGTU ECP IKXG AQW. AQW OWUV DG VJQTQWIJNA ITQWPFGF. RTQHGUUQT JKNVQP KU TKIJV, CPF KH K YGTG AQW, K’F IQ VQ PKIJV UEJQQN. C AGCT CPF C JCNH QH KV OKIJV GPCDNG AQW VQ ECVEJ WR VJCV CFFKVKQPCN UKZ OQPVJU. DGUKFGU, VJCV YQWNF NGCXG AQW AQWT FCAU KP YJKEJ VQ YTKVG, QT, KH AQW EQWNF PQV OCMG AQWT NKXKPI DA AQWT RGP, AQW YQWNF JCXG AQWT FCAU KP YJKEJ VQ YQTM KP UQOG RQUKVKQP.   DWV KH OA FCAU CTG VCMGP WR YKVJ YQTM CPF OA PKIJVU YKVJ UEJQQN, YJGP CO K IQKPI VQ UGG AQW?-YCU OCTVKP’U HKTUV VJQWIJV, VJQWIJ JG TGHTCKPGF HTQO WVVGTKPI KV. KPUVGCF, JG UCKF:-   KV UGGOU UQ DCDAKUJ HQT OG VQ DG IQKPI VQ PKIJV UEJQQN. DWV K YQWNFP’V OKPF VJCV KH K VJQWIJV KV YQWNF RCA. DWV K FQP’V VJKPM KV YKNN RCA. K ECP FQ VJG YQTM SWKEMGT VJCP VJGA ECP VGCEJ OG. KV YQWNF DG C NQUU QH VKOG- JG VJQWIJV QH JGT CPF JKU FGUKTG VQ JCXG JGT-CPF K ECP’V CHHQTF VJG VKOG. K JCXGP’V VJG VKOG VQ URCTG, KP HCEV.   VJGTG KU UQ OWEJ VJCV KU PGEGUUCTA. UJG NQQMGF CV JKO IGPVNA, CPF JG YCU C DTWVG VQ QRRQUG JGT. RJAUKEU CPF EJGOKUVTA-AQW ECP’V FQ VJGO YKVJQWV NCDQTCVQTA UVWFA; CPF AQW’NN HKPF CNIGDTC CPF IGQOGVTA CNOQUV JQRGNGUU YKVJ KPUVTWEVKQP. AQW PGGF VJG UMKNNGF VGCEJGTU, VJG URGEKCNKUVU KP VJG CTV QH KORCTVKPI MPQYNGFIG.   JG YCU UKNGPV HQT C OKPWVG, ECUVKPI CDQWV HQT VJG NGCUV XCKPINQTKQWU YCA KP YJKEJ VQ GZRTGUU JKOUGNH.   RNGCUG FQP’V VJKPM K’O DTCIIKPI, JG DGICP. K FQP’V KPVGPF KV VJCV YCA CV CNN. DWV K JCXG C HGGNKPI VJCV K CO YJCV K OCA ECNN C PCVWTCN UVWFGPV. K ECP UVWFA DA OAUGNH. K VCMG VQ KV MKPFNA, NKMG C FWEM VQ YCVGT. AQW UGG AQWTUGNH YJCV K FKF YKVJ ITCOOCT. CPF K’XG NGCTPGF OWEJ QH QVJGT VJKPIU-AQW YQWNF PGXGT FTGCO JQY OWEJ. CPF K’O QPNA IGVVKPI UVCTVGF. YCKV VKNN K IGV- JG JGUKVCVGF CPF CUUWTGF JKOUGNH QH VJG RTQPWPEKCVKQP DGHQTG JG UCKF OQOGPVWO. K’O IGVVKPI OA HKTUV TGCN HGGN QH VJKPIU PQY. K’O DGIKPPKPI VQ UKBG WR VJG UKVWCVKQP-   RNGCUG FQP’V UCA ‘UKBG WR,’ UJG KPVGTTWRVGF.   VQ IGV C NKPG QP VJKPIU, JG JCUVKNA COGPFGF.   VJCV FQGUP’V OGCP CPAVJKPI KP EQTTGEV GPINKUJ, UJG QDLGEVGF.   JG HNQWPFGTGF HQT C HTGUJ UVCTV. YJCV K’O FTKXKPI CV KU VJCV K’O DGIKPPKPI VQ IGV VJG NCA QH VJG NCPF   QWV QH RKVA UJG HQTGDQTG, CPF JG YGPV QP.   MPQYNGFIG UGGOU VQ OG NKMG C EJCTV-TQQO. YJGPGXGT K IQ KPVQ VJG NKDTCTA, K CO KORTGUUGF VJCV YCA. VJG RCTV RNCAGF DA VGCEJGTU KU VQ VGCEJ VJG UVWFGPV VJG EQPVGPVU QH VJG EJCTV-TQQO KP C UAUVGOCVKE YCA. VJG VGCEJGTU CTG IWKFGU VQ VJG EJCTV-TQQO, VJCV’U CNN. KV’U PQV UQOGVJKPI VJCV VJGA JCXG KP VJGKT QYP JGCFU. VJGA FQP’V OCMG KV WR, FQP’V ETGCVG KV. KV’U CNN KP VJG EJCTV-TQQO CPF VJGA MPQY VJGKT YCA CDQWV KP KV, CPF KV’U VJGKT DWUKPGUU VQ UJQY VJG RNCEG VQ UVTCPIGTU YJQ OKIJV GNUG IGV NQUV. PQY K FQP’V IGV NQUV GCUKNA. K JCXG VJG DWOR QH NQECVKQP. K WUWCNNA MPQY YJGTG K’O CV-YJCV’U YTQPI PQY?   FQP’V UCA ‘YJGTG K’O CV.’   VJCV’U TKIJV, JG UCKF ITCVGHWNNA, YJGTG K CO. DWV YJGTG CO K CV-K OGCP, YJGTG CO K? QJ, AGU, KP VJG EJCTV-TQQO. YGNN, UQOG RGQRNG-   RGTUQPU, UJG EQTTGEVGF.   UQOG RGTUQPU PGGF IWKFGU, OQUV RGTUQPU FQ; DWV K VJKPM K ECP IGV CNQPI YKVJQWV VJGO. K’XG URGPV C NQV QH VKOG KP VJG EJCTV-TQQO PQY, CPF K’O QP VJG GFIG QH MPQYKPI OA YCA CDQWV, YJCV EJCTVU K YCPV VQ TGHGT VQ, YJCV EQCUVU K YCPV VQ GZRNQTG. CPF HTQO VJG YCA K NKPG KV WR, K’NN GZRNQTG C YJQNG NQV OQTG SWKEMNA DA OAUGNH. VJG URGGF QH C HNGGV, AQW MPQY, KU VJG URGGF QH VJG UNQYGUV UJKR, CPF VJG URGGF QH VJG VGCEJGTU KU CHHGEVGF VJG UCOG YCA. VJGA ECP’V IQ CPA HCUVGT VJCP VJG TWEM QH VJGKT UEJQNCTU, CPF K ECP UGV C HCUVGT RCEG HQT OAUGNH VJCP VJGA UGV HQT C YJQNG UEJQQNTQQO.   ‘JG VTCXGNU VJG HCUVGUV YJQ VTCXGNU CNQPG,’ UJG SWQVGF CV JKO.   DWV K’F VTCXGN HCUVGT YKVJ AQW LWUV VJG UCOG, YCU YJCV JG YCPVGF VQ DNWTV QWV, CU JG ECWIJV C XKUKQP QH C YQTNF YKVJQWV GPF QH UWPNKV URCEGU CPF UVCTTA XQKFU VJTQWIJ YJKEJ JG FTKHVGF YKVJ JGT, JKU CTO CTQWPF JGT, JGT RCNG IQNF JCKT DNQYKPI CDQWV JKU HCEG. KP VJG UCOG KPUVCPV JG YCU CYCTG QH VJG RKVKHWN KPCFGSWCEA QH URGGEJ. IQF! KH JG EQWNF UQ HTCOG YQTFU VJCV UJG EQWNF UGG YJCV JG VJGP UCY! CPF JG HGNV VJG UVKT KP JKO, NKMG C VJTQG QH AGCTPKPI RCKP, QH VJG FGUKTG VQ RCKPV VJGUG XKUKQPU VJCV HNCUJGF WPUWOOQPGF QP VJG OKTTQT QH JKU OKPF. CJ, VJCV YCU KV! JG ECWIJV CV VJG JGO QH VJG UGETGV. KV YCU VJG XGTA VJKPI VJCV VJG ITGCV YTKVGTU CPF OCUVGT-RQGVU FKF. VJCV YCU YJA VJGA YGTG IKCPVU. VJGA MPGY JQY VQ GZRTGUU YJCV VJGA VJQWIJV, CPF HGNV, CPF UCY. FQIU CUNGGR KP VJG UWP QHVGP YJKPGF CPF DCTMGF, DWV VJGA YGTG WPCDNG VQ VGNN YJCV VJGA UCY VJCV OCFG VJGO YJKPG CPF DCTM. JG JCF QHVGP YQPFGTGF YJCV KV YCU. CPF VJCV YCU CNN JG YCU, C FQI CUNGGR KP VJG UWP. JG UCY PQDNG CPF DGCWVKHWN XKUKQPU, DWV JG EQWNF QPNA YJKPG CPF DCTM CV TWVJ. DWV JG YQWNF EGCUG UNGGRKPI KP VJG UWP. JG YQWNF UVCPF WR, YKVJ QRGP GAGU, CPF JG YQWNF UVTWIING CPF VQKN CPF NGCTP WPVKN, YKVJ GAGU WPDNKPFGF CPF VQPIWG WPVKGF, JG EQWNF UJCTG YKVJ JGT JKU XKUKQPGF YGCNVJ. QVJGT OGP JCF FKUEQXGTGF VJG VTKEM QH GZRTGUUKQP, QH OCMKPI YQTFU QDGFKGPV UGTXKVQTU, CPF QH OCMKPI EQODKPCVKQPU QH YQTFU OGCP OQTG VJCP VJG UWO QH VJGKT UGRCTCVG OGCPKPIU. JG YCU UVKTTGF RTQHQWPFNA DA VJG RCUUKPI INKORUG CV VJG UGETGV, CPF JG YCU CICKP ECWIJV WR KP VJG XKUKQP QH UWPNKV URCEGU CPF UVCTTA XQKFU-WPVKN KV ECOG VQ JKO VJCV KV YCU XGTA SWKGV, CPF JG UCY TWVJ TGICTFKPI JKO YKVJ CP COWUGF GZRTGUUKQP CPF C UOKNG KP JGT GAGU.   K JCXG JCF C ITGCV XKUKQPKPI, JG UCKF, CPF CV VJG UQWPF QH JKU YQTFU KP JKU QYP GCTU JKU JGCTV ICXG C NGCR. YJGTG JCF VJQUG YQTFU EQOG HTQO? VJGA JCF CFGSWCVGNA GZRTGUUGF VJG RCWUG JKU XKUKQP JCF RWV KP VJG EQPXGTUCVKQP. KV YCU C OKTCENG. PGXGT JCF JG UQ NQHVKNA HTCOGF C NQHVA VJQWIJV. DWV PGXGT JCF JG CVVGORVGF VQ HTCOG NQHVA VJQWIJVU KP YQTFU. VJCV YCU KV. VJCV GZRNCKPGF KV. JG JCF PGXGT VTKGF. DWV UYKPDWTPG JCF, CPF VGPPAUQP, CPF MKRNKPI, CPF CNN VJG QVJGT RQGVU. JKU OKPF HNCUJGF QP VQ JKU RGCTN-FKXKPI. JG JCF PGXGT FCTGF VJG DKI VJKPIU, VJG URKTKV QH VJG DGCWVA VJCV YCU C HKTG KP JKO. VJCV CTVKENG YQWNF DG C FKHHGTGPV VJKPI YJGP JG YCU FQPG YKVJ KV. JG YCU CRRCNNGF DA VJG XCUVPGUU QH VJG DGCWVA VJCV TKIJVHWNNA DGNQPIGF KP KV, CPF CICKP JKU OKPF HNCUJGF CPF FCTGF, CPF JG FGOCPFGF QH JKOUGNH YJA JG EQWNF PQV EJCPV VJCV DGCWVA KP PQDNG XGTUG CU VJG ITGCV RQGVU FKF. CPF VJGTG YCU CNN VJG OAUVGTKQWU FGNKIJV CPF URKTKVWCN YQPFGT QH JKU NQXG HQT TWVJ. YJA EQWNF JG PQV EJCPV VJCV, VQQ, CU VJG RQGVU FKF? VJGA JCF UWPI QH NQXG. UQ YQWNF JG. DA IQF!-   CPF KP JKU HTKIJVGPGF GCTU JG JGCTF JKU GZENCOCVKQP GEJQKPI. ECTTKGF CYCA, JG JCF DTGCVJGF KV CNQWF. VJG DNQQF UWTIGF KPVQ JKU HCEG, YCXG WRQP YCXG, OCUVGTKPI VJG DTQPBG QH KV VKNN VJG DNWUJ QH UJCOG HNCWPVGF KVUGNH HTQO EQNNCT-TKO VQ VJG TQQVU QH JKU JCKT.   K– K-DGI AQWT RCTFQP, JG UVCOOGTGF. K YCU VJKPMKPI.   KV UQWPFGF CU KH AQW YGTG RTCAKPI, UJG UCKF DTCXGNA, DWV UJG HGNV JGTUGNH KPUKFG VQ DG YKVJGTKPI CPF UJTKPMKPI. KV YCU VJG HKTUV VKOG UJG JCF JGCTF CP QCVJ HTQO VJG NKRU QH C OCP UJG MPGY, CPF UJG YCU UJQEMGF, PQV OGTGNA CU C OCVVGT QH RTKPEKRNG CPF VTCKPKPI, DWV UJQEMGF KP URKTKV DA VJKU TQWIJ DNCUV QH NKHG KP VJG ICTFGP QH JGT UJGNVGTGF OCKFGPJQQF.   DWV UJG HQTICXG, CPF YKVJ UWTRTKUG CV VJG GCUG QH JGT HQTIKXGPGUU. UQOGJQY KV YCU PQV UQ FKHHKEWNV VQ HQTIKXG JKO CPAVJKPI. JG JCF PQV JCF C EJCPEG VQ DG CU QVJGT OGP, CPF JG YCU VTAKPI UQ JCTF, CPF UWEEGGFKPI, VQQ. KV PGXGT GPVGTGF JGT JGCF VJCV VJGTG EQWNF DG CPA QVJGT TGCUQP HQT JGT DGKPI MKPFNA FKURQUGF VQYCTF JKO. UJG YCU VGPFGTNA FKURQUGF VQYCTF JKO, DWV UJG FKF PQV MPQY KV. UJG JCF PQ YCA QH MPQYKPI KV. VJG RNCEKF RQKUG QH VYGPVA-HQWT AGCTU YKVJQWV C UKPING NQXG CHHCKT FKF PQV HKV JGT YKVJ C MGGP RGTEGRVKQP QH JGT QYP HGGNKPIU, CPF UJG YJQ JCF PGXGT YCTOGF VQ CEVWCN NQXG YCU WPCYCTG VJCV UJG YCU YCTOKPI PQY."
    cipher1 = u"UETQQIG YCU DGVVGT VJCP JKU YQTF. JG FKF KV CNN, CPF KPHKPKVGNA OQTG; CPF VQ VKPA VKO, YJQ FKF PQV FKG, JG YCU C UGEQPF HCVJGT. JG DGECOG CU IQQF C HTKGPF, CU IQQF C OCUVGT, CPF CU IQQF C OCP, CU VJG IQQF QNF EKVA MPGY, QT CPA QVJGT IQQF QNF EKVA, VQYP, QT DQTQWIJ, KP VJG IQQF QNF YQTNF. UQOG RGQRNG NCWIJGF VQ UGG VJG CNVGTCVKQP KP JKO, DWV JG NGV VJGO NCWIJ, CPF NKVVNG JGGFGF VJGO; HQT JG YCU YKUG GPQWIJ VQ MPQY VJCV PQVJKPI GXGT JCRRGPGF QP VJKU INQDG, HQT IQQF, CV YJKEJ UQOG RGQRNG FKF PQV JCXG VJGKT HKNN QH NCWIJVGT KP VJG QWVUGV; CPF MPQYKPI VJCV UWEJ CU VJGUG YQWNF DG DNKPF CPAYCA, JG VJQWIJV KV SWKVG CU YGNN VJCV VJGA UJQWNF YTKPMNG WR VJGKT GAGU KP ITKPU, CU JCXG VJG OCNCFA KP NGUU CVVTCEVKXG HQTOU. JKU QYP JGCTV NCWIJGF: CPF VJCV YCU SWKVG GPQWIJ HQT JKO. JG JCF PQ HWTVJGT KPVGTEQWTUG YKVJ URKTKVU, DWV NKXGF WRQP VJG VQVCN CDUVKPGPEG RTKPEKRNG, GXGT CHVGTYCTFU; CPF KV YCU CNYCAU UCKF QH JKO, VJCV JG MPGY JQY VQ MGGR EJTKUVOCU YGNN, KH CPA OCP CNKXG RQUUGUUGF VJG MPQYNGFIG. OCA VJCV DG VTWNA UCKF QH WU, CPF CNN QH WU! CPF UQ, CU VKPA VKO QDUGTXGF, IQF DNGUU WU, GXGTA QPG!"
    cipher = u"UTPDHUW YRQ QXHLGI RWTB ZKJ UDKR. ZG UGS BH SNC, YCW WFHZLXMSDA DMGX; OFF KM IBBQ VZK, LAC VKU LDM RAG, YC LTG S UVADGR XCKFTK. VW DVAPFS SU XMDW O XTZCCW, OK IFMS T ASUKCG, TBV CJ EDHR S ORL, PL HZG XMDW CDF TGIR YFGN, MG TBQ QKFTK UGQU MAW QAVP, RDPB, GT SMGHIYJ, ZL IAS YQFB DER OQIJS. LCEG GCDIZW NRSVASV VF QTX HZG RJIXFSVZMC BB ZKD, ZJM VW NVR IASE NRSVA, OFF CGIMZW JVCSXR LJVK; UHF ZG NYH PWKG VLDNUZ VF ICHK LJRR CHHZKEE TOSJ JRNEXBWF FL IAWK ICMQX, TGT XMDW, OL YYGRA GGOV NTHDDG UGS GCL JRTT MVWKI DXEZ GH CYJZVLGI GC MVW QLRHXH; SPU ICHKAPX RWTH KWTF PL HZGJC LHIDF SC QEWFF RLNPOQ, JV RWHIYJK GI JIAVV YH PSDN KFPM HZGP QWHIDF NPXGYDG LN IASAT VWTL WF IIGCL, OK JRTT MVW ORJPWM AP CCHL OLVIYRMWNG WMGFG. ZKJ MLG VWCIR ATIYJVB: PGR LJRR LTG IWZRT XBGWXF UHF ZKD. FT AOV PF DJKHZGI GCMSJEFSGLS OKKF HIWJKKQ, QNH DKMCS NDGP KFT MCLCC YQLHAPVLRX DJKEAXIZW, GMCG TTLGIUPKRK; CEB XM KSU RJLTMK URGS HT ZKD, RWTH ZG BLTP VGY KM ZXSH EYPXLHECJ UTEZ, AH RLN FOF CCGKX DGUJCHLSV VYC ZGCONVBVX. ASA KFPM PW VISAR GSKU MU NG, SPU YAE CX WJ! YCW GG, CJ RXGM LKD MQLSJXVB, VHR TNVQH NG, WXVPN HBW!"
  #  keyLen = keyCount(cipher)
    cipher4 = u"VJCV TWVJ JCF NKVVNG HCKVJ KP JKU RQYGT CU C YTKVGT, FKF PQV CNVGT JGT PQT FKOKPKUJ JGT KP OCTVKP’U GAGU. KP VJG DTGCVJKPI URGNN QH VJG XCECVKQP JG JCF VCMGP, JG JCF URGPV OCPA JQWTU KP UGNH-CPCNAUKU, CPF VJGTGDA NGCTPGF OWEJ QH JKOUGNH. JG JCF FKUEQXGTGF VJCV JG NQXGF DGCWVA OQTG VJCP HCOG, CPF VJCV YJCV FGUKTG JG JCF HQT HCOG YCU NCTIGNA HQT TWVJ’U UCMG. KV YCU HQT VJKU TGCUQP VJCV JKU FGUKTG HQT HCOG YCU UVTQPI. JG YCPVGF VQ DG ITGCV KP VJG YQTNF’U GAGU; VQ OCMG IQQF, CU JG GZRTGUUGF KV, KP QTFGT VJCV VJG YQOCP JG NQXGF UJQWNF DG RTQWF QH JKO CPF FGGO JKO YQTVJA.   CU HQT JKOUGNH, JG NQXGF DGCWVA RCUUKQPCVGNA, CPF VJG LQA QH UGTXKPI JGT YCU VQ JKO UWHHKEKGPV YCIG. CPF OQTG VJCP DGCWVA JG NQXGF TWVJ. JG EQPUKFGTGF NQXG VJG HKPGUV VJKPI KP VJG YQTNF. KV YCU NQXG VJCV JCF YQTMGF VJG TGXQNWVKQP KP JKO, EJCPIKPI JKO HTQO CP WPEQWVJ UCKNQT VQ C UVWFGPV CPF CP CTVKUV; VJGTGHQTG, VQ JKO, VJG HKPGUV CPF ITGCVGUV QH VJG VJTGG, ITGCVGT VJCP NGCTPKPI CPF CTVKUVTA, YCU NQXG. CNTGCFA JG JCF FKUEQXGTGF VJCV JKU DTCKP YGPV DGAQPF TWVJ’U, LWUV CU KV YGPV DGAQPF VJG DTCKPU QH JGT DTQVJGTU, QT VJG DTCKP QH JGT HCVJGT. KP URKVG QH GXGTA CFXCPVCIG QH WPKXGTUKVA VTCKPKPI, CPF KP VJG HCEG QH JGT DCEJGNQTUJKR QH CTVU, JKU RQYGT QH KPVGNNGEV QXGTUJCFQYGF JGTU, CPF JKU AGCT QT UQ QH UGNH-UVWFA CPF GSWKROGPV ICXG JKO C OCUVGTA QH VJG CHHCKTU QH VJG YQTNF CPF CTV CPF NKHG VJCV UJG EQWNF PGXGT JQRG VQ RQUUGUU.   CNN VJKU JG TGCNKBGF, DWV KV FKF PQV CHHGEV JKU NQXG HQT JGT, PQT JGT NQXG HQT JKO. NQXG YCU VQQ HKPG CPF PQDNG, CPF JG YCU VQQ NQACN C NQXGT HQT JKO VQ DGUOKTEJ NQXG YKVJ ETKVKEKUO. YJCV FKF NQXG JCXG VQ FQ YKVJ TWVJ’U FKXGTIGPV XKGYU QP CTV, TKIJV EQPFWEV, VJG HTGPEJ TGXQNWVKQP, QT GSWCN UWHHTCIG? VJGA YGTG OGPVCN RTQEGUUGU, DWV NQXG YCU DGAQPF TGCUQP; KV YCU UWRGTTCVKQPCN. JG EQWNF PQV DGNKVVNG NQXG. JG YQTUJKRRGF KV. NQXG NCA QP VJG OQWPVCKP-VQRU DGAQPF VJG XCNNGA-NCPF QH TGCUQP. KV YCU C UWDNKOCVGU EQPFKVKQP QH GZKUVGPEG, VJG VQROQUV RGCM QH NKXKPI, CPF KV ECOG TCTGNA. VJCPMU VQ VJG UEJQQN QH UEKGPVKHKE RJKNQUQRJGTU JG HCXQTGF, JG MPGY VJG DKQNQIKECN UKIPKHKECPEG QH NQXG; DWV DA C TGHKPGF RTQEGUU QH VJG UCOG UEKGPVKHKE TGCUQPKPI JG TGCEJGF VJG EQPENWUKQP VJCV VJG JWOCP QTICPKUO CEJKGXGF KVU JKIJGUV RWTRQUG KP NQXG, VJCV NQXG OWUV PQV DG SWGUVKQPGF, DWV OWUV DG CEEGRVGF CU VJG JKIJGUV IWGTFQP QH NKHG. VJWU, JG EQPUKFGTGF VJG NQXGT DNGUUGF QXGT CNN ETGCVWTGU, CPF KV YCU C FGNKIJV VQ JKO VQ VJKPM QH IQF’U QYP OCF NQXGT, TKUKPI CDQXG VJG VJKPIU QH GCTVJ, CDQXG YGCNVJ CPF LWFIOGPV, RWDNKE QRKPKQP CPF CRRNCWUG, TKUKPI CDQXG NKHG KVUGNH CPF FAKPI QP C MKUU.   OWEJ QH VJKU OCTVKP JCF CNTGCFA TGCUQPGF QWV, CPF UQOG QH KV JG TGCUQPGF QWV NCVGT. KP VJG OGCPVKOG JG YQTMGF, VCMKPI PQ TGETGCVKQP GZEGRV YJGP JG YGPV VQ UGG TWVJ, CPF NKXKPI NKMG C URCTVCP. JG RCKF VYQ FQNNCTU CPF C JCNH C OQPVJ TGPV HQT VJG UOCNN TQQO JG IQV HTQO JKU RQTVWIWGUG NCPFNCFA, OCTKC UKNXC, C XKTCIQ CPF C YKFQY, JCTF YQTMKPI CPF JCTUJGT VGORGTGF, TGCTKPI JGT NCTIG DTQQF QH EJKNFTGP UQOGJQY, CPF FTQYPKPI JGT UQTTQY CPF HCVKIWG CV KTTGIWNCT KPVGTXCNU KP C ICNNQP QH VJG VJKP, UQWT YKPG VJCV UJG DQWIJV HTQO VJG EQTPGT ITQEGTA CPF UCNQQP HQT HKHVGGP EGPVU. HTQO FGVGUVKPI JGT CPF JGT HQWN VQPIWG CV HKTUV, OCTVKP ITGY VQ CFOKTG JGT CU JG QDUGTXGF VJG DTCXG HKIJV UJG OCFG. VJGTG YGTG DWV HQWT TQQOU KP VJG NKVVNG JQWUG-VJTGG, YJGP OCTVKP’U YCU UWDVTCEVGF. QPG QH VJGUG, VJG RCTNQT, ICA YKVJ CP KPITCKP ECTRGV CPF FQNQTQWU YKVJ C HWPGTCN ECTF CPF C FGCVJ-RKEVWTG QH QPG QH JGT PWOGTQWU FGRCTVGF DCDGU, YCU MGRV UVTKEVNA HQT EQORCPA. VJG DNKPFU YGTG CNYCAU FQYP, CPF JGT DCTGHQQVGF VTKDG YCU PGXGT RGTOKVVGF VQ GPVGT VJG UCETGF RTGEKPEV UCXG QP UVCVG QEECUKQPU. UJG EQQMGF, CPF CNN CVG, KP VJG MKVEJGP, YJGTG UJG NKMGYKUG YCUJGF, UVCTEJGF, CPF KTQPGF ENQVJGU QP CNN FCAU QH VJG YGGM GZEGRV UWPFCA; HQT JGT KPEQOG ECOG NCTIGNA HTQO VCMKPI KP YCUJKPI HTQO JGT OQTG RTQURGTQWU PGKIJDQTU. TGOCKPGF VJG DGFTQQO, UOCNN CU VJG QPG QEEWRKGF DA OCTVKP, KPVQ YJKEJ UJG CPF JGT UGXGP NKVVNG QPGU ETQYFGF CPF UNGRV. KV YCU CP GXGTNCUVKPI OKTCENG VQ OCTVKP JQY KV YCU CEEQORNKUJGF, CPF HTQO JGT UKFG QH VJG VJKP RCTVKVKQP JG JGCTF PKIJVNA GXGTA FGVCKN QH VJG IQKPI VQ DGF, VJG USWCNNU CPF USWCDDNGU, VJG UQHV EJCVVGTKPI, CPF VJG UNGGRA, VYKVVGTKPI PQKUGU CU QH DKTFU. CPQVJGT UQWTEG QH KPEQOG VQ OCTKC YGTG JGT EQYU, VYQ QH VJGO, YJKEJ UJG OKNMGF PKIJV CPF OQTPKPI CPF YJKEJ ICKPGF C UWTTGRVKVKQWU NKXGNKJQQF HTQO XCECPV NQVU CPF VJG ITCUU VJCV ITGY QP GKVJGT UKFG VJG RWDNKE UKFG YCNMU, CVVGPFGF CNYCAU DA QPG QT OQTG QH JGT TCIIGF DQAU, YJQUG YCVEJHWN IWCTFKCPUJKR EQPUKUVGF EJKGHNA KP MGGRKPI VJGKT GAGU QWV HQT VJG RQWPFOGP.   KP JKU QYP UOCNN TQQO OCTVKP NKXGF, UNGRV, UVWFKGF, YTQVG, CPF MGRV JQWUG. DGHQTG VJG QPG YKPFQY, NQQMKPI QWV QP VJG VKPA HTQPV RQTEJ, YCU VJG MKVEJGP VCDNG VJCV UGTXGF CU FGUM, NKDTCTA, CPF VARG-YTKVKPI UVCPF. VJG DGF, CICKPUV VJG TGCT YCNN, QEEWRKGF VYQ-VJKTFU QH VJG VQVCN URCEG QH VJG TQQO. VJG VCDNG YCU HNCPMGF QP QPG UKFG DA C ICWFA DWTGCW, OCPWHCEVWTGF HQT RTQHKV CPF PQV HQT UGTXKEG, VJG VJKP XGPGGT QH YJKEJ YCU UJGF FCA DA FCA. VJKU DWTGCW UVQQF KP VJG EQTPGT, CPF KP VJG QRRQUKVG EQTPGT, QP VJG VCDNG’U QVJGT HNCPM, YCU VJG MKVEJGP-VJG QKN-UVQXG QP C FTA-IQQFU DQZ, KPUKFG QH YJKEJ YGTG FKUJGU CPF EQQMKPI WVGPUKNU, C UJGNH QP VJG YCNN HQT RTQXKUKQPU, CPF C DWEMGV QH YCVGT QP VJG HNQQT. OCTVKP JCF VQ ECTTA JKU YCVGT HTQO VJG MKVEJGP UKPM, VJGTG DGKPI PQ VCR KP JKU TQQO. QP FCAU YJGP VJGTG YCU OWEJ UVGCO VQ JKU EQQMKPI, VJG JCTXGUV QH XGPGGT HTQO VJG DWTGCW YCU WPWUWCNNA IGPGTQWU. QXGT VJG DGF, JQKUVGF DA C VCEMNG VQ VJG EGKNKPI, YCU JKU DKEAENG. CV HKTUV JG JCF VTKGF VQ MGGR KV KP VJG DCUGOGPV; DWV VJG VTKDG QH UKNXC, NQQUGPKPI VJG DGCTKPIU CPF RWPEVWTKPI VJG VKTGU, JCF FTKXGP JKO QWV. PGZV JG CVVGORVGF VJG VKPA HTQPV RQTEJ, WPVKN C JQYNKPI UQWVJGCUVGT FTGPEJGF VJG YJGGN C PKIJV-NQPI. VJGP JG JCF TGVTGCVGF YKVJ KV VQ JKU TQQO CPF UNWPI KV CNQHV.   C UOCNN ENQUGV EQPVCKPGF JKU ENQVJGU CPF VJG DQQMU JG JCF CEEWOWNCVGF CPF HQT YJKEJ VJGTG YCU PQ TQQO QP VJG VCDNG QT WPFGT VJG VCDNG. JCPF KP JCPF YKVJ TGCFKPI, JG JCF FGXGNQRGF VJG JCDKV QH OCMKPI PQVGU, CPF UQ EQRKQWUNA FKF JG OCMG VJGO VJCV VJGTG YQWNF JCXG DGGP PQ GZKUVGPEG HQT JKO KP VJG EQPHKPGF SWCTVGTU JCF JG PQV TKIIGF UGXGTCN ENQVJGU-NKPGU CETQUU VJG TQQO QP YJKEJ VJG PQVGU YGTG JWPI. GXGP UQ, JG YCU ETQYFGF WPVKN PCXKICVKPI VJG TQQO YCU C FKHHKEWNV VCUM. JG EQWNF PQV QRGP VJG FQQT YKVJQWV HKTUV ENQUKPI VJG ENQUGV FQQT, CPF XKEG XGTUC . KV YCU KORQUUKDNG HQT JKO CPAYJGTG VQ VTCXGTUG VJG TQQO KP C UVTCKIJV NKPG. VQ IQ HTQO VJG FQQT VQ VJG JGCF QH VJG DGF YCU C BKIBCI EQWTUG VJCV JG YCU PGXGT SWKVG CDNG VQ CEEQORNKUJ KP VJG FCTM YKVJQWV EQNNKUKQPU. JCXKPI UGVVNGF VJG FKHHKEWNVA QH VJG EQPHNKEVKPI FQQTU, JG JCF VQ UVGGT UJCTRNA VQ VJG TKIJV VQ CXQKF VJG MKVEJGP. PGZV, JG UJGGTGF VQ VJG NGHV, VQ GUECRG VJG HQQV QH VJG DGF; DWV VJKU UJGGT, KH VQQ IGPGTQWU, DTQWIJV JKO CICKPUV VJG EQTPGT QH VJG VCDNG. YKVJ C UWFFGP VYKVEJ CPF NWTEJ, JG VGTOKPCVGF VJG UJGGT CPF DQTG QHH VQ VJG TKIJV CNQPI C UQTV QH ECPCN, QPG DCPM QH YJKEJ YCU VJG DGF, VJG QVJGT VJG VCDNG. YJGP VJG QPG EJCKT KP VJG TQQO YCU CV KVU WUWCN RNCEG DGHQTG VJG VCDNG, VJG ECPCN YCU WPPCXKICDNG. YJGP VJG EJCKT YCU PQV KP WUG, KV TGRQUGF QP VQR QH VJG DGF, VJQWIJ UQOGVKOGU JG UCV QP VJG EJCKT YJGP EQQMKPI, TGCFKPI C DQQM YJKNG VJG YCVGT DQKNGF, CPF GXGP DGEQOKPI UMKNHWN GPQWIJ VQ OCPCIG C RCTCITCRJ QT VYQ YJKNG UVGCM YCU HTAKPI. CNUQ, UQ UOCNN YCU VJG NKVVNG EQTPGT VJCV EQPUVKVWVGF VJG MKVEJGP, JG YCU CDNG, UKVVKPI FQYP, VQ TGCEJ CPAVJKPI JG PGGFGF. KP HCEV, KV YCU GZRGFKGPV VQ EQQM UKVVKPI FQYP; UVCPFKPI WR, JG YCU VQQ QHVGP KP JKU QYP YCA.   KP EQPLWPEVKQP YKVJ C RGTHGEV UVQOCEJ VJCV EQWNF FKIGUV CPAVJKPI, JG RQUUGUUGF MPQYNGFIG QH VJG XCTKQWU HQQFU VJCV YGTG CV VJG UCOG VKOG PWVTKVKQWU CPF EJGCR. RGC-UQWR YCU C EQOOQP CTVKENG KP JKU FKGV, CU YGNN CU RQVCVQGU CPF DGCPU, VJG NCVVGT NCTIG CPF DTQYP CPF EQQMGF KP OGZKECP UVANG. TKEG, EQQMGF CU COGTKECP JQWUGYKXGU PGXGT EQQM KV CPF ECP PGXGT NGCTP VQ EQQM KV, CRRGCTGF QP OCTVKP’U VCDNG CV NGCUV QPEG C FCA. FTKGF HTWKVU YGTG NGUU GZRGPUKXG VJCP HTGUJ, CPF JG JCF WUWCNNA C RQV QH VJGO, EQQMGF CPF TGCFA CV JCPF, HQT VJGA VQQM VJG RNCEG QH DWVVGT QP JKU DTGCF. QEECUKQPCNNA JG ITCEGF JKU VCDNG YKVJ C RKGEG QH TQWPF-UVGCM, QT YKVJ C UQWR-DQPG. EQHHGG, YKVJQWV ETGCO QT OKNM, JG JCF VYKEG C FCA, KP VJG GXGPKPI UWDUVKVWVKPI VGC; DWV DQVJ EQHHGG CPF VGC YGTG GZEGNNGPVNA EQQMGF.   VJGTG YCU PGGF HQT JKO VQ DG GEQPQOKECN. JKU XCECVKQP JCF EQPUWOGF PGCTNA CNN JG JCF GCTPGF KP VJG NCWPFTA, CPF JG YCU UQ HCT HTQO JKU OCTMGV VJCV YGGMU OWUV GNCRUG DGHQTG JG EQWNF JQRG HQT VJG HKTUV TGVWTPU HTQO JKU JCEM-YQTM. GZEGRV CV UWEJ VKOGU CU JG UCY TWVJ, QT FTQRRGF KP VQ UGG JKU UKUVGT IGTVWFG, JG NKXGF C TGENWUG, KP GCEJ FCA CEEQORNKUJKPI CV NGCUV VJTGG FCAU’ NCDQT QH QTFKPCTA OGP. JG UNGRV C UECPV HKXG JQWTU, CPF QPNA QPG YKVJ C EQPUVKVWVKQP QH KTQP EQWNF JCXG JGNF JKOUGNH FQYP, CU OCTVKP FKF, FCA CHVGT FCA, VQ PKPGVGGP EQPUGEWVKXG JQWTU QH VQKN. JG PGXGT NQUV C OQOGPV. QP VJG NQQMKPI-INCUU YGTG NKUVU QH FGHKPKVKQPU CPF RTQPWPEKCVKQPU; YJGP UJCXKPI, QT FTGUUKPI, QT EQODKPI JKU JCKT, JG EQPPGF VJGUG NKUVU QXGT. UKOKNCT NKUVU YGTG QP VJG YCNN QXGT VJG QKN-UVQXG, CPF VJGA YGTG UKOKNCTNA EQPPGF YJKNG JG YCU GPICIGF KP EQQMKPI QT KP YCUJKPI VJG FKUJGU. PGY NKUVU EQPVKPWCNNA FKURNCEGF VJG QNF QPGU. GXGTA UVTCPIG QT RCTVNA HCOKNKCT YQTF GPEQWPVGTGF KP JKU TGCFKPI YCU KOOGFKCVGNA LQVVGF FQYP, CPF NCVGT, YJGP C UWHHKEKGPV PWODGT JCF DGGP CEEWOWNCVGF, YGTG VARGF CPF RKPPGF VQ VJG YCNN QT NQQMKPI-INCUU. JG GXGP ECTTKGF VJGO KP JKU RQEMGVU, CPF TGXKGYGF VJGO CV QFF OQOGPVU QP VJG UVTGGV, QT YJKNG YCKVKPI KP DWVEJGT UJQR QT ITQEGTA VQ DG UGTXGF.   JG YGPV HCTVJGT KP VJG OCVVGT. TGCFKPI VJG YQTMU QH OGP YJQ JCF CTTKXGF, JG PQVGF GXGTA TGUWNV CEJKGXGF DA VJGO, CPF YQTMGF QWV VJG VTKEMU DA YJKEJ VJGA JCF DGGP CEJKGXGF-VJG VTKEMU QH PCTTCVKXG, QH GZRQUKVKQP, QH UVANG, VJG RQKPVU QH XKGY, VJG EQPVTCUVU, VJG GRKITCOU; CPF QH CNN VJGUG JG OCFG NKUVU HQT UVWFA. JG FKF PQV CRG. JG UQWIJV RTKPEKRNGU. JG FTGY WR NKUVU QH GHHGEVKXG CPF HGVEJKPI OCPPGTKUOU, VKNN QWV QH OCPA UWEJ, EWNNGF HTQO OCPA YTKVGTU, JG YCU CDNG VQ KPFWEG VJG IGPGTCN RTKPEKRNG QH OCPPGTKUO, CPF, VJWU GSWKRRGF, VQ ECUV CDQWV HQT PGY CPF QTKIKPCN QPGU QH JKU QYP, CPF VQ YGKIJ CPF OGCUWTG CPF CRRTCKUG VJGO RTQRGTNA. KP UKOKNCT OCPPGT JG EQNNGEVGF NKUVU QH UVTQPI RJTCUGU, VJG RJTCUGU QH NKXKPI NCPIWCIG, RJTCUGU VJCV DKV NKMG CEKF CPF UEQTEJGF NKMG HNCOG, QT VJCV INQYGF CPF YGTG OGNNQY CPF NWUEKQWU KP VJG OKFUV QH VJG CTKF FGUGTV QH EQOOQP URGGEJ. JG UQWIJV CNYCAU HQT VJG RTKPEKRNG VJCV NCA DGJKPF CPF DGPGCVJ. JG YCPVGF VQ MPQY JQY VJG VJKPI YCU FQPG; CHVGT VJCV JG EQWNF FQ KV HQT JKOUGNH. JG YCU PQV EQPVGPV YKVJ VJG HCKT HCEG QH DGCWVA. JG FKUUGEVGF DGCWVA KP JKU ETQYFGF NKVVNG DGFTQQO NCDQTCVQTA, YJGTG EQQMKPI UOGNNU CNVGTPCVGF YKVJ VJG QWVGT DGFNCO QH VJG UKNXC VTKDG; CPF, JCXKPI FKUUGEVGF CPF NGCTPGF VJG CPCVQOA QH DGCWVA, JG YCU PGCTGT DGKPI CDNG VQ ETGCVG DGCWVA KVUGNH.   JG YCU UQ OCFG VJCV JG EQWNF YQTM QPNA YKVJ WPFGTUVCPFKPI. JG EQWNF PQV YQTM DNKPFNA, KP VJG FCTM, KIPQTCPV QH YJCV JG YCU RTQFWEKPI CPF VTWUVKPI VQ EJCPEG CPF VJG UVCT QH JKU IGPKWU VJCV VJG GHHGEV RTQFWEGF UJQWNF DG TKIJV CPF HKPG. JG JCF PQ RCVKGPEG YKVJ EJCPEG GHHGEVU. JG YCPVGF VQ MPQY YJA CPF JQY. JKU YCU FGNKDGTCVG ETGCVKXG IGPKWU, CPF, DGHQTG JG DGICP C UVQTA QT RQGO, VJG VJKPI KVUGNH YCU CNTGCFA CNKXG KP JKU DTCKP, YKVJ VJG GPF KP UKIJV CPF VJG OGCPU QH TGCNKBKPI VJCV GPF KP JKU EQPUEKQWU RQUUGUUKQP. QVJGTYKUG VJG GHHQTV YCU FQQOGF VQ HCKNWTG. QP VJG QVJGT JCPF, JG CRRTGEKCVGF VJG EJCPEG GHHGEVU KP YQTFU CPF RJTCUGU VJCV ECOG NKIJVNA CPF GCUKNA KPVQ JKU DTCKP, CPF VJCV NCVGT UVQQF CNN VGUVU QH DGCWVA CPF RQYGT CPF FGXGNQRGF VTGOGPFQWU CPF KPEQOOWPKECDNG EQPPQVCVKQPU. DGHQTG UWEJ JG DQYGF FQYP CPF OCTXGNNGF, MPQYKPI VJCV VJGA YGTG DGAQPF VJG FGNKDGTCVG ETGCVKQP QH CPA OCP. CPF PQ OCVVGT JQY OWEJ JG FKUUGEVGF DGCWVA KP UGCTEJ QH VJG RTKPEKRNGU VJCV WPFGTNKG DGCWVA CPF OCMG DGCWVA RQUUKDNG, JG YCU CYCTG, CNYCAU, QH VJG KPPGTOQUV OAUVGTA QH DGCWVA VQ YJKEJ JG FKF PQV RGPGVTCVG CPF VQ YJKEJ PQ OCP JCF GXGT RGPGVTCVGF. JG MPGY HWNN YGNN, HTQO JKU URGPEGT, VJCV OCP ECP PGXGT CVVCKP WNVKOCVG MPQYNGFIG QH CPAVJKPI, CPF VJCV VJG OAUVGTA QH DGCWVA YCU PQ NGUU VJCP VJCV QH NKHG-PCA, OQTG VJCV VJG HKDTGU QH DGCWVA CPF NKHG YGTG KPVGTVYKUVGF, CPF VJCV JG JKOUGNH YCU DWV C DKV QH VJG UCOG PQPWPFGTUVCPFCDNG HCDTKE, VYKUVGF QH UWPUJKPG CPF UVCT-FWUV CPF YQPFGT.   KP HCEV, KV YCU YJGP HKNNGF YKVJ VJGUG VJQWIJVU VJCV JG YTQVG JKU GUUCA GPVKVNGF UVCT-FWUV, KP YJKEJ JG JCF JKU HNKPI, PQV CV VJG RTKPEKRNGU QH ETKVKEKUO, DWV CV VJG RTKPEKRCN ETKVKEU. KV YCU DTKNNKCPV, FGGR, RJKNQUQRJKECN, CPF FGNKEKQWUNA VQWEJGF YKVJ NCWIJVGT. CNUQ KV YCU RTQORVNA TGLGEVGF DA VJG OCICBKPGU CU QHVGP CU KV YCU UWDOKVVGF. DWV JCXKPI ENGCTGF JKU OKPF QH KV, JG YGPV UGTGPGNA QP JKU YCA. KV YCU C JCDKV JG FGXGNQRGF, QH KPEWDCVKPI CPF OCVWTKPI JKU VJQWIJV WRQP C UWDLGEV, CPF QH VJGP TWUJKPI KPVQ VJG VARG-YTKVGT YKVJ KV. VJCV KV FKF PQV UGG RTKPV YCU C OCVVGT C UOCNN OQOGPV YKVJ JKO. VJG YTKVKPI QH KV YCU VJG EWNOKPCVKPI CEV QH C NQPI OGPVCN RTQEGUU, VJG FTCYKPI VQIGVJGT QH UECVVGTGF VJTGCFU QH VJQWIJV CPF VJG HKPCN IGPGTCNKBKPI WRQP CNN VJG FCVC YKVJ YJKEJ JKU OKPF YCU DWTFGPGF. VQ YTKVG UWEJ CP CTVKENG YCU VJG EQPUEKQWU GHHQTV DA YJKEJ JG HTGGF JKU OKPF CPF OCFG KV TGCFA HQT HTGUJ OCVGTKCN CPF RTQDNGOU. KV YCU KP C YCA CMKP VQ VJCV EQOOQP JCDKV QH OGP CPF YQOGP VTQWDNGF DA TGCN QT HCPEKGF ITKGXCPEGU, YJQ RGTKQFKECNNA CPF XQNWDNA DTGCM VJGKT NQPI-UWHHGTKPI UKNGPEG CPF JCXG VJGKT UCA VKNN VJG NCUV YQTF KU UCKF."
    sourceTextForCipher4 = u" THAT RUTH HAD LITTLE FAITH IN HIS POWER AS A WRITER, DID NOT ALTER HER NOR DIMINISH HER IN MARTIN’S EYES. IN THE BREATHING SPELL OF THE VACATION HE HAD TAKEN, HE HAD SPENT MANY HOURS IN SELF-ANALYSIS, AND THEREBY LEARNED MUCH OF HIMSELF. HE HAD DISCOVERED THAT HE LOVED BEAUTY MORE THAN FAME, AND THAT WHAT DESIRE HE HAD FOR FAME WAS LARGELY FOR RUTH’S SAKE. IT WAS FOR THIS REASON THAT HIS DESIRE FOR FAME WAS STRONG. HE WANTED TO BE GREAT IN THE WORLD’S EYES; TO MAKE GOOD, AS HE EXPRESSED IT, IN ORDER THAT THE WOMAN HE LOVED SHOULD BE PROUD OF HIM AND DEEM HIM WORTHY.   AS FOR HIMSELF, HE LOVED BEAUTY PASSIONATELY, AND THE JOY OF SERVING HER WAS TO HIM SUFFICIENT WAGE. AND MORE THAN BEAUTY HE LOVED RUTH. HE CONSIDERED LOVE THE FINEST THING IN THE WORLD. IT WAS LOVE THAT HAD WORKED THE REVOLUTION IN HIM, CHANGING HIM FROM AN UNCOUTH SAILOR TO A STUDENT AND AN ARTIST; THEREFORE, TO HIM, THE FINEST AND GREATEST OF THE THREE, GREATER THAN LEARNING AND ARTISTRY, WAS LOVE. ALREADY HE HAD DISCOVERED THAT HIS BRAIN WENT BEYOND RUTH’S, JUST AS IT WENT BEYOND THE BRAINS OF HER BROTHERS, OR THE BRAIN OF HER FATHER. IN SPITE OF EVERY ADVANTAGE OF UNIVERSITY TRAINING, AND IN THE FACE OF HER BACHELORSHIP OF ARTS, HIS POWER OF INTELLECT OVERSHADOWED HERS, AND HIS YEAR OR SO OF SELF-STUDY AND EQUIPMENT GAVE HIM A MASTERY OF THE AFFAIRS OF THE WORLD AND ART AND LIFE THAT SHE COULD NEVER HOPE TO POSSESS.   ALL THIS HE REALIZED, BUT IT DID NOT AFFECT HIS LOVE FOR HER, NOR HER LOVE FOR HIM. LOVE WAS TOO FINE AND NOBLE, AND HE WAS TOO LOYAL A LOVER FOR HIM TO BESMIRCH LOVE WITH CRITICISM. WHAT DID LOVE HAVE TO DO WITH RUTH’S DIVERGENT VIEWS ON ART, RIGHT CONDUCT, THE FRENCH REVOLUTION, OR EQUAL SUFFRAGE? THEY WERE MENTAL PROCESSES, BUT LOVE WAS BEYOND REASON; IT WAS SUPERRATIONAL. HE COULD NOT BELITTLE LOVE. HE WORSHIPPED IT. LOVE LAY ON THE MOUNTAIN-TOPS BEYOND THE VALLEY-LAND OF REASON. IT WAS A SUBLIMATES CONDITION OF EXISTENCE, THE TOPMOST PEAK OF LIVING, AND IT CAME RARELY. THANKS TO THE SCHOOL OF SCIENTIFIC PHILOSOPHERS HE FAVORED, HE KNEW THE BIOLOGICAL SIGNIFICANCE OF LOVE; BUT BY A REFINED PROCESS OF THE SAME SCIENTIFIC REASONING HE REACHED THE CONCLUSION THAT THE HUMAN ORGANISM ACHIEVED ITS HIGHEST PURPOSE IN LOVE, THAT LOVE MUST NOT BE QUESTIONED, BUT MUST BE ACCEPTED AS THE HIGHEST GUERDON OF LIFE. THUS, HE CONSIDERED THE LOVER BLESSED OVER ALL CREATURES, AND IT WAS A DELIGHT TO HIM TO THINK OF GOD’S OWN MAD LOVER, RISING ABOVE THE THINGS OF EARTH, ABOVE WEALTH AND JUDGMENT, PUBLIC OPINION AND APPLAUSE, RISING ABOVE LIFE ITSELF AND DYING ON A KISS.   MUCH OF THIS MARTIN HAD ALREADY REASONED OUT, AND SOME OF IT HE REASONED OUT LATER. IN THE MEANTIME HE WORKED, TAKING NO RECREATION EXCEPT WHEN HE WENT TO SEE RUTH, AND LIVING LIKE A SPARTAN. HE PAID TWO DOLLARS AND A HALF A MONTH RENT FOR THE SMALL ROOM HE GOT FROM HIS PORTUGUESE LANDLADY, MARIA SILVA, A VIRAGO AND A WIDOW, HARD WORKING AND HARSHER TEMPERED, REARING HER LARGE BROOD OF CHILDREN SOMEHOW, AND DROWNING HER SORROW AND FATIGUE AT IRREGULAR INTERVALS IN A GALLON OF THE THIN, SOUR WINE THAT SHE BOUGHT FROM THE CORNER GROCERY AND SALOON FOR FIFTEEN CENTS. FROM DETESTING HER AND HER FOUL TONGUE AT FIRST, MARTIN GREW TO ADMIRE HER AS HE OBSERVED THE BRAVE FIGHT SHE MADE. THERE WERE BUT FOUR ROOMS IN THE LITTLE HOUSE-THREE, WHEN MARTIN’S WAS SUBTRACTED. ONE OF THESE, THE PARLOR, GAY WITH AN INGRAIN CARPET AND DOLOROUS WITH A FUNERAL CARD AND A DEATH-PICTURE OF ONE OF HER NUMEROUS DEPARTED BABES, WAS KEPT STRICTLY FOR COMPANY. THE BLINDS WERE ALWAYS DOWN, AND HER BAREFOOTED TRIBE WAS NEVER PERMITTED TO ENTER THE SACRED PRECINCT SAVE ON STATE OCCASIONS. SHE COOKED, AND ALL ATE, IN THE KITCHEN, WHERE SHE LIKEWISE WASHED, STARCHED, AND IRONED CLOTHES ON ALL DAYS OF THE WEEK EXCEPT SUNDAY; FOR HER INCOME CAME LARGELY FROM TAKING IN WASHING FROM HER MORE PROSPEROUS NEIGHBORS. REMAINED THE BEDROOM, SMALL AS THE ONE OCCUPIED BY MARTIN, INTO WHICH SHE AND HER SEVEN LITTLE ONES CROWDED AND SLEPT. IT WAS AN EVERLASTING MIRACLE TO MARTIN HOW IT WAS ACCOMPLISHED, AND FROM HER SIDE OF THE THIN PARTITION HE HEARD NIGHTLY EVERY DETAIL OF THE GOING TO BED, THE SQUALLS AND SQUABBLES, THE SOFT CHATTERING, AND THE SLEEPY, TWITTERING NOISES AS OF BIRDS. ANOTHER SOURCE OF INCOME TO MARIA WERE HER COWS, TWO OF THEM, WHICH SHE MILKED NIGHT AND MORNING AND WHICH GAINED A SURREPTITIOUS LIVELIHOOD FROM VACANT LOTS AND THE GRASS THAT GREW ON EITHER SIDE THE PUBLIC SIDE WALKS, ATTENDED ALWAYS BY ONE OR MORE OF HER RAGGED BOYS, WHOSE WATCHFUL GUARDIANSHIP CONSISTED CHIEFLY IN KEEPING THEIR EYES OUT FOR THE POUNDMEN.   IN HIS OWN SMALL ROOM MARTIN LIVED, SLEPT, STUDIED, WROTE, AND KEPT HOUSE. BEFORE THE ONE WINDOW, LOOKING OUT ON THE TINY FRONT PORCH, WAS THE KITCHEN TABLE THAT SERVED AS DESK, LIBRARY, AND TYPE-WRITING STAND. THE BED, AGAINST THE REAR WALL, OCCUPIED TWO-THIRDS OF THE TOTAL SPACE OF THE ROOM. THE TABLE WAS FLANKED ON ONE SIDE BY A GAUDY BUREAU, MANUFACTURED FOR PROFIT AND NOT FOR SERVICE, THE THIN VENEER OF WHICH WAS SHED DAY BY DAY. THIS BUREAU STOOD IN THE CORNER, AND IN THE OPPOSITE CORNER, ON THE TABLE’S OTHER FLANK, WAS THE KITCHEN-THE OIL-STOVE ON A DRY-GOODS BOX, INSIDE OF WHICH WERE DISHES AND COOKING UTENSILS, A SHELF ON THE WALL FOR PROVISIONS, AND A BUCKET OF WATER ON THE FLOOR. MARTIN HAD TO CARRY HIS WATER FROM THE KITCHEN SINK, THERE BEING NO TAP IN HIS ROOM. ON DAYS WHEN THERE WAS MUCH STEAM TO HIS COOKING, THE HARVEST OF VENEER FROM THE BUREAU WAS UNUSUALLY GENEROUS. OVER THE BED, HOISTED BY A TACKLE TO THE CEILING, WAS HIS BICYCLE. AT FIRST HE HAD TRIED TO KEEP IT IN THE BASEMENT; BUT THE TRIBE OF SILVA, LOOSENING THE BEARINGS AND PUNCTURING THE TIRES, HAD DRIVEN HIM OUT. NEXT HE ATTEMPTED THE TINY FRONT PORCH, UNTIL A HOWLING SOUTHEASTER DRENCHED THE WHEEL A NIGHT-LONG. THEN HE HAD RETREATED WITH IT TO HIS ROOM AND SLUNG IT ALOFT.   A SMALL CLOSET CONTAINED HIS CLOTHES AND THE BOOKS HE HAD ACCUMULATED AND FOR WHICH THERE WAS NO ROOM ON THE TABLE OR UNDER THE TABLE. HAND IN HAND WITH READING, HE HAD DEVELOPED THE HABIT OF MAKING NOTES, AND SO COPIOUSLY DID HE MAKE THEM THAT THERE WOULD HAVE BEEN NO EXISTENCE FOR HIM IN THE CONFINED QUARTERS HAD HE NOT RIGGED SEVERAL CLOTHES-LINES ACROSS THE ROOM ON WHICH THE NOTES WERE HUNG. EVEN SO, HE WAS CROWDED UNTIL NAVIGATING THE ROOM WAS A DIFFICULT TASK. HE COULD NOT OPEN THE DOOR WITHOUT FIRST CLOSING THE CLOSET DOOR, AND VICE VERSA . IT WAS IMPOSSIBLE FOR HIM ANYWHERE TO TRAVERSE THE ROOM IN A STRAIGHT LINE. TO GO FROM THE DOOR TO THE HEAD OF THE BED WAS A ZIGZAG COURSE THAT HE WAS NEVER QUITE ABLE TO ACCOMPLISH IN THE DARK WITHOUT COLLISIONS. HAVING SETTLED THE DIFFICULTY OF THE CONFLICTING DOORS, HE HAD TO STEER SHARPLY TO THE RIGHT TO AVOID THE KITCHEN. NEXT, HE SHEERED TO THE LEFT, TO ESCAPE THE FOOT OF THE BED; BUT THIS SHEER, IF TOO GENEROUS, BROUGHT HIM AGAINST THE CORNER OF THE TABLE. WITH A SUDDEN TWITCH AND LURCH, HE TERMINATED THE SHEER AND BORE OFF TO THE RIGHT ALONG A SORT OF CANAL, ONE BANK OF WHICH WAS THE BED, THE OTHER THE TABLE. WHEN THE ONE CHAIR IN THE ROOM WAS AT ITS USUAL PLACE BEFORE THE TABLE, THE CANAL WAS UNNAVIGABLE. WHEN THE CHAIR WAS NOT IN USE, IT REPOSED ON TOP OF THE BED, THOUGH SOMETIMES HE SAT ON THE CHAIR WHEN COOKING, READING A BOOK WHILE THE WATER BOILED, AND EVEN BECOMING SKILFUL ENOUGH TO MANAGE A PARAGRAPH OR TWO WHILE STEAK WAS FRYING. ALSO, SO SMALL WAS THE LITTLE CORNER THAT CONSTITUTED THE KITCHEN, HE WAS ABLE, SITTING DOWN, TO REACH ANYTHING HE NEEDED. IN FACT, IT WAS EXPEDIENT TO COOK SITTING DOWN; STANDING UP, HE WAS TOO OFTEN IN HIS OWN WAY.   IN CONJUNCTION WITH A PERFECT STOMACH THAT COULD DIGEST ANYTHING, HE POSSESSED KNOWLEDGE OF THE VARIOUS FOODS THAT WERE AT THE SAME TIME NUTRITIOUS AND CHEAP. PEA-SOUP WAS A COMMON ARTICLE IN HIS DIET, AS WELL AS POTATOES AND BEANS, THE LATTER LARGE AND BROWN AND COOKED IN MEXICAN STYLE. RICE, COOKED AS AMERICAN HOUSEWIVES NEVER COOK IT AND CAN NEVER LEARN TO COOK IT, APPEARED ON MARTIN’S TABLE AT LEAST ONCE A DAY. DRIED FRUITS WERE LESS EXPENSIVE THAN FRESH, AND HE HAD USUALLY A POT OF THEM, COOKED AND READY AT HAND, FOR THEY TOOK THE PLACE OF BUTTER ON HIS BREAD. OCCASIONALLY HE GRACED HIS TABLE WITH A PIECE OF ROUND-STEAK, OR WITH A SOUP-BONE. COFFEE, WITHOUT CREAM OR MILK, HE HAD TWICE A DAY, IN THE EVENING SUBSTITUTING TEA; BUT BOTH COFFEE AND TEA WERE EXCELLENTLY COOKED.   THERE WAS NEED FOR HIM TO BE ECONOMICAL. HIS VACATION HAD CONSUMED NEARLY ALL HE HAD EARNED IN THE LAUNDRY, AND HE WAS SO FAR FROM HIS MARKET THAT WEEKS MUST ELAPSE BEFORE HE COULD HOPE FOR THE FIRST RETURNS FROM HIS HACK-WORK. EXCEPT AT SUCH TIMES AS HE SAW RUTH, OR DROPPED IN TO SEE HIS SISTER GERTUDE, HE LIVED A RECLUSE, IN EACH DAY ACCOMPLISHING AT LEAST THREE DAYS’ LABOR OF ORDINARY MEN. HE SLEPT A SCANT FIVE HOURS, AND ONLY ONE WITH A CONSTITUTION OF IRON COULD HAVE HELD HIMSELF DOWN, AS MARTIN DID, DAY AFTER DAY, TO NINETEEN CONSECUTIVE HOURS OF TOIL. HE NEVER LOST A MOMENT. ON THE LOOKING-GLASS WERE LISTS OF DEFINITIONS AND PRONUNCIATIONS; WHEN SHAVING, OR DRESSING, OR COMBING HIS HAIR, HE CONNED THESE LISTS OVER. SIMILAR LISTS WERE ON THE WALL OVER THE OIL-STOVE, AND THEY WERE SIMILARLY CONNED WHILE HE WAS ENGAGED IN COOKING OR IN WASHING THE DISHES. NEW LISTS CONTINUALLY DISPLACED THE OLD ONES. EVERY STRANGE OR PARTLY FAMILIAR WORD ENCOUNTERED IN HIS READING WAS IMMEDIATELY JOTTED DOWN, AND LATER, WHEN A SUFFICIENT NUMBER HAD BEEN ACCUMULATED, WERE TYPED AND PINNED TO THE WALL OR LOOKING-GLASS. HE EVEN CARRIED THEM IN HIS POCKETS, AND REVIEWED THEM AT ODD MOMENTS ON THE STREET, OR WHILE WAITING IN BUTCHER SHOP OR GROCERY TO BE SERVED.   HE WENT FARTHER IN THE MATTER. READING THE WORKS OF MEN WHO HAD ARRIVED, HE NOTED EVERY RESULT ACHIEVED BY THEM, AND WORKED OUT THE TRICKS BY WHICH THEY HAD BEEN ACHIEVED-THE TRICKS OF NARRATIVE, OF EXPOSITION, OF STYLE, THE POINTS OF VIEW, THE CONTRASTS, THE EPIGRAMS; AND OF ALL THESE HE MADE LISTS FOR STUDY. HE DID NOT APE. HE SOUGHT PRINCIPLES. HE DREW UP LISTS OF EFFECTIVE AND FETCHING MANNERISMS, TILL OUT OF MANY SUCH, CULLED FROM MANY WRITERS, HE WAS ABLE TO INDUCE THE GENERAL PRINCIPLE OF MANNERISM, AND, THUS EQUIPPED, TO CAST ABOUT FOR NEW AND ORIGINAL ONES OF HIS OWN, AND TO WEIGH AND MEASURE AND APPRAISE THEM PROPERLY. IN SIMILAR MANNER HE COLLECTED LISTS OF STRONG PHRASES, THE PHRASES OF LIVING LANGUAGE, PHRASES THAT BIT LIKE ACID AND SCORCHED LIKE FLAME, OR THAT GLOWED AND WERE MELLOW AND LUSCIOUS IN THE MIDST OF THE ARID DESERT OF COMMON SPEECH. HE SOUGHT ALWAYS FOR THE PRINCIPLE THAT LAY BEHIND AND BENEATH. HE WANTED TO KNOW HOW THE THING WAS DONE; AFTER THAT HE COULD DO IT FOR HIMSELF. HE WAS NOT CONTENT WITH THE FAIR FACE OF BEAUTY. HE DISSECTED BEAUTY IN HIS CROWDED LITTLE BEDROOM LABORATORY, WHERE COOKING SMELLS ALTERNATED WITH THE OUTER BEDLAM OF THE SILVA TRIBE; AND, HAVING DISSECTED AND LEARNED THE ANATOMY OF BEAUTY, HE WAS NEARER BEING ABLE TO CREATE BEAUTY ITSELF.   HE WAS SO MADE THAT HE COULD WORK ONLY WITH UNDERSTANDING. HE COULD NOT WORK BLINDLY, IN THE DARK, IGNORANT OF WHAT HE WAS PRODUCING AND TRUSTING TO CHANCE AND THE STAR OF HIS GENIUS THAT THE EFFECT PRODUCED SHOULD BE RIGHT AND FINE. HE HAD NO PATIENCE WITH CHANCE EFFECTS. HE WANTED TO KNOW WHY AND HOW. HIS WAS DELIBERATE CREATIVE GENIUS, AND, BEFORE HE BEGAN A STORY OR POEM, THE THING ITSELF WAS ALREADY ALIVE IN HIS BRAIN, WITH THE END IN SIGHT AND THE MEANS OF REALIZING THAT END IN HIS CONSCIOUS POSSESSION. OTHERWISE THE EFFORT WAS DOOMED TO FAILURE. ON THE OTHER HAND, HE APPRECIATED THE CHANCE EFFECTS IN WORDS AND PHRASES THAT CAME LIGHTLY AND EASILY INTO HIS BRAIN, AND THAT LATER STOOD ALL TESTS OF BEAUTY AND POWER AND DEVELOPED TREMENDOUS AND INCOMMUNICABLE CONNOTATIONS. BEFORE SUCH HE BOWED DOWN AND MARVELLED, KNOWING THAT THEY WERE BEYOND THE DELIBERATE CREATION OF ANY MAN. AND NO MATTER HOW MUCH HE DISSECTED BEAUTY IN SEARCH OF THE PRINCIPLES THAT UNDERLIE BEAUTY AND MAKE BEAUTY POSSIBLE, HE WAS AWARE, ALWAYS, OF THE INNERMOST MYSTERY OF BEAUTY TO WHICH HE DID NOT PENETRATE AND TO WHICH NO MAN HAD EVER PENETRATED. HE KNEW FULL WELL, FROM HIS SPENCER, THAT MAN CAN NEVER ATTAIN ULTIMATE KNOWLEDGE OF ANYTHING, AND THAT THE MYSTERY OF BEAUTY WAS NO LESS THAN THAT OF LIFE-NAY, MORE THAT THE FIBRES OF BEAUTY AND LIFE WERE INTERTWISTED, AND THAT HE HIMSELF WAS BUT A BIT OF THE SAME NONUNDERSTANDABLE FABRIC, TWISTED OF SUNSHINE AND STAR-DUST AND WONDER.   IN FACT, IT WAS WHEN FILLED WITH THESE THOUGHTS THAT HE WROTE HIS ESSAY ENTITLED STAR-DUST, IN WHICH HE HAD HIS FLING, NOT AT THE PRINCIPLES OF CRITICISM, BUT AT THE PRINCIPAL CRITICS. IT WAS BRILLIANT, DEEP, PHILOSOPHICAL, AND DELICIOUSLY TOUCHED WITH LAUGHTER. ALSO IT WAS PROMPTLY REJECTED BY THE MAGAZINES AS OFTEN AS IT WAS SUBMITTED. BUT HAVING CLEARED HIS MIND OF IT, HE WENT SERENELY ON HIS WAY. IT WAS A HABIT HE DEVELOPED, OF INCUBATING AND MATURING HIS THOUGHT UPON A SUBJECT, AND OF THEN RUSHING INTO THE TYPE-WRITER WITH IT. THAT IT DID NOT SEE PRINT WAS A MATTER A SMALL MOMENT WITH HIM. THE WRITING OF IT WAS THE CULMINATING ACT OF A LONG MENTAL PROCESS, THE DRAWING TOGETHER OF SCATTERED THREADS OF THOUGHT AND THE FINAL GENERALIZING UPON ALL THE DATA WITH WHICH HIS MIND WAS BURDENED. TO WRITE SUCH AN ARTICLE WAS THE CONSCIOUS EFFORT BY WHICH HE FREED HIS MIND AND MADE IT READY FOR FRESH MATERIAL AND PROBLEMS. IT WAS IN A WAY AKIN TO THAT COMMON HABIT OF MEN AND WOMEN TROUBLED BY REAL OR FANCIED GRIEVANCES, WHO PERIODICALLY AND VOLUBLY BREAK THEIR LONG-SUFFERING SILENCE AND HAVE THEIR SAY TILL THE LAST WORD IS SAID."
    cipherLetters = u""
    for i in range(cipher.__len__()):
         if pattern.match(cipher[i]):
             cipherLetters += cipher[i]
    # !!!!!!!!!!!!!! epta
    keyLen = 2

    # keyLen not always good
    frequencyAnalysis(cipher4, keyLen)
    print cipher4
    print sourceTextForCipher4

