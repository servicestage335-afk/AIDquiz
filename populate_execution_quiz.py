import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        theme_id = 2
        
        # Subject
        subject_name = "Outils et techniques d’exécution des projets et programmes"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, "Formation sur les outils et techniques d’exécution des projets et programmes."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz - link to theme here
        quiz_title = "Validation des Compétences : Outils et techniques d’exécution"
        cursor.execute("SELECT id FROM quiz_engine_quiz WHERE title = ?", (quiz_title,))
        quiz = cursor.fetchone()
        if not quiz:
            # Link Quiz to theme_id=2
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
                "text": "Quel outil est couramment utilisé pour visualiser le calendrier d'exécution d'un projet ?",
                "answers": [
                    ("Diagramme de Gantt", True),
                    ("Matrice SWOT", False),
                    ("Analyse de risque", False),
                    ("Charte de projet", False)
                ]
            },
            {
                "text": "Quelle est la fonction principale du suivi et contrôle durant l'exécution ?",
                "answers": [
                    ("Comparer la performance réelle aux objectifs planifiés pour prendre des mesures correctives.", True),
                    ("Changer constamment les objectifs sans justification.", False),
                    ("Ignorer les écarts budgétaires.", False),
                    ("Réduire la communication entre les membres de l'équipe.", False)
                ]
            },
            {
                "text": "Quel rôle joue le chef de projet lors de la phase d'exécution ?",
                "answers": [
                    ("Il supervise les tâches, gère les conflits et assure que les ressources sont utilisées efficacement.", True),
                    ("Il laisse l'équipe travailler sans aucune supervision.", False),
                    ("Il s'occupe uniquement des documents administratifs.", False),
                    ("Il délègue toute responsabilité sans aucun suivi.", False)
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
