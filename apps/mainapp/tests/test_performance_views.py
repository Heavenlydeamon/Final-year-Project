from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from mainapp.models import UserProfile, Section, Topic, QuizAttempt

class StudentPerformanceViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student1', password='password123')
        self.profile, created = UserProfile.objects.get_or_create(user=self.user, defaults={'role': 'student'})
        if not created:
            self.profile.role = 'student'
            self.profile.save()
        self.section = Section.objects.create(name='Test Section')
        self.topic = Topic.objects.create(name='Test Topic', section=self.section)
        self.client.login(username='student1', password='password123')

    def test_performance_view_no_attempts(self):
        """Test performance view when student has no quiz attempts"""
        response = self.client.get(reverse('student_performance'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/student_performance.html')
        self.assertEqual(response.context['total_quizzes'], 0)
        self.assertEqual(response.context['avg_score'], 0)
        self.assertEqual(response.context['section_performance'], {})

    def test_performance_view_with_attempts(self):
        """Test performance view with normal quiz attempts"""
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=8,
            total_questions=10
        )
        response = self.client.get(reverse('student_performance'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_quizzes'], 1)
        self.assertEqual(response.context['section_performance']['Test Section']['avg_percentage'], 80.0)

    def test_performance_view_zero_questions_attempt(self):
        """Test performance view with an attempt that has 0 total questions (regression test)"""
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=0,
            total_questions=0
        )
        # This used to cause ZeroDivisionError
        response = self.client.get(reverse('student_performance'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['section_performance']['Test Section']['avg_percentage'], 0)
