
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from review import forms, models
from authentication import models as models_auth
# Create your views here.


@login_required
def flux(request):
    return render(request, 'review/flux.html')



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
            ticket.save()
            #ticket.contributors.add(request.user, through_defaults={'contribution': 'Auteur principal'})
            return redirect('display_posts')

    context = {
        'ticket_form': ticket_form,
        'photo_form': photo_form,
    }

    return render(request, 'review/create_ticket.html', context=context)



@login_required
def create_review(request):
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
                ticket.save()
                review = review_form.save(commit=False)
                review.ticket = ticket
                review.save()
                #ticket.contributors.add(request.user, through_defaults={'contribution': 'Auteur principal'})
                return redirect('display_posts')
    context = {
        'ticket_form': ticket_form,
        'photo_form': photo_form,
        'review_form': review_form,
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
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    context = {
        'tickets': tickets,
        'reviews': reviews,
    }
    return render(request, 'review/display_posts.html', context=context)


@login_required
def follow_users(request):
    form = forms.FollowUsersForm(instance=request.user)
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('flux')
    return render(request, 'review/follow_users_form.html', context={'form': form})

@login_required
def subscription(request):
    user = request.user
    if user.is_active:
        if request.method == 'GET':
            form = forms.UserFollowsForm()
            user_follows = models.UserFollows.objects.filter(user=request.user)
            followers = models.UserFollows.objects.filter(followed_user=request.user)
            infos = {'page_title': 'Abonnements', 'user_follows': user_follows, 'followers': followers, 'form': form}
            return render(request, 'review/subscription.html', infos)
        elif request.method == 'POST':
            form = forms.UserFollowsForm(request.POST, request.FILES)
            if form.is_valid():
                followed_user = form.cleaned_data['followed_user']
                if followed_user is not None:
                    if user != followed_user:
                        data_check = models.UserFollows.objects.filter(user=user).filter(followed_user=followed_user)
                        if not data_check:
                            form.instance.user = request.user
                            form.save()
                            messages.success(request, 'Vous êtes maintenant abonné à cet utilisateur')
                            return redirect('subscription')
                        else:
                            messages.error(request, "Vous suivez déjà cet utilisateur")
                            return redirect('subscription')
                    else:
                        messages.error(request, "Vous ne pouvez pas suivre votre propre profil")
                        return redirect('subscription')
                elif followed_user is None:
                    messages.error(request, "Vous devez sélectionner un utilisateur")
                    return redirect('subscription')
    else:
        return redirect('flux')

@login_required
def unsubscribe(request, followed_user_id):
    user = request.user
    followed_user = get_object_or_404(models_auth.User, id=followed_user_id)
    user_follows = models.UserFollows.objects.filter(followed_user=followed_user).filter(user=user)
    if user_follows:
        user_follows.delete()
    return redirect('subscription')