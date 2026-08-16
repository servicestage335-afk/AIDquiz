import logging
import pandas as pd
import math
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, update_last_login
from django.contrib.auth import signals
from django.contrib import messages
from django.utils import timezone
from django.db import DatabaseError, OperationalError, connection, transaction
from django.http import HttpResponseRedirect, JsonResponse
from .models import Subject, Quiz, Question, Answer, Assignment, UserProfile, QuizTheme, ContactRequest
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.contrib.auth import load_backend
from django.contrib.auth import login as auth_login

logger = logging.getLogger(__name__)

# Helper function
def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def send_password_reset_code(email, code):
    import sib_api_v3_sdk
    from sib_api_v3_sdk.rest import ApiException
    
    configuration = sib_api_v3_sdk.Configuration()
    api_key = getattr(settings, 'EMAIL_HOST_PASSWORD', None) or getattr(settings, 'BREVO_API_KEY', '')
    configuration.api_key['api-key'] = api_key
    
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    sender_email = getattr(settings, 'DEFAULT_FROM_EMAIL', '')
    
    subject = "Password Reset Code"
    html_content = f"<p>Your password reset verification code is: <strong>{code}</strong></p>"
    
    sender = {"name": "AID Quiz Platform", "email": sender_email}
    to = [{"email": email}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=sender,
        subject=subject,
        html_content=html_content
    )
    
    try:
        api_instance.send_transac_email(send_smtp_email)
        return True
    except ApiException as e:
        print(f"BREVO API ERROR DETAILS: {e.body}")
        logger.error(f"Failed to send password reset code email to {email} via Brevo API: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error when sending password reset code email to {email}: {e}")
        return False


# ================= AUTH & DASHBOARD =================

def password_reset_request_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                import random
                code = f"{random.randint(100000, 999999)}"
                profile, _ = UserProfile.objects.get_or_create(user=user)
                profile.verification_code = code
                profile.verification_code_created_at = timezone.now()
                profile.save()
                
                if send_password_reset_code(email, code):
                    messages.success(request, 'Password reset verification code has been sent to your email.')
                    request.session['reset_email'] = email
                    return redirect('password_reset_confirm')
                else:
                    messages.error(request, 'Failed to send verification email. Please try again later.')
            except User.DoesNotExist:
                # To prevent user enumeration, show success or a generic message, but prompt says implement request/confirm
                messages.success(request, 'If an account with that email exists, a reset code has been sent.')
                request.session['reset_email'] = email
                return redirect('password_reset_confirm')
        else:
            messages.error(request, 'Please provide a valid email address.')
    return render(request, 'password_reset_request.html')

