import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Subject
        subject_name = "Management Environnemental - Norme ISO 14001"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, 
                            "Principes et exigences du système de management environnemental selon la norme ISO 14001."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz - Linking to theme ID 1 or another appropriate theme, let's say theme 1 or check existing themes
        quiz_title = "Validation des Compétences : Management Environnemental ISO 14001"
        cursor.execute("SELECT id FROM quiz_engine_quiz WHERE title = ?", (quiz_title,))
        quiz = cursor.fetchone()
        if not quiz:
            cursor.execute("INSERT INTO quiz_engine_quiz (subject_id, title, theme_id, passing_score) VALUES (?, ?, ?, ?)", 
                           (subject_id, quiz_title, 1, 70))
            quiz_id = cursor.lastrowid
            print(f"Inserted Quiz: ID {quiz_id}")
        else:
            quiz_id = quiz[0]
            print(f"Quiz already exists: ID {quiz_id}")

        # Questions & Answers based on user input
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

        # Insert questions and answers
        for q_data in questions_data:
            cursor.execute("INSERT INTO quiz_engine_question (quiz_id, question_text) VALUES (?, ?)", 
                           (quiz_id, q_data["text"]))
            question_id = cursor.lastrowid
            
            for ans_text, is_correct in q_data["answers"]:
                cursor.execute("INSERT INTO quiz_engine_answer (question_id, answer_text, is_correct) VALUES (?, ?, ?)", 
                               (question_id, ans_text, 1 if is_correct else 0))

        conn.commit()
        print("ISO 14001 Quiz populated successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error populating quiz: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    populate()
