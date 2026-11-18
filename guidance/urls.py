from django.urls import path
from . import views

urlpatterns = [
    # A. Home Page
    path('', views.home, name='home'),

    # B. Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # C. Student Dashboard (login required)
    path('dashboard/', views.dashboard, name='dashboard'),

    # D. Academic Guidance
    path('academic-guidance/', views.academic_guidance, name='academic_guidance'),

    # E. Career Guidance (list with search and detail with path parameter)
    path('career-guidance/', views.career_guidance, name='career_guidance'),
    path('career-guidance/<slug:career_name>/', views.career_detail, name='career_detail'),

    # F. Ask a Question (login required)
    path('ask-question/', views.ask_question, name='ask_question'),

    # G. My Queries (login required)
    path('my-queries/', views.my_queries, name='my_queries'),
]
