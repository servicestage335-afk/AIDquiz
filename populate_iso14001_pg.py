import os
import psycopg2
from urllib.parse import urlparse

def populate_pg():
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("ERROR: DATABASE_URL environment variable is not set.")
        return

    url = urlparse(db_url)
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port or 5432

    print("Connecting to PostgreSQL...")
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    try:
        subject_name = "Management Environnemental - Norme ISO 14001"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = %s;", (subject_name,))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (%s, %s) RETURNING id;", 
                           (subject_name, 
                            "Principes et exigences du système de management environnemental selon la norme ISO 14001."))
            subject_id = cursor.fetchone()[0]
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        quiz_title = "Validation des Compétences : Management Environnemental ISO 14001"
        cursor.execute("SELECT id FROM quiz_engine_quiz WHERE title = %s;", (quiz_title,))
        quiz = cursor.fetchone()
        if not quiz:
            cursor.execute("INSERT INTO quiz_engine_quiz (subject_id, title, theme_id, passing_score) VALUES (%s, %s, %s, %s) RETURNING id;", 
                           (subject_id, quiz_title, 7, 70))
            quiz_id = cursor.fetchone()[0]
            print(f"Inserted Quiz: ID {quiz_id} under theme_id 7")
        else:
            quiz_id = quiz[0]
            cursor.execute("UPDATE quiz_engine_quiz SET theme_id = 7 WHERE id = %s;", (quiz_id,))
            print(f"Quiz already exists: ID {quiz_id}, updated theme_id to 7")

        # Clear existing questions for this quiz to avoid duplication on restart
        cursor.execute("DELETE FROM quiz_engine_question WHERE quiz_id = %s;", (quiz_id,))

        questions_data = [
            {
                "text": "L’objectif principal de la norme ISO 14001 est :",
                "answers": [
                    ("Améliorer la rentabilité", False),
                    ("Maîtriser les impacts environnementaux", True),
                    ("Réduire les coûts RH", False),
                    ("Augmenter la production", False)
                ]
            },
            {
                "text": "Un aspect environnemental est :",
                "answers": [
                    ("Une exigence réglementaire", False),
                    ("Un élément des activités ayant un impact sur l’environnement", True),
                    ("Un objectif environnemental", False),
                    ("Une procédure interne", False)
                ]
            },
            {
                "text": "Un impact environnemental est :",
                "answers": [
                    ("Une cause", False),
                    ("Une conséquence d’un aspect", True),
                    ("Une politique", False),
                    ("Une action corrective", False)
                ]
            },
            {
                "text": "Parmi les situations suivantes, laquelle est une situation anormale ?",
                "answers": [
                    ("Production normale", False),
                    ("Maintenance planifiée", True),
                    ("Fonctionnement stable", False),
                    ("Activité administrative", False)
                ]
            },
            {
                "text": "La revue de direction permet :",
                "answers": [
                    ("De remplacer les audits", False),
                    ("D’évaluer la performance du SME", True),
                    ("De recruter du personnel", False),
                    ("De définir les salaires", False)
                ]
            },
            {
                "text": "La notion de cycle de vie signifie :",
                "answers": [
                    ("La durée de vie du personnel", False),
                    ("Les étapes de la vie d’un produit/service de sa conception à sa fin", True),
                    ("Le planning de production", False),
                    ("La durée d’un projet", False)
                ]
            },
            {
                "text": "Une obligation de conformité comprend :",
                "answers": [
                    ("Uniquement les lois", False),
                    ("Les lois et autres exigences (clients, engagements)", True),
                    ("Seulement les normes ISO", False),
                    ("Les procédures internes", False)
                ]
            },
            {
                "text": "Le leadership dans ISO 14001 implique :",
                "answers": [
                    ("Déléguer uniquement au responsable QHSE", False),
                    ("S’impliquer activement dans le SME", True),
                    ("Ignorer les aspects environnementaux", False),
                    ("Se limiter aux audits", False)
                ]
            },
            {
                "text": "Une action corrective vise à :",
                "answers": [
                    ("Corriger immédiatement un problème", False),
                    ("Éliminer la cause d’une non-conformité", True),
                    ("Former le personnel", False),
                    ("Documenter les processus", False)
                ]
            },
            {
                "text": "L’analyse environnementale sert à :",
                "answers": [
                    ("Évaluer les salaires", False),
                    ("Identifier les aspects et impacts environnementaux", True),
                    ("Planifier les audits", False),
                    ("Gérer les stocks", False)
                ]
            }
        ]

        for q_data in questions_data:
            cursor.execute("INSERT INTO quiz_engine_question (quiz_id, question_text) VALUES (%s, %s) RETURNING id;", 
                           (quiz_id, q_data["text"]))
            question_id = cursor.fetchone()[0]
            
            for ans_text, is_correct in q_data["answers"]:
                cursor.execute("INSERT INTO quiz_engine_answer (question_id, answer_text, is_correct) VALUES (%s, %s, %s);", 
                               (question_id, ans_text, is_correct))

        conn.commit()
        print("ISO 14001 Quiz restarted and successfully inserted into PostgreSQL under theme id 7!")

    except Exception as e:
        conn.rollback()
        print(f"Error populating PostgreSQL quiz: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    populate_pg()
