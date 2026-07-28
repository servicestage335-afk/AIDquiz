from django.core.management.base import BaseCommand
from django.db import transaction
from quiz_engine.models import Subject, Quiz, Question, Answer

class Command(BaseCommand):
    help = 'Seeds the database with initial AID-Academy training quiz data.'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            # 1. Create Subject
            subject, created = Subject.objects.get_or_create(
                name="Création de communautés et de réseaux électroniques",
                defaults={
                    "description": "Formation axée sur l'évaluation des besoins des membres d'une communauté en ligne, la gestion des aspects techniques (sécurité, vie privée, outils), et les techniques d'animation et de facilitation pour le développement professionnel."
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Subject: {subject.name}'))

            # 2. Create Quiz
            quiz, created = Quiz.objects.get_or_create(
                title="Validation des Compétences : Communautés et Réseaux Électroniques",
                subject=subject,
                defaults={"passing_score": 70}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Quiz: {quiz.title}'))

            # 3. Questions and Answers
            questions_data = [
                {
                    "text": "Lors de la phase initiale de création d'une communauté virtuelle pour le développement, quelle est la première démarche critique à mener ?",
                    "answers": [
                        ("Choisir la plateforme technologique la plus moderne.", False),
                        ("Comprendre et évaluer les besoins spécifiques des membres cibles ainsi que les possibilités techniques/institutionnelles.", True),
                        ("Lancer immédiatement une campagne de promotion à grande échelle.", False),
                        ("Recruter uniquement des experts techniques externes.", False),
                    ]
                },
                {
                    "text": "Quels aspects indispensables doivent être pris en compte pour garantir la viabilité à long terme d'une communauté en ligne ?",
                    "answers": [
                        ("Uniquement le design graphique et le nombre de fonctionnalités.", False),
                        ("Les compétences requises, la vie privée, la sécurité, le multilinguisme et la gestion budgétaire.", True),
                        ("L'utilisation exclusive d'outils payants et propriétaires.", False),
                        ("L'absence totale de modération pour laisser la communauté s'autogérer.", False),
                    ]
                },
                {
                    "text": "Parmi les méthodes suivantes, laquelle favorise le mieux l'apprentissage entre pairs et l'engagement actif des membres d'une communauté AID ?",
                    "answers": [
                        ("L'envoi massif de newsletters à sens unique sans espace de retour.", False),
                        ("La combinaison de simulations, d'études de cas concrets, de discussions de groupe et de partages d'expériences du terrain.", True),
                        ("La mise à disposition de documents PDF statiques sans animation.", False),
                        ("La restriction des interactions professionnelles aux seuls administrateurs.", False),
                    ]
                },
                {
                    "text": "Pour structurer la gouvernance d'une communauté virtuelle réussie, que comprend la gestion du personnel nécessaire ?",
                    "answers": [
                        ("Embaucher uniquement des développeurs web.", False),
                        ("Définir une équipe de travail avec des rôles clairs de facilitation (community management), de formation et d'évaluation des activités.", True),
                        ("Ne nommer aucun responsable pour éviter la hiérarchie.", False),
                        ("Confier la gestion de la communauté à un algorithme automatisé à 100%.", False),
                    ]
                }
            ]

            for q_data in questions_data:
                question, _ = Question.objects.get_or_create(
                    quiz=quiz,
                    question_text=q_data["text"]
                )
                for ans_text, is_correct in q_data["answers"]:
                    Answer.objects.get_or_create(
                        question=question,
                        answer_text=ans_text,
                        is_correct=is_correct
                    )
            
            self.stdout.write(self.style.SUCCESS('Successfully seeded questions and answers.'))
