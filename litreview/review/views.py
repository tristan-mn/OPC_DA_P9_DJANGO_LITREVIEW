from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Value, CharField, Q
from django.contrib import messages

from review import forms, models

from authentication import models as authentication_models
# Create your views here.

@login_required
def create_ticket(request):
    ticket_form = forms.TicketForm()
    photo_form = forms.PhotoForm()
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            ticket = ticket_form.save(commit=False)
            ticket.photo = photo
            ticket.author = request.user
            ticket.save()
            return redirect('flux')

    context = {
        'ticket_form': ticket_form,
        'photo_form': photo_form,
    }

    return render(request, 'review/create_ticket.html', context=context)



@login_required
def create_review_and_ticket(request):
    ticket_form = forms.TicketForm()
    photo_form = forms.PhotoForm()
    review_form = forms.ReviewForm()
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(),
                photo_form.is_valid(),
                review_form.is_valid()]):
                photo = photo_form.save(commit=False)
                photo.uploader = request.user
                photo.save()
                ticket = ticket_form.save(commit=False)
                ticket.photo = photo
                ticket.author = request.user
                ticket.save()
                review = review_form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                return redirect('flux')
    context = {
        'ticket_form': ticket_form,
        'photo_form': photo_form,
        'review_form': review_form,
    }

    return render(request, 'review/create_review_and_ticket.html', context=context)



@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
        return redirect('flux')
    context = {
            'review_form' : review_form,
            'ticket': ticket,
        }
    return render(request, 'review/create_review.html', context=context)



@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteTicketReviewForm()
    if request.method == 'POST':
        print(request.POST)
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('display_posts')
        if 'delete_ticket_or_review' in request.POST:
            delete_form = forms.DeleteTicketReviewForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('display_posts')
    
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'review/edit_ticket.html', context=context)



@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    delete_form = forms.DeleteTicketReviewForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('display_posts')
        if 'delete_ticket_or_review' in request.POST:
            delete_form = forms.DeleteTicketReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('display_posts')
    
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'review/edit_review.html', context=context)



@login_required
def display_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    return render(request, 'review/display_review.html', {'review': review})


@login_required
def display_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'review/display_ticket.html', {'ticket': ticket})


@login_required
def display_posts(request):
    tickets = models.Ticket.objects.filter(author=request.user)
    reviews = models.Review.objects.filter(user=request.user)

    tickets_sorted = sorted(tickets, key=lambda instance: instance.date_created, reverse=True)
    reviews_sorted = sorted(reviews, key=lambda instance: instance.date_created, reverse=True)
    context = {
        'tickets': tickets_sorted,
        'reviews': reviews_sorted,
    }
    return render(request, 'review/display_posts.html', context=context)


def flux(request):
    # Nos followers
    user_follow = authentication_models.User.objects.filter(followed_by__in=models.UserFollows.objects.filter(user=request.user))
    
    # Toutes nos reviews ou celles de nos followers
    all_reviews = models.Review.objects.filter(Q(user__in=user_follow) | Q(user=request.user))
    
    # Tous nos tickets et ceux de nos followers
    all_tickets = models.Ticket.objects.filter(Q(author__in=user_follow) | Q(author=request.user)).exclude(review__in=all_reviews) 
    
    all_unreviewed_tickets = all_tickets.exclude(review__in=all_reviews).annotate(
        state=Value('UNREVIEWED', CharField()))


    tickets_and_reviews = sorted(chain(all_unreviewed_tickets, all_reviews),
                    key=lambda instance: instance.date_created, reverse=True)

    context = {
        'tickets_and_reviews': tickets_and_reviews
        }
    return render(request, 'review/flux.html', context=context)

def get_reviewed_tickets_id(request):
    all_reviews = models.Review.objects.all()
    return [review.ticket.id for review in all_reviews]

@login_required
def follow_users(request):
    user_follows = models.UserFollows.objects.filter(user=request.user)
    user_followed = models.UserFollows.objects.filter(followed_user=request.user)
    if request.method == 'POST':
        user = request.POST.get('username')
        try:
            user_to_follow = authentication_models.User.objects.get(username=user)
            if user_to_follow == request.user:
                messages.error(request, 'Vous ne pouvez pas vous ajouter vous-même !')
                return redirect('follow_users')
        except authentication_models.User.DoesNotExist:
            messages.error(request, "nom incorrect ou utilisateur inexistant")
            return redirect('follow_users')
        else:
            subscription = models.UserFollows(user=request.user, followed_user=user_to_follow)
            subscription.save()
    return render(request, 'review/follow_users_form.html', {'user_follows': user_follows, 'user_followed': user_followed})

@login_required
def unsubscribe(request, user):
    user_to_remove = authentication_models.User.objects.get(username=user)
    models.UserFollows.objects.get(followed_user_id=user_to_remove.id, user_id=request.user.id).delete()
    return redirect('review/follow_users_form.html')