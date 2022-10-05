from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Value, CharField, Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError

from review import forms, models

from authentication import models as authentication_models

# Create your views here.


@login_required
def create_ticket(request):
    """
    view nous permettant de créer un ticket et de l'enregistrer
    pour le ticket on recupere une photo et on l'enregistre

    Args:
        request (object): requete http

    Returns:
        httpresponse: on retourne la requete http, le template visé avec les variables de gabarit
    """
    ticket_form = forms.TicketForm()
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST)
        photo = request.FILES.get("photo")
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.author = request.user
            ticket.photo = photo
            ticket.save()
            return redirect("flux")

    context = {
        "ticket_form": ticket_form,
    }

    return render(request, "review/create_ticket.html", context=context)


@login_required
def create_review_and_ticket(request):
    """
    view nous permettant de créer un ticket avec une review sur ce même ticket
    pour cela on utlise 3 formulaire:
    TicketForm, PhotoForm, ReviewForm

    Args:
        request (object): requete http

    Returns:
        httpresponse: on retourne la requete http, le template visé avec les variables de gabarit
    """
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST)
        review_form = forms.ReviewForm(request.POST)
        rating = request.POST.get("rating")
        photo = request.FILES.get("photo")
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.photo = photo
            ticket.author = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.rating = rating
            review.save()
            return redirect("flux")
    context = {
        "ticket_form": ticket_form,
        "review_form": review_form,
        "range": range(6),
    }

    return render(request, "review/create_review_and_ticket.html", context=context)


@login_required
def create_review(request, ticket_id):
    """
    view nous permettant de créer une review pour un ticket existant
    que ce soit le notre ou non

    Args:
        request (object): requete http
        ticket_id (str): l'id du ticket visé

    Returns:
        httpresponse: on retourne la requete http, le template visé avec les variables de gabarit
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewForm()
    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST)
        rating = request.POST.get("rating")
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.rating = rating
            review.user = request.user
            review.save()
            return redirect("flux")
    context = {
        "review_form": review_form,
        "ticket": ticket,
        "range": range(6),
    }
    return render(request, "review/create_review.html", context=context)


@login_required
def edit_ticket(request, ticket_id):
    """
    view nous permettant de modifier un ticket que nous avons créé précédemment

    Args:
        request (object): requete http
        ticket_id (str): l'id du ticket visé

    Returns:
        httpresponse: on retourne la requete http, le template visé avec les variables de gabarit
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if ticket.author != request.user:
        return redirect("display_posts")
    else:
        photo_url = ticket.photo.url
        edit_form = forms.TicketForm(instance=ticket)
        delete_form = forms.DeleteTicketReviewForm()
        if request.method == "POST":
            if "edit_ticket" in request.POST:
                photo = request.FILES.get("photo")
                ticket.photo = photo
                edit_form = forms.TicketForm(request.POST, instance=ticket)
                if edit_form.is_valid():
                    edit_form.save()
                    return redirect("display_posts")
            if "delete_ticket_or_review" in request.POST:
                delete_form = forms.DeleteTicketReviewForm(request.POST)
                if delete_form.is_valid():
                    ticket.delete()
                    return redirect("display_posts")

    context = {
        "photo_url": photo_url,
        "edit_form": edit_form,
        "delete_form": delete_form,
    }
    return render(request, "review/edit_ticket.html", context=context)


@login_required
def edit_review(request, review_id):
    """
    view nous permettant de modifier une review que l'on créée précédemment

    Args:
        request (object): requete http
        review_id (str): l'id de la review visée

    Returns:
        httpresponse: on retourne la requete http, le template visé avec les variables de gabarit
    """
    review = get_object_or_404(models.Review, id=review_id)
    if review.user != request.user:
        return redirect("display_posts")
    else:
        edit_form = forms.ReviewForm(instance=review)
        delete_form = forms.DeleteTicketReviewForm()
        if request.method == "POST":
            if "edit_review" in request.POST:
                rating = request.POST.get("rating")
                review.rating = rating
                edit_form = forms.ReviewForm(request.POST, instance=review)
                if edit_form.is_valid():
                    edit_form.save()
                    return redirect("display_posts")
            if "delete_ticket_or_review" in request.POST:
                delete_form = forms.DeleteTicketReviewForm(request.POST)
                if delete_form.is_valid():
                    review.delete()
                    return redirect("display_posts")

    context = {
        "review": review,
        "edit_form": edit_form,
        "delete_form": delete_form,
        "range": range(6),
    }
    return render(request, "review/edit_review.html", context=context)


