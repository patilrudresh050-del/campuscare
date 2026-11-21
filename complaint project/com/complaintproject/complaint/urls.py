from django.urls import path
from . import views

urlpatterns = [

    # ---------------- STUDENT ----------------
    path('', views.student_login, name='student_login'),
    path('register/', views.student_register, name='student_register'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('add/', views.add_complaint, name='add_complaint'),
    path('edit/<int:id>/', views.edit_complaint, name='edit_complaint'),
    path('delete/<int:id>/', views.delete_complaint, name='delete_complaint'),
    path('student-view/<int:id>/', views.student_view, name='student_view'),
    path('logout/', views.student_logout, name='student_logout'),

    # ---------------- ADMIN ----------------
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-view/<int:id>/', views.admin_view, name='admin_view'),
    path('approve/<int:id>/', views.approve_complaint, name='approve_complaint'),
    path('reject/<int:id>/', views.reject_complaint, name='reject_complaint'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
]