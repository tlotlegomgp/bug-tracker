from django import forms
from account.models import Profile
from .models import Ticket, TicketAssignee


select_styling = 'form-control form-control-sm custom-select custom-select-sm'


class TicketForm(forms.Form):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'name': "name", 'required': ""}))
    description = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class': 'form-control', 'name': "description", 'required': ""}))
    status = forms.ChoiceField(choices=Ticket.TICKET_STATUS, widget=forms.Select(attrs={'class': select_styling}), label_suffix="")
    priority = forms.ChoiceField(choices=Ticket.TICKET_PRIORITY, widget=forms.Select(attrs={'class': select_styling, }), label_suffix="")
    class_type = forms.ChoiceField(choices=Ticket.TICKET_TYPE, widget=forms.Select(attrs={'class': select_styling}), label_suffix="")
    assignee = forms.ChoiceField(choices=((u.id, u.first_name + " " + u.last_name)
                                          for u in Profile.objects.all()), widget=forms.Select(attrs={'class': select_styling}))
    user_role = forms.ChoiceField(choices=TicketAssignee.ROLE, widget=forms.Select(attrs={'class': select_styling}), label_suffix="")


class TicketCommentForm(forms.Form):
    comment = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'name': "comment"}))


class TicketAttachmentForm(forms.Form):
    attachment = forms.FileField(widget=forms.FileInput(attrs={'style': "border-color: rgb(28, 40, 38)"}))
    note = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'name': "address"}), required=False)
