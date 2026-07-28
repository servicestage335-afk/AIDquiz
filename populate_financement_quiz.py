import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        theme_id = 2
        
        # Subject
        subject_name = "Financement des projets et programmes"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, "Formation sur le financement des projets et programmes."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz
        quiz_title = "Validation des Compétences : Financement des projets et programmes"
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
                "text": "Quel est l'objectif principal du budget d'investissement d'un projet ?",
                "answers": [
                    ("Couvrir les dépenses opérationnelles quotidiennes.", False),
                    ("Financer les actifs à long terme et les dépenses nécessaires à la création du projet.", True),
                    ("Augmenter uniquement le salaire du personnel.", False),
                    ("Gérer les imprévus de la vie courante.", False)
                ]
            },
            {
                "text": "Qu'est-ce qu'un bailleur de fonds dans le cadre du financement de projets ?",
                "answers": [
                    ("Une personne qui emprunte de l'argent au projet.", False),
                    ("Une entité (organisme, État, institution) qui fournit des ressources financières à un projet.", True),
                    ("Le chef de projet lui-même.", False),
                    ("Le fournisseur de logiciels du projet.", False)
                ]
            },
            {
                "text": "Quel indicateur permet de mesurer la rentabilité financière d'un projet ?",
                "answers": [
                    ("Le taux de rotation du personnel.", False),
                    ("La Valeur Actuelle Nette (VAN) ou le Taux de Rendement Interne (TRI).", True),
                    ("Le nombre de réunions tenues par mois.", False),
                    ("La couleur du logo du projet.", False)
                ]
            }
        ]

        for q_data in questions_data:
            cursor.execute("SELECT id FROM quiz_engine_question WHERE quiz_id = ? AND question_text = ?", (quiz_id, q_data["text"]))
            question = cursor.fetchone()
            if not question:
                cursor.execute("INSERT INTO quiz_engine_question (quiz_id, question_text) VALUES (?, ?)", (quiz_id, q_data["text"]))
                question_id = cursor.lastrowid
                
                for ans_text, is_correct in q_data["answers"]:
                    cursor.execute("INSERT INTO quiz_engine_answer (question_id, answer_text, is_correct) VALUES (?, ?, ?)", (question_id, ans_text, 1 if is_correct else 0))
                print(f"Inserted Question and Answers: {q_data['text'][:30]}...")
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
