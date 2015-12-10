from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from decriptor.forms import InputTextForm
from decriptor.models import SourceText
import algoritm.alg
import algoritm.cipher
import algoritm.algArtem
import algoritm.algNormal
import algoritm.algKey


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
        if 'decrypt' in request.POST:
            print "decrypt"
            newText1 = algoritm.alg.deleteChangeBadSymbols(text)
            keyLen = algoritm.algKey.key_count(text)
            print keyLen
            newText = algoritm.algNormal.decipherEnglish(newText1, keyLen)
        elif 'encrypt' in request.POST:
            print  "encrypt"
            newText1 = algoritm.alg.deleteChangeBadSymbols(text)
            keyLen = int(form.cleaned_data['keyLen'])
            newText = algoritm.cipher.main(newText1, cypherArray[0:keyLen])


        raw.text = newText
        context = {'rawText' : raw}
        return render(request, "result.html", context)
    return render(request,
        "input.html", {"form" : form }
        )