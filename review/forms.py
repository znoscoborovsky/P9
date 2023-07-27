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

class ReviewForm(forms.ModelForm):
    CHOICES = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = models.Review
        fields = ['headline', 'body', 'rating']

class DeleteReview(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class FollowerForm(forms.ModelForm):
    #select_user_to_follow = forms.CharField()
    class Meta:
        model = models.UserFollows
        fields = ['followed_user']
