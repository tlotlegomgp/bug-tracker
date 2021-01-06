from django import forms


select_styling = 'form-control form-control-sm custom-select custom-select-sm'

CHOICES = (
    ('False', 'False'),
    ('True', 'True'),

)


class UserForm(forms.Form):

    is_active = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': select_styling}))
    is_staff = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': select_styling}))
    is_admin = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': select_styling}))


class MessageForm(forms.Form):
    message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)
