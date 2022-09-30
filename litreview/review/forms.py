from django import forms
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()

class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = models.Ticket
        fields = ['headline', 'body']
        labels = {
            'headline': 'Titre',
            'body': 'Description'
        }

class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image']
    
class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = models.Review
        fields = ['headline','body']
        labels = {
            'headline': 'Titre',
            'body': 'Commentaire'
        }

class DeleteTicketReviewForm(forms.Form):
    delete_ticket_or_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ['followed_user']
        