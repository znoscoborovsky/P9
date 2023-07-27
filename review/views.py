from itertools import chain
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import formset_factory, ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from . import forms, models
User = get_user_model()

@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    my_tickets = tickets.filter(author=request.user)
    reviews = models.Review.objects.all()
    my_reviews = reviews.filter(author=request.user)
    average = 0
    if reviews:
        for review in reviews:
            average += review.rating
        average = average/len(reviews)
    context = {
        "my_tickets":my_tickets,
        "my_reviews":my_reviews,
        "average":average,
        }

    return render(request, "review/home.html", context=context)

@login_required
def create_ticket(request):
    ticket = forms.TicketForm()
    if request.method == 'POST':
        ticket = forms.TicketForm(request.POST,request.FILES)
        if ticket.is_valid():
            ticket.save(commit=False)
            ticket.instance.author = request.user
            ticket.save()
            return redirect('home')
    return render(request,'review/create_ticket.html',context={'ticket':ticket})

@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteTicket()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST,request.FILES, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_ticket' in request.POST:
            delete_form = forms.DeleteTicket(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'review/edit_ticket.html', context=context)

def create_review(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review = forms.ReviewForm()
    if request.method == 'POST':
        review = forms.ReviewForm(request.POST,request.FILES)
        if review.is_valid():
            review.save(commit=False)
            review.instance.author = request.user
            review.instance.ticket = ticket
            review.save()
            return redirect('home')
    return render(request,'review/create_review.html',context={'review':review})

def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    delete_form = forms.DeleteReview()
    edit_form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        if "edit_review" in request.POST:
            edit_form=forms.ReviewForm(request.POST, instance=review)  
            if edit_form.is_valid():
                edit_form.save()
                return redirect("home")
        if "delete_review" in request.POST:
            review.delete()
            return redirect("home")
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'review/edit_review.html', context=context)

def create_ticket_and_review(request):
    pass

@login_required
def follow_users(request):
    message = ""
    form = forms.FollowerForm()
    follows = models.UserFollows.objects.filter(user=request.user)
    count = len(follows)
    if request.method == 'POST':
        #if request.POST in follows:
        
        form = forms.FollowerForm(request.POST)
        #raise ValidationError(f"Vous suivez déjà les publications de {request.POST['followed_user']}")
        
        if form.is_valid():
            #form.cleaned_data['followed_user'] 
            try: 
                form.save(commit=False)
                form.instance.user = request.user
                form.save()
                return redirect('home')
            except:
                message = f"vous suivez déjà {form.cleaned_data['followed_user']}"
                return render(request, 'review/follow_users_form.html', context={'form': form, 'follows':follows, 'count':count, "message":message})
    return render(request, 'review/follow_users_form.html', context={'form': form, 'follows':follows, 'count':count, "message":message})

def del_follower(request,  follow_id):
    models.UserFollows.objects.filter(user_id=request.user.id, followed_user_id=follow_id).delete()
    return redirect('follow_users')
