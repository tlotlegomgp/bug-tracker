from django import forms
from account.models import Profile

select_styling = 'form-control form-control-sm custom-select custom-select-sm'


class ProjectForm(forms.Form):

    MANAGER_CHOICES = ((str(p.id), p.first_name + " " + p.last_name) for p in Profile.objects.all().order_by('first_name'))
    MEMBER_CHOICES = ((str(p.id), p.first_name + " " + p.last_name) for p in Profile.objects.all().order_by('first_name'))

    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'name': "name", 'required': ""}))
    description = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class': 'form-control', 'name': "description", 'required': ""}))
    manager = forms.ChoiceField(choices=MANAGER_CHOICES, widget=forms.Select(attrs={'class': select_styling}))
    members = forms.MultipleChoiceField(choices=MEMBER_CHOICES, widget=forms.SelectMultiple(attrs={'class': select_styling}))
