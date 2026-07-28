from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from quiz_engine.models import QuizTheme, Subject, Quiz, Question, Answer

class QuizAdditionFlowTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='admin', password='password')
        self.theme = QuizTheme.objects.create(name='Test Theme')
        self.subject = Subject.objects.create(name='Test Subject')
        self.quiz = Quiz.objects.create(theme=self.theme, subject=self.subject, title='Test Quiz', passing_score=50)
        self.question = Question.objects.create(quiz=self.quiz, question_text='Test Question')
        self.answer = Answer.objects.create(question=self.question, answer_text='Test Answer', is_correct=True)
        self.normal_user = User.objects.create_user(username='user', password='password')

    def test_add_quiz_flow(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('add_quiz'), {
            'theme_id': self.theme.id,
            'subject_id': self.subject.id,
            'title': 'New Test Quiz',
            'passing_score': 75
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertTrue(Quiz.objects.filter(title='New Test Quiz', passing_score=75).exists())

    def test_delete_actions(self):
        self.client.login(username='admin', password='password')
        
        # Test delete quiz
        res = self.client.post(reverse('delete_quiz', args=[self.quiz.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['status'], 'success')
        self.assertFalse(Quiz.objects.filter(id=self.quiz.id).exists())

        # Test delete question
        q2 = Question.objects.create(quiz=self.quiz, question_text='Another Question')
        res = self.client.post(reverse('delete_question', args=[q2.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['status'], 'success')
        self.assertFalse(Question.objects.filter(id=q2.id).exists())

        # Test delete answer
        a2 = Answer.objects.create(question=self.question, answer_text='Another Answer')
        res = self.client.post(reverse('delete_answer', args=[a2.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['status'], 'success')
        self.assertFalse(Answer.objects.filter(id=a2.id).exists())

        # Test delete theme
        t2 = QuizTheme.objects.create(name='Another Theme')
        res = self.client.post(reverse('delete_theme', args=[t2.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['status'], 'success')
        self.assertFalse(QuizTheme.objects.filter(id=t2.id).exists())

        # Test delete subject
        s2 = Subject.objects.create(name='Another Subject')
        res = self.client.post(reverse('delete_subject', args=[s2.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['status'], 'success')
        self.assertFalse(Subject.objects.filter(id=s2.id).exists())

        # Test delete user
        res = self.client.post(reverse('delete_user', args=[self.normal_user.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['status'], 'success')
        self.assertFalse(User.objects.filter(id=self.normal_user.id).exists())

class PasswordResetFlowTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='oldpassword')

    def test_password_reset_flow(self):
        # 1. Request password reset
        response = self.client.post(reverse('password_reset_request'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get('reset_email'), 'test@example.com')

        # Check that profile has verification code
        profile = self.user.profile
        self.assertIsNotNone(profile.verification_code)
        code = profile.verification_code

        # 2. Confirm password reset
        response = self.client.post(reverse('password_reset_confirm'), {
            'verification_code': code,
            'new_password': 'newsecurepassword123',
            'confirm_password': 'newsecurepassword123'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify user password changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newsecurepassword123'))


