import os
import django
import sys

# Configure stdout to handle UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_platform.settings')
django.setup()

from quiz_engine.models import QuizTheme

def add_theme():
    theme_name = "Développement Agricole – Sécurité Alimentaire"
    if not QuizTheme.objects.filter(name=theme_name).exists():
        theme = QuizTheme.objects.create(name=theme_name, description="Thème pour le développement agricole et la sécurité alimentaire")
        print(f"Theme '{theme_name}' created successfully.")
    else:
        print(f"Theme '{theme_name}' already exists.")

if __name__ == "__main__":
    add_theme()
