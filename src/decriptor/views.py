# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render
from decriptor.forms import InputTextForm
from decriptor.models import SourceText, Lang
import algoritm.alg
import algoritm.cipher
import algoritm.algArtem
import algoritm.algKey
import algoritm.algKeyTest
import algoritm.englishCrack
import algoritm.russianCipher
import algoritm.russian
import algoritm.tools

cypherArray = u"dglsobmtsdgmrgkoerjheiorhjakmsldfk"
russianArray = u"АБ"

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
            newText1 = algoritm.alg.deleteChangeBadSymbols(text)
            # raw.keyLen = algoritm.algKeyTest.key_count(text)
            # newKeylen = algoritm.algKey.key_count(text)
            raw.keyLen.append(2)
            newKeylen.append(2)
            if raw.lang == Lang.en:
                list = algoritm.englishCrack.decipherEnglish(newText1, raw.keyLen[0])
            elif int(raw.lang) == int(Lang.ru):
                list = algoritm.russian.decipherRussian(newText1, raw.keyLen[0])
            elif raw.lang == Lang.de:
                list = algoritm.englishCrack.decipherEnglish(newText1, raw.keyLen[0])
            newText = list[0]
            raw.mappingFunctions = list[1]
        elif 'encrypt' in request.POST:
            print  "encrypt"
            newText1 = algoritm.alg.deleteChangeBadSymbols(text)
            keyLen = int(form.cleaned_data['keyLen'])
            raw.keyLen.append(keyLen)
            print "asdasd"
            if int(raw.lang) == int(Lang.en):
                print "1"
                newText = algoritm.cipher.main(newText1, cypherArray[0:keyLen])
            elif int(raw.lang) == int(Lang.ru):
                print "asdasd"
                newText1 = algoritm.tools.deleteE(newText1)
                newText = algoritm.russianCipher.main(newText1, russianArray[0:keyLen])
            elif raw.lang == Lang.de:
                print "2"
                newText = algoritm.cipher.main(newText1, cypherArray[0:keyLen])
        print "22"
        print  raw.keyLen
        raw.text = newText
        context = {'rawText' : raw}
        print newKeylen
        return render(request, "result.html", context)
    return render(request,
        "input.html", {"form" : form }
        )