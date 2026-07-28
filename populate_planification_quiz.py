import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        theme_id = 2
        
        # Subject
        subject_name = "Planification stratégique et opérationnelle des projets et programmes"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        
        if not subject:
            # Subject does not have a theme_id column
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, "Formation sur la planification stratégique et opérationnelle des projets et programmes."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz - link to theme here
        quiz_title = "Validation des Compétences : Planification stratégique et opérationnelle"
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
                "text": "Quelle est la différence fondamentale entre la planification stratégique et la planification opérationnelle ?",
                "answers": [
                    ("La planification stratégique définit le 'quoi' et le 'pourquoi' à long terme, tandis que l'opérationnelle définit le 'comment' à court terme.", True),
                    ("La planification opérationnelle est centrée sur la vision, tandis que la stratégique est centrée sur les tâches quotidiennes.", False),
                    ("Il n'y a aucune différence, ce sont des termes interchangeables.", False),
                    ("La planification stratégique concerne uniquement les finances, tandis que l'opérationnelle concerne les ressources humaines.", False)
                ]
            },
            {
                "text": "Qu'est-ce qu'une étape clé dans le cycle de vie d'un projet ?",
                "answers": [
                    ("L'abandon du projet après la phase d'étude.", False),
                    ("La définition des objectifs, la planification, l'exécution, le suivi/contrôle et la clôture.", True),
                    ("La répétition infinie de la planification sans jamais passer à l'exécution.", False),
                    ("L'ignorance des risques pour aller plus vite.", False)
                ]
            },
            {
                "text": "Pourquoi est-il essentiel d'identifier les parties prenantes lors de la phase de planification ?",
                "answers": [
                    ("Pour les ignorer durant le projet.", False),
                    ("Pour comprendre leurs besoins, attentes et influencer positivement la réussite du projet.", True),
                    ("Pour éviter de communiquer avec elles.", False),
                    ("Parce que c'est une obligation légale sans utilité pratique.", False)
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
