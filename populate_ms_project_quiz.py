import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        theme_id = 2
        
        # Subject
        subject_name = "MS PROJECT : planifier et suivre l’exécution des projets"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, "Formation sur MS Project pour la planification et le suivi des projets."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz
        quiz_title = "Validation des Compétences : MS Project"
        cursor.execute("SELECT id FROM quiz_engine_quiz WHERE title = ?", (quiz_title,))
        quiz = cursor.fetchone()
        if not quiz:
            cursor.execute("INSERT INTO quiz_engine_quiz (subject_id, theme_id, title, passing_score) VALUES (?, ?, ?, ?)", 
                           (subject_id, theme_id, quiz_title, 70))
            quiz_id = cursor.lastrowid
            print(f"Inserted Quiz: ID {quiz_id}")
        else:
            quiz_id = quiz[0]
            print(f"Quiz already exists: ID {quiz_id}")

        # Questions & Answers
        questions_data = [
            {
                "text": "Quelle est la principale fonction de MS Project ?",
                "answers": [
                    ("Gestion de projet, planification et suivi.", True),
                    ("Traitement de texte avancé.", False),
                    ("Gestion de base de données relationnelle.", False),
                    ("Retouche d'images.", False)
                ]
            },
            {
                "text": "Qu'est-ce qu'un jalon dans MS Project ?",
                "answers": [
                    ("Une tâche d'une durée de 0 jour indiquant une étape clé.", True),
                    ("Une tâche qui dure toujours plus de 10 jours.", False),
                    ("Une ressource matérielle.", False),
                    ("Un coût fixe.", False)
                ]
            },
            {
                "text": "Comment définir une dépendance entre deux tâches ?",
                "answers": [
                    ("En reliant les tâches dans le diagramme de Gantt ou via l'onglet prédécesseurs.", True),
                    ("En changeant la couleur de la barre de tâche.", False),
                    ("En supprimant la ressource affectée.", False),
                    ("En augmentant le budget.", False)
                ]
            }
        ]

        for q_data in questions_data:
            cursor.execute("SELECT id FROM quiz_engine_question WHERE quiz_id = ? AND question_text = ?", (quiz_id, q_data["text"]))
            question = cursor.fetchone()
            if not question:
                cursor.execute("INSERT INTO quiz_engine_question (quiz_id, question_text) VALUES (?, ?)", (quiz_id, q_data["text"]))
                question_id = cursor.lastrowid
                print(f"Inserted Question: ID {question_id}")
                
                for ans_text, is_correct in q_data["answers"]:
                    cursor.execute("INSERT INTO quiz_engine_answer (question_id, answer_text, is_correct) VALUES (?, ?, ?)", (question_id, ans_text, 1 if is_correct else 0))
            else:
                print(f"Question already exists: {q_data['text'][:30]}...")

        conn.commit()
        print("Data population completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    populate()
