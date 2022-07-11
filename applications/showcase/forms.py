from django import forms


class SearchProductsForm(forms.Form):
    search_input = forms.CharField(label="")
