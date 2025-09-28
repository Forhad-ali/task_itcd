from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('viewer-dashboard/', views.viewer_dashboard, name='viewer_dashboard'),
    
    # Ticket URLs
    path("tickets/", views.ticket_list, name="ticket_list"),
    path("tickets/create/", views.ticket_create, name="ticket_create"),
    path("tickets/<int:ticket_id>/edit/", views.ticket_update, name="ticket_update"),
    path("tickets/<int:ticket_id>/delete/", views.ticket_delete, name="ticket_delete"),

]
