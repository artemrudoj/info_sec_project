# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render
from decriptor.forms import InputTextForm
from decriptor.models import SourceText, Lang
import algoritm.cipher
import algoritm.algArtem
import algoritm.algKey
import algoritm.algKeyTest
import algoritm.englishCrack
import algoritm.russianCipher
import algoritm.russian
import algoritm.tools
import algoritm.germanCrack
cypherArray = u"dglsobmtsdgmrgkoerjheiorhjakmsldfk"
russianArray = u"АБДБИЬФИФБЙЦАЙЦЗАБЦЙЗЩА"

class HomePage(TemplateView):
    template_name = "input.html"

class ResultPage(TemplateView):
    template_name = "result.html"

def get_text(request):
    form = InputTextForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        raw = SourceText(
            text=form.cleaned_data['text'],
            lang=form.cleaned_data['lang']
        )
        text = unicode(raw.text)
        newText = ""
        newKeylen = []
        if 'decrypt' in request.POST:
            print "decrypt"
            newText1 = algoritm.tools.deleteChangeBadSymbols(text)
            if int(raw.lang) == (Lang.en):
                raw.keyLen = algoritm.algKeyTest.key_count(text, 1)
                list = algoritm.englishCrack.decipherEnglish(newText1, raw.keyLen[0])
            elif int(raw.lang) == int(Lang.ru):
                raw.keyLen = algoritm.algKeyTest.key_count(text, 0)
                print raw.keyLen
                list = algoritm.russian.decipherRussian(newText1, raw.keyLen[0])
            elif int(raw.lang) == int(Lang.de):
                raw.keyLen = algoritm.algKeyTest.key_count(text, 2)
                list = algoritm.germanCrack.decipherGerman(newText1, raw.keyLen[0])
            newText = list[0]
            raw.mappingFunctions = list[1]
        elif 'encrypt' in request.POST:
            print  "encrypt"
            newText1 = algoritm.tools.deleteChangeBadSymbols(text)
            keyLen = int(form.cleaned_data['keyLen'])
            raw.keyLen.append(keyLen)
            print "asdasd"
            if int(raw.lang) == int(Lang.en):
                print "1"
                newText = algoritm.tools.superEncrytor(newText1, keyLen, algoritm.englishCrack.usualEnglishLettersRate)
            elif int(raw.lang) == int(Lang.ru):
                print "asdasd"
                newText1 = algoritm.tools.deleteE(newText1)
                newText = algoritm.tools.superEncrytor(newText1, keyLen, algoritm.russian.usualRussianLettersRate)
            elif int(raw.lang) == int(Lang.de):
                print "2"
                newText = algoritm.tools.superEncrytor(newText1, keyLen, algoritm.germanCrack.usualGermanLettersRate)
        print "22"
        print  raw.keyLen
        raw.text = newText
        context = {'rawText' : raw}
        print newKeylen
        return render(request, "result.html", context)
    return render(request,
        "input.html", {"form" : form }
        )