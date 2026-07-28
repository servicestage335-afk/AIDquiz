import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Subject
        subject_name = "Politique sociale pour planificateurs du développement"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, 
                            "Comprendre les fondements et les outils de la politique sociale dans le cadre du développement."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz - Linking to theme ID 2
        quiz_title = "Validation des Connaissances : Politique Sociale"
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
                "text": "Quel est l'objectif principal d'une politique sociale dans le développement ?",
                "answers": [
                    ("Réduire les inégalités et améliorer le bien-être social", True),
                    ("Augmenter uniquement le PIB national", False),
                    ("Privatiser tous les services publics", False),
                    ("Réduire les dépenses budgétaires sans condition", False)
                ]
            },
            {
                "text": "Parmi ces instruments, lequel est un outil classique de la protection sociale ?",
                "answers": [
                    ("Les filets de sécurité sociale", True),
                    ("Le taux d'intérêt bancaire", False),
                    ("La balance commerciale", False),
                    ("L'indice de prix à la consommation", False)
                ]
            },
            {
                "text": "Quelle approche met l'accent sur l'autonomisation des individus pour sortir de la pauvreté ?",
                "answers": [
                    ("L'approche basée sur les droits et les capacités", True),
                    ("L'approche purement assistancielle", False),
                    ("L'approche de la croissance économique par le haut", False),
                    ("L'approche de la dérégulation totale", False)
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
