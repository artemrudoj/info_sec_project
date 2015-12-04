from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from decriptor.forms import InputTextForm
from decriptor.models import SourceText
import algoritm.alg
import algoritm.cipher



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
        print raw.text
        text = unicode(raw.text)
        print raw.lang
        if (raw.lang == '0'):
            newText1 = algoritm.alg.deleteChangeBadSymbols(text)
            newText = algoritm.cipher.main(newText1, 'sfgtrd')
        else :
            newText1 = algoritm.alg.deleteChangeBadSymbols(text)
            newText = algoritm.alg.frequencyAnalysis(newText1, 6)
            print "asd"
        raw.text = newText
        context = {'rawText' : raw}
        return render(request, "result.html", context)
    return render(request,
        "input.html", {"form" : form }
        )