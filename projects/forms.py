from django import forms


class ProjectForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'name': "name", 'required': ""}))
    description = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class': 'form-control', 'name': "description", 'required': ""}))
