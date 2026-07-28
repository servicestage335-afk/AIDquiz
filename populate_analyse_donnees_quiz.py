import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        theme_id = 2
        
        # Subject
        subject_name = "Analyse de données pour planificateurs de développement"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, "Formation sur l'analyse de données pour les planificateurs de développement."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz - link to theme here
        quiz_title = "Validation des Compétences : Analyse de données pour le développement"
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
                "text": "Quelle est la principale utilité de l'analyse de données dans la planification du développement ?",
                "answers": [
                    ("Aider à la prise de décision basée sur des preuves.", True),
                    ("Remplacer totalement l'intuition humaine.", False),
                    ("Augmenter uniquement le coût des projets.", False),
                    ("Compiler des données sans les utiliser.", False)
                ]
            },
            {
                "text": "Parmi ces outils, lequel est le plus couramment utilisé pour l'analyse statistique avancée ?",
                "answers": [
                    ("Traitement de texte simple.", False),
                    ("Logiciels comme R, Python (Pandas), ou SPSS.", True),
                    ("Un simple carnet de notes.", False),
                    ("Calculatrices basiques uniquement.", False)
                ]
            },
            {
                "text": "Qu'est-ce qu'une donnée 'nettoyée' dans le processus d'analyse ?",
                "answers": [
                    ("Une donnée qui a été supprimée.", False),
                    ("Une donnée dont les erreurs, les doublons et les valeurs manquantes ont été corrigés.", True),
                    ("Une donnée qui a été copiée plusieurs fois.", False),
                    ("Une donnée que personne ne peut lire.", False)
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
