from django import forms


class PersonalLinkForm(forms.Form):
    full_link = forms.URLField(label='', min_length=1, required=True)
    short_link = forms.URLField(label='', min_length=1, required=True)


class LinkForm(forms.Form):
    full_link = forms.URLField(label='', min_length=1, required=True)

