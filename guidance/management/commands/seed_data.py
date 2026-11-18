from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from guidance.models import Career, StudentQuery


class Command(BaseCommand):
    help = 'Seeds the database with the 5 career paths, demo accounts, and sample queries'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding Student Guidance Portal database...'))

        # 1. Create Admin Superuser
        admin_user, created = User.objects.get_or_create(username='admin')
        admin_user.first_name = 'Admin'
        admin_user.email = 'admin@guidanceportal.edu'
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password('admin@123')
        admin_user.save()
        if created:
            self.stdout.write(self.style.SUCCESS('Created superuser: admin / admin@123'))

        # 2. Create Demo Student
        student1, created = User.objects.get_or_create(username='student1')
        student1.first_name = 'Aarav Patel'
        student1.email = 'student1@example.com'
        student1.set_password('student@123')
        student1.save()
        if created:
            self.stdout.write(self.style.SUCCESS('Created demo student: student1 / student@123'))

        # 3. Seed the 5 Career Guidance Paths (Section 3.E)
        careers_data = [
            {
                'title': 'Web Development',
                'slug': 'web-development',
                'icon': 'bi-globe2',
                'description': (
                    'Web Development focuses on designing, building, and maintaining websites and web '
                    'applications that run in browsers. It covers frontend user interfaces, backend '
                    'server logic, databases, and responsive design.'
                ),
                'skills': 'HTML5, CSS3, JavaScript, Bootstrap, Python, Django, SQL, Git',
                'roadmap': (
                    'Learn HTML5 semantic tags, CSS3 layouts (Flexbox/Grid), and responsive Bootstrap.\n'
                    'Learn core JavaScript for interactivity and form handling.\n'
                    'Learn Python and Django (URLs, views, templates, forms, and SQLite/ORM).\n'
                    'Build 2 complete web applications with login and database CRUD features.'
                ),
                'job_roles': (
                    'Frontend Web Developer\n'
                    'Backend Developer (Python/Django)\n'
                    'Full-Stack Web Developer\n'
                    'Web Application Designer'
                ),
            },
            {
                'title': 'Data Science',
                'slug': 'data-science',
                'icon': 'bi-bar-chart-line',
                'description': (
                    'Data Science combines statistics, programming, and analytical thinking to extract '
                    'meaningful insights from structured and unstructured data, helping organizations '
                    'make evidence-based decisions.'
                ),
                'skills': 'Python, SQL, Statistics, Probability, Pandas, NumPy, Matplotlib, Excel',
                'roadmap': (
                    'Build strong foundations in probability, statistics, and spreadsheets.\n'
                    'Learn SQL to query, filter, and join relational database tables.\n'
                    'Practice data cleaning and visualization with Python, Pandas, and Matplotlib.\n'
                    'Complete 2-3 exploratory data analysis projects on real public datasets.'
                ),
                'job_roles': (
                    'Data Analyst\n'
                    'Junior Data Scientist\n'
                    'Business Intelligence Analyst\n'
                    'Reporting & Analytics Associate'
                ),
            },
            {
                'title': 'Artificial Intelligence',
                'slug': 'artificial-intelligence',
                'icon': 'bi-cpu',
                'description': (
                    'Artificial Intelligence explores how software systems can learn from data, '
                    'recognize patterns, process text or images, and automate complex decision-making '
                    'tasks using machine learning techniques.'
                ),
                'skills': 'Python, Linear Algebra, Probability, Machine Learning, Scikit-Learn, PyTorch, Data Preprocessing',
                'roadmap': (
                    'Master Python fundamentals along with linear algebra and basic calculus.\n'
                    'Learn supervised and unsupervised algorithms using Scikit-Learn.\n'
                    'Study model evaluation metrics, train/test splits, and overfitting.\n'
                    'Build a beginner neural network or text/image classifier project.'
                ),
                'job_roles': (
                    'Machine Learning Engineer\n'
                    'AI Research Intern\n'
                    'Computer Vision Developer\n'
                    'NLP Associate Engineer'
                ),
            },
            {
                'title': 'Cybersecurity',
                'slug': 'cybersecurity',
                'icon': 'bi-shield-lock',
                'description': (
                    'Cybersecurity focuses on protecting computer systems, networks, and web '
                    'applications from unauthorized access, vulnerabilities, and digital threats '
                    'through defensive engineering and security testing.'
                ),
                'skills': 'Computer Networks, Linux CLI, TCP/IP, Web Security (OWASP), Python Scripting, Cryptography Basics',
                'roadmap': (
                    'Learn networking fundamentals: IP addressing, DNS, HTTP/HTTPS, and firewalls.\n'
                    'Gain comfort with Linux command-line tools and basic Python/Bash scripting.\n'
                    'Study common web vulnerabilities such as SQL injection, XSS, and CSRF.\n'
                    'Practice legally on beginner lab challenges and security monitoring tools.'
                ),
                'job_roles': (
                    'Security Operations (SOC) Analyst\n'
                    'Junior Penetration Tester\n'
                    'Network Security Associate\n'
                    'Application Security Engineer'
                ),
            },
            {
                'title': 'Software Engineering',
                'slug': 'software-engineering',
                'icon': 'bi-code-square',
                'description': (
                    'Software Engineering applies computer science principles and structured design '
                    'methods to build, test, and maintain reliable software systems collaboratively '
                    'across desktop, web, and backend platforms.'
                ),
                'skills': 'Python / Java / C++, Data Structures & Algorithms, OOP, DBMS, Operating Systems, Git, Testing',
                'roadmap': (
                    'Become confident in one core language (Python, Java, or C++) and OOP concepts.\n'
                    'Study Data Structures, Algorithms, DBMS, and Operating Systems thoroughly.\n'
                    'Learn version control with Git and how to write automated unit tests.\n'
                    'Build and document a multi-module team software project end to end.'
                ),
                'job_roles': (
                    'Software Development Engineer (SDE)\n'
                    'Backend Software Engineer\n'
                    'QA & Test Automation Engineer\n'
                    'Application Developer'
                ),
            },
        ]

        for item in careers_data:
            Career.objects.update_or_create(slug=item['slug'], defaults=item)
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(careers_data)} Career Guidance paths'))

        # 4. Seed 2 Sample Queries for demo student
        StudentQuery.objects.get_or_create(
            user=student1,
            category='Academic',
            question='How should I plan my weekly study schedule to balance semester exams and coding practice?',
            defaults={
                'status': 'Answered',
                'answer': (
                    'Dedicate 1 hour on weekdays to revising college subjects right after classes, and reserve '
                    '45 minutes in the evening for coding practice. Use Saturday mornings for weekly revision '
                    'and solving previous years question papers.'
                ),
            },
        )
        StudentQuery.objects.get_or_create(
            user=student1,
            category='Career',
            question='Which beginner projects should I build first if I want to focus on Web Development with Django?',
            defaults={
                'status': 'Pending',
                'answer': '',
            },
        )

        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))
        self.stdout.write(self.style.SUCCESS('Admin Login   : admin / admin@123 (at /admin/)'))
        self.stdout.write(self.style.SUCCESS('Student Login : student1 / student@123 (at /login/)'))
