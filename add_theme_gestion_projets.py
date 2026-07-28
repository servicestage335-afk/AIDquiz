import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_platform.settings')
django.setup()

from quiz_engine.models import QuizTheme

def add_theme():
    theme_name = "Gestion de Projets et Programmes"
    if not QuizTheme.objects.filter(name=theme_name).exists():
        theme = QuizTheme.objects.create(name=theme_name, description="Theme pour la gestion de projets et programmes")
        print(f"Theme '{theme_name}' created successfully.")
    else:
        print(f"Theme '{theme_name}' already exists.")

if __name__ == "__main__":
    add_theme()
