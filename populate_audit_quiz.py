import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Subject
        subject_name = "Audit et contrôle des projets et programmes"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, 
                            "Principes fondamentaux de l'audit et du contrôle pour garantir la conformité et la performance des projets."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz - Linking to theme ID 2
        quiz_title = "Évaluation des Connaissances : Audit et Contrôle de Projets"
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
                "text": "Quel est l'objectif principal d'un audit de projet ?",
                "answers": [
                    ("Évaluer la conformité et identifier les opportunités d'amélioration", True),
                    ("Punir les responsables de projet", False),
                    ("Réduire le budget du projet immédiatement", False),
                    ("Modifier la portée du projet sans autorisation", False)
                ]
            },
            {
                "text": "Que signifie le concept de contrôle de gestion dans un programme ?",
                "answers": [
                    ("La mise en place de mécanismes pour assurer que les objectifs sont atteints", True),
                    ("L'annulation de toutes les activités de risque", False),
                    ("La délégation de toutes les responsabilités à un tiers", False),
                    ("L'augmentation continue de la bureaucratie", False)
                ]
            },
            {
                "text": "Quelle étape fait partie intégrante du processus d'audit ?",
                "answers": [
                    ("La préparation et la planification de l'audit", True),
                    ("La dissimulation des erreurs trouvées", False),
                    ("La mise en œuvre immédiate sans rapport", False),
                    ("Le changement des indicateurs après coup", False)
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
