from itertools import chain
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import formset_factory
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from . import forms, models
#User = get_user_model()

def home(request):
    tickets = models.Ticket.objects.all()
    return render(request, "review/home.html", {"tickets":tickets})

@login_required
def create_ticket(request):
    ticket = forms.TicketForm()
    ticket.author = request.user
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
