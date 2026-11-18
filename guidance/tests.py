from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from guidance.models import Career, StudentQuery
from guidance.forms import StudentRegistrationForm, StudentQueryForm


class GuidanceModelAndFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            password='Password123',
            email='test@example.com',
            first_name='Test Student'
        )
        self.career = Career.objects.create(
            title='Web Development',
            description='Overview of web development.',
            skills='HTML5, CSS3, Python, Django',
            roadmap='Learn HTML\nLearn Python\nBuild an App',
            job_roles='Frontend Developer\nBackend Developer'
        )

    def test_career_slug_and_methods(self):
        self.assertEqual(self.career.slug, 'web-development')
        self.assertEqual(len(self.career.get_skills_list()), 4)
        self.assertEqual(len(self.career.get_roadmap_steps()), 3)
        self.assertEqual(len(self.career.get_job_roles_list()), 2)
        self.assertEqual(str(self.career), 'Web Development')

    def test_student_query_creation(self):
        query = StudentQuery.objects.create(
            user=self.user,
            category='Academic',
            question='How to prepare for midterms effectively?',
            status='Pending'
        )
        self.assertEqual(query.status, 'Pending')
        self.assertIn('teststudent', str(query))

    def test_registration_form_valid(self):
        form = StudentRegistrationForm(data={
            'first_name': 'Rohan Sharma',
            'username': 'rohansharma',
            'email': 'rohan@example.com',
            'password': 'StrongPassword1',
            'confirm_password': 'StrongPassword1',
        })
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.username, 'rohansharma')

    def test_registration_form_password_mismatch(self):
        form = StudentRegistrationForm(data={
            'first_name': 'Rohan Sharma',
            'username': 'rohansharma',
            'email': 'rohan@example.com',
            'password': 'StrongPassword1',
            'confirm_password': 'DifferentPassword2',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors)

    def test_query_form_empty_question(self):
        form = StudentQueryForm(data={
            'category': 'Academic',
            'question': '    ',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('question', form.errors)


class GuidanceViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(
            username='student_alice',
            password='Password123',
            email='alice@example.com',
            first_name='Alice'
        )
        self.other_student = User.objects.create_user(
            username='student_bob',
            password='Password123',
            email='bob@example.com',
            first_name='Bob'
        )
        self.career = Career.objects.create(
            title='Web Development',
            description='Web overview',
            skills='Python, Django',
            roadmap='Step 1\nStep 2\nStep 3',
            job_roles='Web Developer'
        )

    def test_home_page_loads(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Student Guidance Portal')
        self.assertContains(resp, 'Academic Guidance')
        self.assertContains(resp, 'Career Guidance')

    def test_academic_guidance_loads(self):
        resp = self.client.get(reverse('academic_guidance'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Study Planning')
        self.assertContains(resp, 'Time Management')
        self.assertContains(resp, 'Exam Preparation')
        self.assertContains(resp, 'Higher Studies')

    def test_career_guidance_list_and_search(self):
        resp = self.client.get(reverse('career_guidance'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Web Development')

        # GET search works
        search_match = self.client.get(reverse('career_guidance') + '?q=Web')
        self.assertEqual(search_match.status_code, 200)
        self.assertContains(search_match, 'Web Development')

        search_nomatch = self.client.get(reverse('career_guidance') + '?q=NonExistent123')
        self.assertEqual(search_nomatch.status_code, 200)
        self.assertContains(search_nomatch, 'No careers matched')

    def test_career_detail_page(self):
        url = reverse('career_detail', kwargs={'career_name': self.career.slug})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Beginner Roadmap')
        self.assertContains(resp, 'Python, Django')

    def test_career_detail_404(self):
        url = reverse('career_detail', kwargs={'career_name': 'does-not-exist'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_dashboard_requires_login(self):
        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('login'), resp.url)

    def test_login_and_dashboard(self):
        self.client.login(username='student_alice', password='Password123')
        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Alice')

    def test_ask_question_requires_login_and_saves(self):
        # Unauthenticated redirects
        resp = self.client.get(reverse('ask_question'))
        self.assertEqual(resp.status_code, 302)

        # Authenticated submits
        self.client.login(username='student_alice', password='Password123')
        post_data = {
            'category': 'Academic',
            'question': 'How many hours should I study each day for exams?',
        }
        submit_resp = self.client.post(reverse('ask_question'), data=post_data)
        self.assertRedirects(submit_resp, reverse('my_queries'))

        query = StudentQuery.objects.filter(user=self.student).first()
        self.assertIsNotNone(query)
        self.assertEqual(query.status, 'Pending')
        self.assertEqual(query.category, 'Academic')

    def test_my_queries_shows_only_own_records_and_admin_answer(self):
        # Alice's query (initially Pending)
        alice_query = StudentQuery.objects.create(
            user=self.student,
            category='Academic',
            question='Alice confidential doubt about project grading.'
        )
        # Bob's query
        StudentQuery.objects.create(
            user=self.other_student,
            category='Career',
            question='Bob private doubt about internship interview.'
        )

        # Log in as Alice -> should see Alice's query, NOT Bob's query
        self.client.login(username='student_alice', password='Password123')
        resp = self.client.get(reverse('my_queries'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Alice confidential doubt')
        self.assertContains(resp, 'Pending')
        self.assertNotContains(resp, 'Bob private doubt')

        # Simulate Admin answering the query and changing status to Answered
        alice_query.answer = 'Focus on clear architecture diagrams and working demo flows.'
        alice_query.status = 'Answered'
        alice_query.save()

        # Alice returns to My Queries and sees the answer & Answered status
        resp_after = self.client.get(reverse('my_queries'))
        self.assertEqual(resp_after.status_code, 200)
        self.assertContains(resp_after, 'Answered')
        self.assertContains(resp_after, 'Focus on clear architecture diagrams')
