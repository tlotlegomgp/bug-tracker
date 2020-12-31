from django import forms
from account.models import Profile

select_styling = 'form-control form-control-sm custom-select custom-select-sm'

ROLE_CHOICES = (
    ('Developer', 'Developer'),
    ('Submitter', 'Submitter')
)

MANAGER_CHOICES = ((str(p.id), p.first_name + " " + p.last_name) for p in Profile.objects.all().order_by('first_name'))
MEMBER_CHOICES = ((str(p.id), p.first_name + " " + p.last_name) for p in Profile.objects.all().order_by('first_name'))


class ProjectForm(forms.Form):

    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'name': "name", 'required': ""}))
    description = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class': 'form-control', 'name': "description", 'required': ""}))
    manager = forms.ChoiceField(choices=MANAGER_CHOICES, widget=forms.Select(attrs={'class': select_styling}))
    members = forms.MultipleChoiceField(choices=MEMBER_CHOICES, widget=forms.SelectMultiple(attrs={'class': select_styling}))


class ProjectRolesForm(forms.Form):
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': select_styling}))
    members = forms.MultipleChoiceField(choices=((str(p.id), p.first_name + " " + p.last_name)
                                                 for p in Profile.objects.all().order_by('first_name')), widget=forms.SelectMultiple(attrs={'class': select_styling}))
