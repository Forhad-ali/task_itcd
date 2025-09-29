from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
  
    # Ticket URLs
    path("tickets/", views.ticket_list, name="ticket_list"),
    path("tickets/create/", views.ticket_create, name="ticket_create"),
    path("tickets/<int:ticket_id>/edit/", views.ticket_update, name="ticket_update"),
    path("tickets/<int:ticket_id>/delete/", views.ticket_delete, name="ticket_delete"),
    
    # User management URLs
    path("users/", views.user_list, name="user_list"),
    path("users/create/", views.user_create, name="user_create"),
    path("users/<int:user_id>/edit/", views.user_update, name="user_update"),


]
