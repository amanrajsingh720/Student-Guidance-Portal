# Student Guidance Portal 

A simple, beginner-friendly Django web application built for a two-member Computer Applications (CA) project. Students can browse academic guidance topics, explore career paths, search careers, and submit questions that an administrator answers through Django Admin.

---

## 1. Technology Stack
- **Backend:** Python 3, Django (MVT architecture, built-in Auth, Django Admin)
- **Database:** SQLite (`db.sqlite3`)
- **Frontend:** Django Templates, HTML5, CSS3, Bootstrap 5, Bootstrap Icons

---

## 2. Pages & URLs

| URL | Name | Description |
|---|---|---|
| `/` | `home` | Home page with introduction, academic/career overview, and Register/Login buttons |
| `/register/` | `register` | Student registration (Full Name, Username, Email, Password, Confirm Password) |
| `/login/` | `login` | Student login using Django authentication |
| `/logout/` | `logout` | Logs out the current user |
| `/dashboard/` | `dashboard` | Protected student dashboard with welcome message, counts, and quick links |
| `/academic-guidance/` | `academic_guidance` | Predefined topics: Study Planning, Time Management, Exam Preparation, Higher Studies |
| `/career-guidance/` | `career_guidance` | 5 career paths with simple GET search (`?q=...`) |
| `/career-guidance/<career-name>/` | `career_detail` | Career detail page with overview, skills, beginner roadmap, and job roles |
| `/ask-question/` | `ask_question` | Protected POST form for students to submit Academic or Career questions |
| `/my-queries/` | `my_queries` | Protected list showing only the logged-in student's queries, status, and admin replies |
| `/admin/` | Django Admin | Admin interface to answer student queries, mark them Answered, and manage careers |

---

## 3. Project Structure

```
django/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── guidance_portal/             # Django project settings & root URLs
│   ├── settings.py
│   └── urls.py
├── guidance/                    # Main Django app
│   ├── models.py                # Career & StudentQuery models
│   ├── forms.py                 # StudentRegistrationForm & StudentQueryForm
│   ├── views.py                 # Page views, auth, GET search, POST query handling
│   ├── urls.py                  # App URL routing
│   ├── admin.py                 # Django Admin configuration
│   ├── tests.py                 # 14 automated tests
│   └── management/commands/
│       └── seed_data.py         # Seeds 5 careers + demo student & admin
├── templates/
│   ├── base.html                # Shared layout (navbar, messages, footer)
│   ├── 404.html                 # Friendly 404 page
│   └── guidance/                # App page templates
└── static/
    └── css/style.css            # Clean responsive custom styles
```

---

## 4. Local Setup & Run Instructions

### Step 1: Create and Activate Virtual Environment
```bash
python3 -m venv venv
```
- **macOS / Linux:** `source venv/bin/activate`
- **Windows (CMD):** `venv\Scripts\activate`
- **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Database Migrations
```bash
python3 manage.py migrate
```

### Step 4: Load Demo Data (5 Careers + Demo Accounts)
```bash
python3 manage.py seed_data
```
*(Or create your own admin account with `python3 manage.py createsuperuser`.)*

### Step 5: Run Tests
```bash
python3 manage.py test --verbosity=2
```

### Step 6: Start the Development Server
```bash
python3 manage.py runserver
```
Open http://127.0.0.1:8000/ in your browser.

---

## 5. Demo Accounts
- **Student Login (`/login/`):** `student1` / `student@123`
- **Admin Login (`/admin/`):** `admin` / `admin@123`

---

## 6. Demo / Viva Flow
1. Open `/` (Home Page).
2. Register a new student at `/register/`.
3. Log in at `/login/` and view `/dashboard/`.
4. Open `/academic-guidance/` to view the 4 study topics.
5. Open `/career-guidance/`, search for a career using `?q=Web`, and click into `/career-guidance/web-development/`.
6. Submit a question at `/ask-question/`.
7. Open `/my-queries/` to see the question with **Pending** status.
8. Log in to `/admin/` as `admin`, open **Student Queries**, type an answer, change status to **Answered**, and save.
9. Return to `/my-queries/` as the student to show the **Answered** badge and admin response.

---

## 7. Team Division (2 Members)
- **Member 1 (Backend):** Django setup, models (`Career`, `StudentQuery`), migrations, authentication, views, URL routing, forms & validation, Django Admin, and backend tests.
- **Member 2 (Frontend):** Shared `base.html` template and navbar, Home & Dashboard UI, Academic & Career pages, forms styling, My Queries layout, CSS, and frontend testing.
