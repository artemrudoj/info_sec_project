from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from decriptor.forms import InputTextForm
from decriptor.models import SourceText


class HomePage(TemplateView):
    template_name = "input.html"

class ResultPage(TemplateView):
    template_name = "result.html"

def get_text(request):
    print 1
    form = InputTextForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        print 2
        raw = SourceText(
            text=form.cleaned_data['text'],
            lang=form.cleaned_data['lang']
        )
        context = {'rawText' : raw}
        return render(request, "result.html", context)
    return render(request,
        "input.html", {"form" : form }
        )