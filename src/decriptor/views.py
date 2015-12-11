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


cypherArray = "dglsobmtsdgmrgkoerjheiorhjakmsldfk"

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
            raw.keyLen = algoritm.algKeyTest.key_count(text)
            newKeylen = algoritm.algKey.key_count(text)
            if raw.lang == Lang.en:
                list = algoritm.englishCrack.decipherEnglish(newText1, raw.keyLen[0])
            elif raw.lang == Lang.ru:
                list = algoritm.englishCrack.decipherEnglish(newText1, raw.keyLen[0])
            elif raw.lang == Lang.de:
                list = algoritm.englishCrack.decipherEnglish(newText1, raw.keyLen[0])
            newText = list[0]
            raw.mappingFunctions = list[1]
        elif 'encrypt' in request.POST:
            print  "encrypt"
            newText1 = algoritm.alg.deleteChangeBadSymbols(text)
            keyLen = int(form.cleaned_data['keyLen'])
            raw.keyLen.append(keyLen)
            if raw.lang == Lang.en:
                newText = algoritm.cipher.main(newText1, cypherArray[0:keyLen])
            elif raw.lang == Lang.ru:
                newText = algoritm.cipher.main(newText1, cypherArray[0:keyLen])
            elif raw.lang == Lang.de:
                newText = algoritm.cipher.main(newText1, cypherArray[0:keyLen])
        print  raw.keyLen
        raw.text = newText
        context = {'rawText' : raw}
        print newKeylen
        return render(request, "result.html", context)
    return render(request,
        "input.html", {"form" : form }
        )