import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Subject
        subject_name = "Mise en œuvre d’une démarche de responsabilité sociétale au sein des organisations"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, 
                            "Formation sur l'intégration des principes de responsabilité sociétale dans la stratégie et les opérations des organisations."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz - Linking to theme ID 2
        quiz_title = "Validation des Compétences : Démarche RSO"
        cursor.execute("SELECT id FROM quiz_engine_quiz WHERE title = ?", (quiz_title,))
        quiz = cursor.fetchone()
        if not quiz:
            # We assume quiz_engine_quiz has a 'theme_id' field based on requirement
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
                "text": "Qu'est-ce que la Responsabilité Sociétale des Organisations (RSO) ?",
                "answers": [
                    ("Uniquement le respect des lois environnementales.", False),
                    ("La responsabilité d'une organisation vis-à-vis des impacts de ses décisions et activités sur la société et l'environnement.", True),
                    ("Une stratégie de marketing pour améliorer l'image de marque.", False),
                    ("Un synonyme de philanthropie obligatoire.", False)
                ]
            },
            {
                "text": "Quel est l'un des piliers fondamentaux de la RSO ?",
                "answers": [
                    ("Maximisation des profits à court terme.", False),
                    ("La gouvernance de l'organisation.", True),
                    ("L'augmentation du temps de travail des employés.", False),
                    ("La réduction de la communication externe.", False)
                ]
            },
            {
                "text": "Comment une démarche RSO peut-elle bénéficier à une organisation ?",
                "answers": [
                    ("En augmentant les coûts opérationnels sans contrepartie.", False),
                    ("En améliorant l'engagement des employés et la réputation de l'organisation.", True),
                    ("En rendant la conformité légale facultative.", False),
                    ("En isolant l'organisation de son écosystème.", False)
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
