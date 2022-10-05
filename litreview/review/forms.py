from django import forms
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()


class TicketForm(forms.ModelForm):
    """
    on créé notre model de formulaire TicketForm

    Args:
        forms (object): on hérite du model de formulaire de django
    """

    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ["headline", "body"]
        labels = {"headline": "Titre", "body": "Description"}


class ReviewForm(forms.ModelForm):
    """
    on créé notre model de formulaire ReviewForm

    Args:
        forms (object): on hérite du model de formulaire de django
    """

    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ["headline", "body"]
        labels = {"headline": "Titre", "body": "Commentaire"}


class DeleteTicketReviewForm(forms.Form):
    """
    on créé notre model de formulaire DeleteTicketReviewForm

    Args:
        forms (object): on hérite du model de formulaire de django
    """

    delete_ticket_or_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class FollowUsersForm(forms.ModelForm):
    """
    on créé notre model de formulaire FollowUsersForm

    Args:
        forms (object): on hérite du model de formulaire de django
    """

    class Meta:
        model = models.UserFollows
        fields = ["followed_user"]
