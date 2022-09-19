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
            ticket.contributors.add(request.user, through_defaults={'contribution': 'Auteur principal'})
            return redirect('posts')

    context = {
        'ticket_form': ticket_form,
        'photo_form': photo_form,
    }

    return render(request, 'review/create_ticket.html', context=context)

@login_required
def create_review(request):
    return render(request, 'review/create_review.html')

@login_required
def display_posts(request):
    return render(request, 'review/display_posts.html')