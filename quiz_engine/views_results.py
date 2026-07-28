from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Assignment

@login_required
def view_results(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, user=request.user, status='completed')
    return render(request, 'quiz_results.html', {
        'assignment': assignment,
        'quiz': assignment.quiz,
        'questions': assignment.quiz.questions.all().prefetch_related('answers')
    })
