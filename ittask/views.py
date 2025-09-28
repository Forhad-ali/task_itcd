from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .decorators import role_required

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "ittask/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = LoginForm()
    return render(request, "ittask/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard_view(request):
    role = request.user.role
    if role == "admin":
        return redirect("admin_dashboard")
    elif role == "manager":
        return redirect("manager_dashboard")
    elif role == "staff":
        return redirect("staff_dashboard")
    else:
        return redirect("viewer_dashboard")

# role dashboards
@role_required(allowed_roles=['admin'])
def admin_dashboard(request):
    return render(request, "ittask/admin_dashboard.html")

@role_required(allowed_roles=['manager', 'admin'])
def manager_dashboard(request):
    return render(request, "ittask/manager_dashboard.html")

@role_required(allowed_roles=['staff', 'manager', 'admin'])
def staff_dashboard(request):
    return render(request, "ittask/staff_dashboard.html")

@role_required(allowed_roles=['viewer', 'staff', 'manager', 'admin'])
def viewer_dashboard(request):
    return render(request, "ittask/viewer_dashboard.html")



from .models import Ticket
from .forms import TicketForm

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
