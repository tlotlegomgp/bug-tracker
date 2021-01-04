from django import forms


class TodoForm(forms.Form):
    todo = forms.CharField(max_length=80, widget=forms.TextInput(attrs={'class': 'form-control', 'name': "todo", 'style': 'border-color: rgb(28, 40, 38);'}))