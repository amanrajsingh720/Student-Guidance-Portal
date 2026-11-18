from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Career, StudentQuery
from .forms import StudentRegistrationForm, StudentQueryForm


# -----------------------------------------------------------------------------
# Predefined Academic Guidance Topics (as requested in Section 3.D)
# -----------------------------------------------------------------------------
ACADEMIC_TOPICS = [
    {
        'title': 'Study Planning',
        'icon': 'bi-calendar-check',
        'summary': 'Build an effective weekly study routine that keeps you consistent throughout the semester.',
        'details': (
            'Plan your week every Sunday. Break heavy subjects into 45-minute focused blocks. '
            'Spend the first 15 minutes reviewing the previous lecture before moving to new concepts. '
            'Active recall and solving textbook practice problems will help you retain topics far longer '
            'than passively re-reading slides.'
        ),
    },
    {
        'title': 'Time Management',
        'icon': 'bi-clock-history',
        'summary': 'Balance college lectures, practical lab work, coding practice, and personal downtime.',
        'details': (
            'Use the Pomodoro technique (25 minutes study, 5 minutes break) to avoid study fatigue. '
            'Tackle your most difficult subject first thing in the morning when your concentration is highest. '
            'Keep your phone away during study blocks and maintain a single checklist for upcoming assignment deadlines.'
        ),
    },
    {
        'title': 'Exam Preparation',
        'icon': 'bi-journal-check',
        'summary': 'Strategies for semester midterms, end-semester theory exams, and lab practicals.',
        'details': (
            'Start revision at least two weeks before exams. Analyze the last 5 years of university question papers '
            'to spot recurring high-weightage topics. Write down clean formulas, block diagrams, and sample algorithms '
            'in a separate quick-revision notebook.'
        ),
    },
    {
        'title': 'Higher Studies',
        'icon': 'bi-mortarboard',
        'summary': 'Pathways and preparation timelines for postgraduate admissions (GATE, GRE, CAT, MBA).',
        'details': (
            'If you plan to pursue M.Tech or MS, start preparing for GATE or GRE in your 5th semester. '
            'Maintain a good CGPA (above 7.5/8.0), participate in at least one faculty-guided technical project, '
            'and draft your Statement of Purpose (SOP) early.'
        ),
    },
]


# -----------------------------------------------------------------------------
# A. Home Page (/)
# -----------------------------------------------------------------------------
def home(request):
    """Home landing page with project introduction, brief sections, and CTA buttons."""
    careers_preview = Career.objects.all()[:4]
    context = {
        'academic_topics': ACADEMIC_TOPICS,
        'careers_preview': careers_preview,
    }
    return render(request, 'guidance/home.html', context)


# -----------------------------------------------------------------------------
# B. User Authentication (/register/, /login/, /logout/)
# -----------------------------------------------------------------------------
def register_view(request):
    """Registers a new student account and redirects to login upon success."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f"Account created successfully for {user.first_name or user.username}! Please log in."
            )
            return redirect('login')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = StudentRegistrationForm()

    return render(request, 'guidance/register.html', {'form': form})


def login_view(request):
    """Logs in an existing student or admin using Django AuthenticationForm."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name or user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'guidance/login.html', {'form': form})


def logout_view(request):
    """Logs out the user and redirects back to home."""
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


# -----------------------------------------------------------------------------
# C. Student Dashboard (/dashboard/) [Login Required]
# -----------------------------------------------------------------------------
@login_required
def dashboard(request):
    """Student dashboard showing welcome greeting, quick links, and recent queries."""
    user_queries = StudentQuery.objects.filter(user=request.user)
    total_queries = user_queries.count()
    pending_queries = user_queries.filter(status='Pending').count()
    answered_queries = user_queries.filter(status='Answered').count()

    context = {
        'total_queries': total_queries,
        'pending_queries': pending_queries,
        'answered_queries': answered_queries,
        'recent_queries': user_queries[:4],
        'careers_preview': Career.objects.all()[:3],
    }
    return render(request, 'guidance/dashboard.html', context)


# -----------------------------------------------------------------------------
# D. Academic Guidance (/academic-guidance/)
# -----------------------------------------------------------------------------
def academic_guidance(request):
    """Displays predefined academic guidance topics with useful descriptions."""
    context = {
        'topics': ACADEMIC_TOPICS,
    }
    return render(request, 'guidance/academic.html', context)


# -----------------------------------------------------------------------------
# E. Career Guidance (/career-guidance/ & /career-guidance/<slug>/)
# -----------------------------------------------------------------------------
def career_guidance(request):
    """Lists careers and supports GET search filtering using ?q=... parameter."""
    search_query = request.GET.get('q', '').strip()
    careers = Career.objects.all()

    if search_query:
        careers = careers.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(skills__icontains=search_query)
        )

    context = {
        'careers': careers,
        'search_query': search_query,
        'total_count': careers.count(),
    }
    return render(request, 'guidance/career_list.html', context)


def career_detail(request, career_name):
    """Displays a single career path detail using a path parameter."""
    career = get_object_or_404(Career, slug=career_name)
    other_careers = Career.objects.exclude(id=career.id)[:3]
    context = {
        'career': career,
        'skills': career.get_skills_list(),
        'roadmap_steps': career.get_roadmap_steps(),
        'job_roles': career.get_job_roles_list(),
        'other_careers': other_careers,
    }
    return render(request, 'guidance/career_detail.html', context)


# -----------------------------------------------------------------------------
# F. Ask a Question (/ask-question/) [Login Required]
# -----------------------------------------------------------------------------
@login_required
def ask_question(request):
    """Allows logged-in students to submit an Academic or Career question via POST."""
    if request.method == 'POST':
        form = StudentQueryForm(request.POST)
        if form.is_valid():
            query_obj = form.save(commit=False)
            query_obj.user = request.user
            query_obj.status = 'Pending'
            query_obj.save()
            messages.success(
                request,
                'Your question has been submitted! An administrator will review and answer it.'
            )
            return redirect('my_queries')
        else:
            messages.error(request, 'Please check your question and submit again.')
    else:
        initial = {}
        category_param = request.GET.get('category', '').strip().capitalize()
        if category_param in ['Academic', 'Career']:
            initial['category'] = category_param
        form = StudentQueryForm(initial=initial)

    return render(request, 'guidance/ask_question.html', {'form': form})


# -----------------------------------------------------------------------------
# G. My Queries (/my-queries/) [Login Required]
# -----------------------------------------------------------------------------
@login_required
def my_queries(request):
    """Lists only the logged-in student's questions, showing status and answer."""
    # Strict ownership check: filter solely by request.user
    queries = StudentQuery.objects.filter(user=request.user)

    status_filter = request.GET.get('status', '').strip().capitalize()
    if status_filter in ['Pending', 'Answered']:
        queries = queries.filter(status=status_filter)

    context = {
        'queries': queries,
        'status_filter': status_filter,
    }
    return render(request, 'guidance/my_queries.html', context)
