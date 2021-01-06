from django import forms


class TodoForm(forms.Form):
    todo = forms.CharField(max_length=80, widget=forms.TextInput(attrs={'class': 'form-control', 'name': "todo"}))


class ConversationForm(forms.Form):
    message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'form-control', 'name': "message", 'style': 'max-height: 120px; min-height: 120px;'}))