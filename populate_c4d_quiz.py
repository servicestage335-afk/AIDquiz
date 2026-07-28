import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Subject
        subject_name = "La communication pour le développement C4D"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, 
                            "Principes et stratégies de communication pour favoriser le changement social et comportemental."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz - Linking to theme ID 2
        quiz_title = "Validation des Connaissances : C4D - Communication pour le Développement"
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
                "text": "Qu'est-ce que la 'Communication pour le Développement' (C4D) ?",
                "answers": [
                    ("Une approche systématique de communication pour le changement social et comportemental", True),
                    ("Un simple outil de publicité pour les projets gouvernementaux", False),
                    ("Une méthode de gestion de base de données relationnelles", False),
                    ("Une technique de planification financière", False)
                ]
            },
            {
                "text": "Quelle est l'une des étapes clés de l'élaboration d'une stratégie C4D ?",
                "answers": [
                    ("L'analyse de la situation et des comportements cibles", True),
                    ("L'augmentation du budget global du projet", False),
                    ("La réduction des réunions de coordination", False),
                    ("Le remplacement des équipes techniques", False)
                ]
            },
            {
                "text": "Pourquoi le dialogue communautaire est-il essentiel dans une approche C4D ?",
                "answers": [
                    ("Pour assurer l'appropriation du changement par les populations concernées", True),
                    ("Pour réduire le coût de la campagne de communication", False),
                    ("Pour limiter l'accès à l'information aux experts seulement", False),
                    ("Pour accélérer la clôture des projets", False)
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
