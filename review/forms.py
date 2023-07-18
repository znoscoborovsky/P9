from django import forms
from django.contrib.auth import get_user_model
from . import models
User = get_user_model()

class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']

class DeleteTicket(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)