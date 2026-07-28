import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Subject
        subject_name = "Préparation à la certification en gestion de projet PMP® (Project Management Professional)"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, 
                            "Préparation complète pour la certification PMP® basée sur le PMBOK Guide."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz - Linking to theme ID 2
        quiz_title = "Validation des Compétences : Certification PMP®"
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
                "text": "Quel est le document qui définit la vision, les objectifs et les résultats attendus d'un projet ?",
                "answers": [
                    ("La charte du projet", True),
                    ("Le plan de gestion des risques", False),
                    ("Le registre des parties prenantes", False),
                    ("La structure de découpage du projet (WBS)", False)
                ]
            },
            {
                "text": "Dans le cadre de la gestion agile, quel rôle est responsable de maximiser la valeur du produit ?",
                "answers": [
                    ("Le Scrum Master", False),
                    ("Le Product Owner", True),
                    ("L'équipe de développement", False),
                    ("Le chef de projet", False)
                ]
            },
            {
                "text": "Que signifie le terme 'Chemin critique' dans la gestion de projet ?",
                "answers": [
                    ("Le chemin le plus court pour terminer le projet", False),
                    ("La séquence des activités déterminant la durée la plus courte du projet", True),
                    ("Le chemin qui comporte le plus de risques", False),
                    ("Le chemin utilisé pour la planification des ressources", False)
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
