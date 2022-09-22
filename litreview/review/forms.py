from django import forms

from . import models


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = models.Ticket
        fields = ['headline', 'body']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image']
    
class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']

class DeleteTicketReviewForm(forms.Form):
    delete_ticket_or_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

