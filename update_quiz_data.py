import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_platform.settings')
django.setup()

from quiz_engine.models import QuizTheme, Quiz

def update_quiz_data():
    # 1. Create the new QuizTheme
    theme_name = "Digitalisation de l’administration publique"
    theme, created = QuizTheme.objects.get_or_create(name=theme_name)
    
    if created:
        print(f"Created new theme: {theme.name} with ID: {theme.id}")
    else:
        print(f"Theme already exists: {theme.name} with ID: {theme.id}")

    # 2. Update all Quiz records to have this theme
    count = Quiz.objects.all().update(theme=theme)
    print(f"Updated {count} quizzes to use theme ID: {theme.id}")

if __name__ == "__main__":
    update_quiz_data()