@login_required
def display_posts(request):
    """
    on affiche tous les posts triés de l'utilisateur
    avec la possibilité de les supprimer

    Args:
        request (object): requete http

    Returns:
        httpresponse: on retourne la requete http, le template visé avec les variables de gabarit
    """
    tickets = models.Ticket.objects.filter(author=request.user)
    reviews = models.Review.objects.filter(user=request.user)
    delete_form = forms.DeleteTicketReviewForm()

    for ticket in tickets:
        if "delete_ticket_or_review" in request.POST:
            delete_form = forms.DeleteTicketReviewForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect("display_posts")

    for review in reviews:
        if "delete_ticket_or_review" in request.POST:
            delete_form = forms.DeleteTicketReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect("display_posts")

    tickets_sorted = sorted(
        tickets, key=lambda instance: instance.date_created, reverse=True
    )
    reviews_sorted = sorted(
        reviews, key=lambda instance: instance.date_created, reverse=True
    )

    context = {
        "tickets": tickets_sorted,
        "reviews": reviews_sorted,
        "delete_form": delete_form,
    }
    return render(request, "review/display_posts.html", context=context)


def flux(request):
    """
    une view qui nous permet d'afficher tous tickets ou reviews de l'utilisateur
    et ceux des personnes qu'il suit

    Args:
        request (object): requete http

    Returns:
        httpresponse: on retourne la requete http, le template visé avec les variables de gabarit
    """
    # Nos followers
    user_follow = authentication_models.User.objects.filter(
        followed_by__in=models.UserFollows.objects.filter(user=request.user)
    )

    # Toutes nos reviews ou celles de nos followers
    all_reviews = models.Review.objects.filter(
        Q(user__in=user_follow) | Q(user=request.user)
    )

    # Tous nos tickets et ceux de nos followers
    all_tickets = models.Ticket.objects.filter(
        Q(author__in=user_follow) | Q(author=request.user)
    ).exclude(review__in=all_reviews)

    all_unreviewed_tickets = all_tickets.exclude(review__in=all_reviews).annotate(
        state=Value("UNREVIEWED", CharField())
    )

    tickets_and_reviews = sorted(
        chain(all_unreviewed_tickets, all_reviews),
        key=lambda instance: instance.date_created,
        reverse=True,
    )

    paginator = Paginator(tickets_and_reviews, 6)
    page = request.GET.get("page")
    user = request.user

    page_obj = paginator.get_page(page)

    context = {
        "page_obj": page_obj,
        "user": user,
    }
    return render(request, "review/flux.html", context=context)


@login_required
def follow_users(request):
    """
    view nous permettant de s'abonner à d'autres utilisateurs
    on récupère aussi les utilisateurs qui sont abonnés à l'utilisateur connecté

    Args:
        request (object): requete http

    Returns:
        httpresponse: on retourne la requete http, le template visé avec les variables de gabarit
    """
    user_follows = models.UserFollows.objects.filter(user=request.user)
    user_followed = models.UserFollows.objects.filter(followed_user=request.user)
    if request.method == "POST":
        user = request.POST.get("username")
        try:
            user_to_follow = authentication_models.User.objects.get(username=user)
            if user_to_follow == request.user:
                messages.error(request, "Vous ne pouvez pas vous ajouter vous-même !")
                return redirect("follow_users")
            elif models.UserFollows.objects.filter(followed_user=user_to_follow):
                messages.error(request, "Vous suivez déjà cet utilisateur")
                return redirect("follow_users")
        except authentication_models.User.DoesNotExist:
            messages.error(request, "nom incorrect ou utilisateur inexistant")
            return redirect("follow_users")
        else:
            subscription = models.UserFollows(
                user=request.user, followed_user=user_to_follow
            )
            subscription.save()

    user = request.user

    context = {
        "user_follows": user_follows,
        "user_followed": user_followed,
        "user": user,
    }
    return render(request, "review/follow_users_form.html", context=context)


@login_required
def unsubscribe(request, user):
    """
    view permettant de se désabonner d'un utilisateur

    Args:
        request (object): requete http
        user (str): nom de l'utilisateur

    Returns:
        htttpresponse: on se redirige vers la page des followers
    """
    user_to_remove = authentication_models.User.objects.get(username=user)
    models.UserFollows.objects.get(followed_user_id=user_to_remove.id, user_id=request.user.id).delete()
    return redirect("follow_users")
