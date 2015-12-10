from django import forms
from decriptor.models import Lang


class InputTextForm(forms.Form):

    LANG_CHOISE = (
    (Lang.ru, 'ru'),
    (Lang.en, 'en'),
    (Lang.fr, 'fr'),
    )

    text = forms.CharField(widget=forms.Textarea)
    lang = forms.ChoiceField(choices=LANG_CHOISE, widget=forms.RadioSelect())
    keyLen = forms.CharField()