def password_reset_confirm_view(request):
    email = request.session.get('reset_email')
    if request.method == 'POST':
        code = request.POST.get('verification_code')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not email:
            messages.error(request, 'Session expired or email not found. Please request a new code.')
            return redirect('password_reset_request')
            
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'password_reset_confirm.html', {'email': email})
            
        try:
            user = User.objects.get(email=email)
            profile = UserProfile.objects.filter(user=user).first()
            
            if not profile or not profile.verification_code or profile.verification_code != code:
                messages.error(request, 'Invalid verification code.')
                return render(request, 'password_reset_confirm.html', {'email': email})
                
            if profile.verification_code_created_at:
                diff = timezone.now() - profile.verification_code_created_at
                if diff.total_seconds() > 900:
                    messages.error(request, 'Verification code has expired. Please request a new one.')
                    return redirect('password_reset_request')
            
            user.set_password(new_password)
            user.save()
            
            profile.verification_code = None
            profile.verification_code_created_at = None
            profile.save()
            
            request.session.pop('reset_email', None)
            messages.success(request, 'Your password has been successfully reset. You can now login.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('password_reset_request')
            
    return render(request, 'password_reset_confirm.html', {'email': email})

class LoginView(auth_views.LoginView):
    template_name = 'login.html'
    def form_valid(self, form):
        logger.info(f"Login success for user: {form.get_user().username}")
        return super().form_valid(form)
    def form_invalid(self, form):
        logger.warning(f"Login failed: {form.errors}")
        return super().form_invalid(form)
    def get_success_url(self): return '/aidadminpage/' if self.request.user.is_staff else '/dashboard/'

def logout_view(request):
    auth_logout(request)
    request.session.clear()
    return redirect('/login/')

@login_required
def user_dashboard(request):
    pending = Assignment.objects.filter(user=request.user, status='pending').select_related('quiz__subject')
    completed_assignments = Assignment.objects.filter(user=request.user, status='completed').select_related('quiz__subject').order_by('-completed_at')
    
    total_quizzes_taken = completed_assignments.count()
    
    if total_quizzes_taken > 0:
        total_score_sum = sum(a.score for a in completed_assignments)
        average_score = round(total_score_sum / total_quizzes_taken)
        certifications_earned = sum(1 for a in completed_assignments if a.score >= a.quiz.passing_score)
    else:
        average_score = 0
        certifications_earned = 0

    context = {
        'pending_assignments': pending,
        'completed_assignments': completed_assignments,
        'average_score': average_score,
        'certifications_earned': certifications_earned,
    }
    return render(request, 'dashboard.html', context)

@login_required
def take_quiz(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, user=request.user)
    questions = Question.objects.filter(quiz=assignment.quiz).prefetch_related('answers')
    return render(request, 'quiz.html', {'assignment': assignment, 'questions': questions})

@login_required
def submit_quiz(request, assignment_id):
    if request.method == 'POST':
        assignment = get_object_or_404(Assignment, id=assignment_id, user=request.user)
        total_score = 0
        for question in Question.objects.filter(quiz=assignment.quiz):
            ans_id = request.POST.get(f'question_{question.id}')
            if ans_id and Answer.objects.filter(id=ans_id, question=question, is_correct=True).exists():
                total_score += 1
        assignment.score = total_score
        assignment.status = 'completed'
        assignment.completed_at = timezone.now()
        assignment.save()
    return redirect('dashboard')

@login_required
def view_results(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, user=request.user, status='completed')
    return render(request, 'quiz_results.html', {'assignment': assignment, 'quiz': assignment.quiz, 'questions': assignment.quiz.questions.all().prefetch_related('answers')})

# ================= STAFF ADMINISTRATIVE SECTIONS =================

@login_required
def aidadminpage(request):
    if not request.user.is_staff: return redirect('user_dashboard')
    
    # Explicitly fetch all QuizTheme objects and all Quizzes to group them by matching theme_id == quiztheme.id
    quiz_themes = QuizTheme.objects.all().prefetch_related('quizzes__questions__answers')
    quizzes = Quiz.objects.all().select_related('theme', 'subject').prefetch_related('questions__answers')
    
    try:
        contact_requests = list(ContactRequest.objects.all().order_by('-created_at'))
    except Exception:
        contact_requests = []

    # Pandas and Math advanced analytics computation for the Admin Apercu / Overview page
    assignments_qs = Assignment.objects.all().select_related('quiz', 'user')
    assignments_data = list(assignments_qs.values('id', 'status', 'score', 'assigned_at', 'completed_at', 'quiz__title', 'user__username'))
    
    if assignments_data:
        df_assign = pd.DataFrame(assignments_data)
    else:
        df_assign = pd.DataFrame(columns=['id', 'status', 'score', 'assigned_at', 'completed_at', 'quiz__title', 'user__username'])

    users_qs = User.objects.filter(is_staff=False).select_related('profile')
    users_data = list(users_qs.values('id', 'username', 'email', 'date_joined'))
    if users_data:
        df_users = pd.DataFrame(users_data)
    else:
        df_users = pd.DataFrame(columns=['id', 'username', 'email', 'date_joined'])

    total_users_count = len(df_users)
    total_assignments_count = len(df_assign)
    completed_df = df_assign[df_assign['status'] == 'completed'] if not df_assign.empty else pd.DataFrame()
    completed_count = len(completed_df)
    pending_count = total_assignments_count - completed_count

    # Math & Pandas stats calculations
    if completed_count > 0:
        mean_score = float(completed_df['score'].mean())
        median_score = float(completed_df['score'].median())
        std_score = float(completed_df['score'].std()) if completed_count > 1 else 0.0
        if math.isnan(std_score):
            std_score = 0.0
        min_score = int(completed_df['score'].min())
        max_score = int(completed_df['score'].max())
        success_rate = float((completed_df['score'] >= 50).mean() * 100)
    else:
        mean_score = 0.0
        median_score = 0.0
        std_score = 0.0
        min_score = 0
        max_score = 0
        success_rate = 0.0

    # Quiz breakdown stats using pandas groupby
    quiz_stats = []
    if not completed_df.empty and 'quiz__title' in completed_df.columns:
        grouped = completed_df.groupby('quiz__title').agg(
            attempts=('score', 'count'),
            avg_score=('score', 'mean'),
            max_score=('score', 'max'),
            min_score=('score', 'min')
        ).reset_index()
        for _, row in grouped.iterrows():
            quiz_stats.append({
                'title': row['quiz__title'],
                'attempts': int(row['attempts']),
                'avg_score': round(float(row['avg_score']), 1),
                'max_score': int(row['max_score']),
                'min_score': int(row['min_score'])
            })

    analytics_stats = {
        'total_users': total_users_count,
        'total_assignments': total_assignments_count,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'mean_score': round(mean_score, 1),
        'median_score': round(median_score, 1),
        'std_score': round(std_score, 1),
        'min_score': min_score,
        'max_score': max_score,
        'success_rate': round(success_rate, 1),
        'quiz_stats': quiz_stats,
    }

    context = {
        'quiz_themes': quiz_themes,
        'themes': quiz_themes, # keeping both for backward compatibility with templates if needed
        'quizzes': quizzes,
        'subjects': Subject.objects.all(),
        'users': users_qs,
        'contact_requests': contact_requests,
        'total_quizzes': quizzes.count(),
        'analytics': analytics_stats,
    }
    return render(request, 'aidadminpage.html', context)

@login_required
def submit_contact_request(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        organization = request.POST.get('organization')
        message = request.POST.get('message')
        if name and email and organization and message:
            try:
                ContactRequest.objects.create(
                    name=name,
                    email=email,
                    organization=organization,
                    message=message
                )
                return JsonResponse({'status': 'success', 'message': 'Demande enregistrée avec succès.'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        return JsonResponse({'status': 'error', 'message': 'Tous les champs sont obligatoires.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)


# ================= AJAX CRUD =================

@login_required
def add_theme(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        if name:
            QuizTheme.objects.create(name=name, description=description)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_theme(request, id):
    if request.method == 'POST':
        theme = QuizTheme.objects.filter(pk=id).first()
        if theme:
            theme.delete()
        if is_ajax(request):
            return JsonResponse({'status': 'success'})
        return redirect('aidadminpage')
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def add_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Subject.objects.create(name=name)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_subject(request, id):
    if request.method == 'POST':
        subject = Subject.objects.filter(pk=id).first()
        if subject:
            subject.delete()
        if is_ajax(request):
            return JsonResponse({'status': 'success'})
        return redirect('aidadminpage')
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def add_quiz_to_theme(request):
    if request.method == 'POST':
        theme_id = request.POST.get('theme_id')
        title = request.POST.get('title')
        passing_score = request.POST.get('passing_score', 50)
        print(f"DEBUG: add_quiz_to_theme called with theme_id={theme_id}, title={title}, passing_score={passing_score}")
        
        if theme_id and title:
            theme = get_object_or_404(QuizTheme, pk=theme_id)
            subject, created = Subject.objects.get_or_create(name=theme.name)
            quiz = Quiz.objects.create(
                theme=theme,
                subject=subject,
                title=title,
                passing_score=int(passing_score)
            )
            print(f"DEBUG: Quiz created successfully with ID {quiz.id}")
            return JsonResponse({'status': 'success'})
        else:
            print("DEBUG: add_quiz_to_theme failed - missing theme_id or title")
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_quiz(request, id):
    if request.method == 'POST':
        print(f"DEBUG: delete_quiz called for id={id}")
        quiz = Quiz.objects.filter(pk=id).first()
        if quiz:
            quiz.delete()
            print(f"DEBUG: Quiz {id} deleted successfully")
        else:
            print(f"DEBUG: Quiz {id} not found for deletion")
        if is_ajax(request):
            return JsonResponse({'status': 'success'})
        return redirect('aidadminpage')
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def add_question(request):
    q_id, text = request.POST.get('quiz_id'), request.POST.get('question_text')
    print(f"DEBUG: add_question called with quiz_id={q_id}, text={text}")
    if q_id and text:
        q = Question.objects.create(quiz_id=q_id, question_text=text)
        print(f"DEBUG: Question created with ID {q.id}")
        return JsonResponse({'status': 'success'})
    print("DEBUG: add_question failed - missing quiz_id or text")
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def edit_question(request, id):
    if request.method == 'POST':
        text = request.POST.get('question_text')
        print(f"DEBUG: edit_question called for id={id}, text={text}")
        question = Question.objects.filter(pk=id).first()
        if question and text:
            question.question_text = text
            question.save()
            print(f"DEBUG: Question {id} updated successfully")
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_question(request, id):
    if request.method == 'POST':
        print(f"DEBUG: delete_question called for id={id}")
        question = Question.objects.filter(pk=id).first()
        if question:
            question.delete()
            print(f"DEBUG: Question {id} deleted successfully")
        if is_ajax(request):
            return JsonResponse({'status': 'success'})
        return redirect('aidadminpage')
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def add_answer(request):
    q_id = request.POST.get('question_id')
    text = request.POST.get('answer_text')
    is_correct = request.POST.get('is_correct') == 'true'
    print(f"DEBUG: add_answer called with question_id={q_id}, text={text}, is_correct={is_correct}")
    if q_id and text:
        ans = Answer.objects.create(question_id=q_id, answer_text=text, is_correct=is_correct)
        print(f"DEBUG: Answer created with ID {ans.id}")
        return JsonResponse({'status': 'success'})
    print("DEBUG: add_answer failed - missing question_id or text")
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def edit_answer(request, id):
    if request.method == 'POST':
        text = request.POST.get('answer_text')
        print(f"DEBUG: edit_answer called for id={id}, text={text}")
        answer = Answer.objects.filter(pk=id).first()
        if answer and text:
            answer.answer_text = text
            answer.save()
            print(f"DEBUG: Answer {id} updated successfully")
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def toggle_correct_answer(request, id):
    if request.method == 'POST':
        print(f"DEBUG: toggle_correct_answer called for id={id}")
        answer = Answer.objects.filter(pk=id).first()
        if answer:
            answer.is_correct = not answer.is_correct
            answer.save()
            print(f"DEBUG: Answer {id} is_correct toggled to {answer.is_correct}")
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_answer(request, id):
    if request.method == 'POST':
        print(f"DEBUG: delete_answer called for id={id}")
        answer = Answer.objects.filter(pk=id).first()
        if answer:
            answer.delete()
            print(f"DEBUG: Answer {id} deleted successfully")
        if is_ajax(request):
            return JsonResponse({'status': 'success'})
        return redirect('aidadminpage')
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def assign_quiz(request):
    u_id, q_id = request.POST.get('user_id'), request.POST.get('quiz_id')
    if u_id and q_id:
        Assignment.objects.create(user_id=u_id, quiz_id=q_id)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def add_user(request):
    u, e, p = request.POST.get('username'), request.POST.get('email'), request.POST.get('password')
    if u and e and p:
        user = User.objects.create_user(username=u, email=e, password=p)
        UserProfile.objects.create(user=user)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_user(request, user_id):
    if request.method == 'POST':
        user = User.objects.filter(pk=user_id).first()
        if user:
            user.delete()
        if is_ajax(request):
            return JsonResponse({'status': 'success'})
        return redirect('aidadminpage')
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def edit_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def admin_update_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            if User.objects.filter(username=username).exclude(id=request.user.id).exists():
                return JsonResponse({'status': 'error', 'message': 'Le nom d\'utilisateur est déjà pris.'}, status=400)
            request.user.username = username
            request.user.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Le nom d\'utilisateur est obligatoire.'}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def admin_send_verification_code(request):
    if request.method == 'POST' and request.user.is_staff:
        import random
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        code = f"{random.randint(100000, 999999)}"
        profile.verification_code = code
        profile.verification_code_created_at = timezone.now()
        profile.save()
        
        if send_password_reset_code(request.user.email, code):
            logger.info(f"Admin verification code sent successfully to {request.user.email}")
        else:
            logger.error(f"Failed to send admin verification code to {request.user.email}")
            
        return JsonResponse({'status': 'success', 'debug_code': code})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def admin_verify_code_only(request):
    if request.method == 'POST' and request.user.is_staff:
        code = request.POST.get('verification_code')
        profile = UserProfile.objects.filter(user=request.user).first()
        
        if not profile or not profile.verification_code or profile.verification_code != code:
            return JsonResponse({'status': 'error', 'message': 'Invalid verification code.'}, status=400)
            
        if profile.verification_code_created_at:
            diff = timezone.now() - profile.verification_code_created_at
            if diff.total_seconds() > 900:
                return JsonResponse({'status': 'error', 'message': 'Verification code has expired.'}, status=400)
                
        request.session['admin_code_verified'] = True
        return JsonResponse({'status': 'success', 'message': 'Code verified successfully. Password modification unlocked.'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def user_profile_view(request):
    return render(request, 'user_profile.html')

@login_required
def aid_blog_view(request):
    return render(request, 'aidblog.html')

def public_aid_page(request):
    return render(request, 'aidblog.html')

@login_required
def admin_verify_and_reset_password(request):
    if request.method == 'POST':
        code = request.POST.get('verification_code')
        new_password = request.POST.get('new_password')
        profile = UserProfile.objects.filter(user=request.user).first()
        
        is_verified_session = request.session.get('admin_code_verified', False)
        
        if not is_verified_session:
            if not profile or not profile.verification_code or profile.verification_code != code:
                return JsonResponse({'status': 'error', 'message': 'Invalid verification code.'}, status=400)
                
            if profile.verification_code_created_at:
                diff = timezone.now() - profile.verification_code_created_at
                if diff.total_seconds() > 900:
                    return JsonResponse({'status': 'error', 'message': 'Verification code has expired.'}, status=400)
                
        if new_password:
            request.user.set_password(new_password)
            request.user.save()
            if profile:
                profile.verification_code = None
                profile.verification_code_created_at = None
                profile.save()
            request.session.pop('admin_code_verified', None)
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'New password cannot be empty.'}, status=400)
    return JsonResponse({'status': 'error'}, status=400)
