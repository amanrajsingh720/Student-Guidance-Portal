from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Career(models.Model):
    """Stores a career guidance path with skills, roadmap steps, and example roles."""
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    icon = models.CharField(
        max_length=50,
        default='bi-briefcase',
        help_text='Bootstrap Icon class (e.g. bi-code-slash, bi-bar-chart).'
    )
    description = models.TextField(help_text='Brief overview of this career path.')
    skills = models.TextField(help_text='Comma-separated list of relevant skills.')
    roadmap = models.TextField(help_text='Beginner learning roadmap (one step per line, 3-5 steps).')
    job_roles = models.TextField(help_text='Example job roles (one role per line).')

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    def get_roadmap_steps(self):
        return [line.strip() for line in self.roadmap.splitlines() if line.strip()]

    def get_job_roles_list(self):
        return [line.strip() for line in self.job_roles.splitlines() if line.strip()]

    def __str__(self):
        return self.title


class StudentQuery(models.Model):
    """Stores a question submitted by a logged-in student and the admin's reply."""
    CATEGORY_CHOICES = [
        ('Academic', 'Academic'),
        ('Career', 'Career'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Answered', 'Answered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queries')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Academic')
    question = models.TextField()
    answer = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student Query'
        verbose_name_plural = 'Student Queries'

    def __str__(self):
        return f"{self.user.username} ({self.category}) - {self.status}"
