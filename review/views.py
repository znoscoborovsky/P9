from itertools import chain
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value
from django.shortcuts import get_object_or_404, redirect, render

from . import forms, models
User = get_user_model()

def make_average(reviews):
    average=0
    for review in reviews:
        average += review.rating
    return average/len(reviews)

def lovers(average):
    full, half = divmod(average, 1)
    if 0.75 > half >= 0.25:
        half = 1
    elif half >= 0.75:
        full += 1
        half = 0
    else:
        half = 0
    full = int(full)
    empty = 5 - full - half
    return [1]*full, [1]*half, [1]*empty

# see comments in field average in model
def update_average(reviews):
    for review in reviews:
        review.hearts["average"]["average"] = make_average(reviews)
        review.hearts["average"]["full"], \
        review.hearts["average"]["half"], \
        review.hearts["average"]["empty"] = lovers(review.hearts["average"]["average"])
        review.hearts["author_rating"]["full"], \
        review.hearts["author_rating"]["half"], \
        review.hearts["author_rating"]["empty"] = lovers(review.hearts["author_rating"]["rating"])
        review.save()        

@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    my_tickets = tickets.filter(author=request.user)
    reviews = models.Review.objects.all()
    my_reviews = reviews.filter(author=request.user)
    my_reviews = my_reviews.annotate(content_type=Value('REVIEW', CharField()))
    my_tickets = my_tickets.annotate(content_type=Value('TICKET', CharField()))
    my_posts = sorted(chain(my_reviews, my_tickets),
                      key=lambda instance: instance.date_created,
                      reverse=True
                    )
    tickets = tickets.exclude(author=request.user)
    reviews = reviews.exclude(author=request.user)
    sub_list = []
    follows = models.UserFollows.objects.filter(user=request.user)
    for follow in follows:
        sub_list.append(follow.followed_user)
    follow_tickets = tickets.filter(author__in=sub_list).exclude(author=request.user)
    follow_reviews = reviews.filter(author__in=sub_list).exclude(ticket__author=request.user)
    reviews_my_tickets = reviews.filter(ticket__author=request.user)
    follow_tickets = follow_tickets.annotate(content_type=Value('TICKET', CharField()))
    follow_reviews = follow_reviews.annotate(content_type=Value('REVIEW', CharField()))
    reviews_my_tickets = reviews_my_tickets.annotate(content_type=Value('REVIEW', CharField()))
    reviews_my_tickets = reviews_my_tickets.order_by("-date_created")
    follows = sorted(chain(follow_tickets, follow_reviews),
                      key=lambda instance: instance.date_created,
                      reverse=True
                      )
    other_tickets = tickets.exclude(author__in=sub_list).exclude(author=request.user).annotate(content_type=Value('TICKET', CharField()))
    other_reviews = reviews.exclude(author__in=sub_list).exclude(ticket__author=request.user).annotate(content_type=Value('REVIEW', CharField()))
    others = sorted(chain(other_tickets, other_reviews ),
                      key=lambda instance: instance.date_created,
                      reverse=True
                      )
    context = {
        "my_posts":my_posts,
        "follows":follows,
        "reviews_my_tickets":reviews_my_tickets,
        "others":others
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

@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if models.Review.objects.filter(author=request.user).filter(ticket_id=ticket_id):
        return redirect('no_more_review')
    review = forms.ReviewForm()
    if request.method == 'POST':
        review = forms.ReviewForm(request.POST,request.FILES)
        if review.is_valid():
            review.save(commit=False)
            review.instance.author = request.user
            review.instance.ticket = ticket
            review.instance.hearts = {}
            review.instance.hearts["average"] = {}
            review.instance.hearts["author_rating"] = {}
            review.instance.hearts["author_rating"]["rating"] = review.instance.rating
            review.save()
            update_average(models.Review.objects.filter(ticket_id=ticket_id))
            return redirect('home')
    context={'review':review,
             'ticket':ticket
             }
    return render(request,'review/create_review.html', context=context)

@login_required
def no_more_critic(request):
    return render(request,'review/no_more_critic.html', context={})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    delete_form = forms.DeleteReview()
    edit_form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        if "edit_review" in request.POST:
            edit_form=forms.ReviewForm(request.POST, instance=review)  
            if edit_form.is_valid():
                edit_form.instance.average = {}
                edit_form.instance.hearts = {}
                edit_form.instance.hearts["average"] = {}
                edit_form.instance.hearts["author_rating"] = {}
                edit_form.instance.hearts["author_rating"]["rating"] = edit_form.instance.rating
                edit_form.save()
                update_average(models.Review.objects.filter(ticket_id=review.ticket_id))
                return redirect("home")
        if "delete_review" in request.POST:
            review.delete()
            return redirect("home")
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'review/edit_review.html', context=context)

@login_required
def create_ticket_and_review(request):
    ticket = forms.TicketForm()
    review = forms.ReviewForm()
    if request.method == 'POST':
        review = forms.ReviewForm(request.POST,request.FILES)
        ticket = forms.TicketForm(request.POST,request.FILES)
        if all([review.is_valid(), ticket.is_valid()]):
            ticket.save(commit=False)
            ticket.instance.author = request.user
            ticket.save()     
            review.instance.author = request.user
            review.instance.ticket = ticket.instance
            review.instance.hearts = {}
            review.instance.hearts["average"] = {}
            review.instance.hearts["author_rating"] = {}
            review.instance.hearts["author_rating"]["rating"] = review.instance.rating
            review.save()
            update_average(models.Review.objects.filter(ticket_id=review.instance.ticket_id))
            return redirect("home")
    context = {
        'ticket': ticket,
        'review': review,
        }
    return render(request, 'review/edit_ticket_and_review.html', context=context)

@login_required
def follow_users(request):
    message = ""
    form = forms.FollowerForm()
    follows = models.UserFollows.objects.filter(user=request.user)
    follows_me = []
    for somebody in models.UserFollows.objects.all():
        if somebody.followed_user == request.user:
            follows_me.append(somebody.user)
    count = len(follows)
    if request.method == 'POST':
        form = forms.FollowerForm(request.POST)
        if form.is_valid():
            try: 
                form.save(commit=False)
                form.instance.user = request.user
                form.save()
                return redirect('follow_users')
            except:
                message = f"vous suivez déjà {form.cleaned_data['followed_user']}"
                return render(request, 'review/follow_users_form.html', context={'form': form, 
                                                                                 'follows':follows, 
                                                                                 'count':count, 
                                                                                 "message":message,
                                                                                 "follows_me":follows_me
                                                                                })
    return render(request, 'review/follow_users_form.html', context={'form': form,
                                                                     'follows':follows, 
                                                                     'count':count, 
                                                                     "message":message,
                                                                     "follows_me":follows_me
                                                                     })

@login_required
def del_follower(request,  follow_id):
    models.UserFollows.objects.filter(user_id=request.user.id, followed_user_id=follow_id).delete()
    return redirect('follow_users')


