from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required


from review import forms

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
            photo = photo_form(commit=False)
            photo.uploader = request.user
            photo.save()
            ticket = ticket_form.save(commit=False)
            ticket.photo = photo
            ticket.save()
            #ticket.contributors.add(request.user, through_defaults={'contribution': 'Auteur principal'})
            return redirect('posts')

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
    if request == "POST":
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(),
                photo_form.is_valid(),
                review_form.is_valid()]):
                photo = photo_form(commit=False)
                photo.uploader = request.user
                photo.save()
                ticket = ticket_form.save(commit=False)
                ticket.photo = photo
                ticket.save()
                review = review_form.save(commit=False)
                review.ticket = ticket
                review.save()
                #ticket.contributors.add(request.user, through_defaults={'contribution': 'Auteur principal'})
                return redirect('posts')
    context = {
        'ticket_form': ticket_form,
        'photo_form': photo_form,
        'review_form': review_form,
    }

    return render(request, 'review/create_review.html', context=context)

@login_required
def display_posts(request):
    return render(request, 'review/display_posts.html')