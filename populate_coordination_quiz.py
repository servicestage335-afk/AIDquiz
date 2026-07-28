import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Subject
        subject_name = "Coordonner les projets et programmes de développement"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, 
                            "Principes et méthodes pour assurer la cohérence et la synergie entre les projets et programmes de développement."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz - Linking to theme ID 2
        quiz_title = "Validation des Connaissances : Coordination de Projets et Programmes"
        cursor.execute("SELECT id FROM quiz_engine_quiz WHERE title = ?", (quiz_title,))
        quiz = cursor.fetchone()
        if not quiz:
            cursor.execute("INSERT INTO quiz_engine_quiz (subject_id, title, theme_id, passing_score) VALUES (?, ?, ?, ?)", 
                           (subject_id, quiz_title, 2, 70))
            quiz_id = cursor.lastrowid
            print(f"Inserted Quiz: ID {quiz_id}")
        else:
            quiz_id = quiz[0]
            print(f"Quiz already exists: ID {quiz_id}")

        # Questions & Answers
        questions_data = [
            {
                "text": "Quel est l'objectif premier de la coordination des projets et programmes ?",
                "answers": [
                    ("Assurer la synergie, éviter les doubles emplois et optimiser les ressources", True),
                    ("Augmenter le nombre de projets en cours", False),
                    ("Réduire la durée de chaque projet individuellement", False),
                    ("Centraliser toutes les décisions au niveau gouvernemental", False)
                ]
            },
            {
                "text": "Qu'est-ce qu'une matrice de responsabilités dans le contexte de la coordination ?",
                "answers": [
                    ("Un outil qui définit les rôles et responsabilités de chaque acteur dans le cadre d'un programme", True),
                    ("Une liste des budgets alloués par projet", False),
                    ("Un planning chronologique des réunions de suivi", False),
                    ("Un graphique montrant l'évolution des risques du programme", False)
                ]
            },
            {
                "text": "Pourquoi le partage d'informations est-il crucial pour la coordination ?",
                "answers": [
                    ("Pour favoriser la transparence, la prise de décision éclairée et la cohérence des actions", True),
                    ("Pour satisfaire les exigences des bailleurs de fonds uniquement", False),
                    ("Pour augmenter la charge de travail administrative", False),
                    ("Pour limiter l'autonomie des chefs de projet", False)
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
