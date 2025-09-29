from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .decorators import role_required
from .models import Ticket
from .forms import TicketForm

from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser
from .forms import UserCreateForm, UserUpdateForm
from .decorators import role_required
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "ittask/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("ticket_list")
    else:
        form = LoginForm()
    return render(request, "ittask/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")



# List all tickets
@login_required
def ticket_list(request):
    role = request.user.role
    if role == "admin" or role == "manager":
        tickets = Ticket.objects.all()
    elif role == "staff":
        tickets = Ticket.objects.filter(assigned_to=request.user)
    else:  # viewer
        tickets = Ticket.objects.all()
    return render(request, "ittask/ticket_list.html", {"tickets": tickets})

# Create ticket
@role_required(['admin','manager'])
def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect("ticket_list")
    else:
        form = TicketForm()
    return render(request, "ittask/ticket_form.html", {"form": form, "title": "Create Ticket"})

# Update ticket
@role_required(['admin','manager','staff'])
def ticket_update(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("ticket_list")
    else:
        form = TicketForm(instance=ticket)
    return render(request, "ittask/ticket_form.html", {"form": form, "title": "Update Ticket"})

# Delete ticket
@role_required(['admin','manager'])
def ticket_delete(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.delete()
    return redirect("ticket_list")




# List users
@role_required(['admin'])
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, "ittask/user_list.html", {"users": users})

# Create user
@role_required(['admin'])
def user_create(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = UserCreateForm()
    return render(request, "ittask/user_form.html", {"form": form, "title": "Create User"})

# Update user
@role_required(['admin'])
def user_update(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = UserUpdateForm(instance=user)
    return render(request, "ittask/user_form.html", {"form": form, "title": "Update User"})
