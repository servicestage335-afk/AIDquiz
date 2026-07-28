import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Subject
        subject_name = "Systèmes de gestion des bases de données"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, "Formation axée sur la compréhension des SGBD, les bonnes pratiques de stockage et de gestion documentaire, ainsi que les différences fondamentales entre bases de données relationnelles (SQL) et textuelles (CDS/ISIS)."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz
        quiz_title = "Validation des Compétences : Systèmes de Gestion de Bases de Données"
        cursor.execute("SELECT id FROM quiz_engine_quiz WHERE title = ?", (quiz_title,))
        quiz = cursor.fetchone()
        if not quiz:
            cursor.execute("INSERT INTO quiz_engine_quiz (subject_id, title, passing_score) VALUES (?, ?, ?)", 
                           (subject_id, quiz_title, 70))
            quiz_id = cursor.lastrowid
            print(f"Inserted Quiz: ID {quiz_id}")
        else:
            quiz_id = quiz[0]
            print(f"Quiz already exists: ID {quiz_id}")

        # Questions & Answers
        questions_data = [
            {
                "text": "Quelle est la distinction principale entre une base de données relationnelle et une base de données textuelle ?",
                "answers": [
                    ("Les bases textuelles ne peuvent stocker que des fichiers images sans texte.", False),
                    ("Les bases relationnelles s'appuient sur des structures de tables interconnectées et le langage SQL, tandis que les bases textuelles se focalisent sur la gestion, l'indexation et la recherche documentaire de contenus textuels.", True),
                    ("Les bases relationnelles n'autorisent pas le stockage d'informations numériques.", False),
                    ("Il n'existe aucune différence technique, ce sont des synonymes exacts.", False)
                ]
            },
            {
                "text": "Quel outil ou langage est traditionnellement associé à la mise en œuvre et à l'interrogation des bases de données relationnelles ?",
                "answers": [
                    ("Le protocole FTP uniquement.", False),
                    ("Le langage SQL (Structured Query Language).", True),
                    ("Le système CDS/ISIS exclusivement.", False),
                    ("Un simple éditeur de texte non structuré.", False)
                ]
            },
            {
                "text": "Dans le cadre de la diffusion d'information, quelle est l'utilité première d'un SGBD performant selon le programme AID ?",
                "answers": [
                    ("Verrouiller les accès pour empêcher toute consultation externe.", False),
                    ("Appliquer les bonnes pratiques pour stocker, structurer, gérer et rendre efficacement accessibles les documents numériques.", True),
                    ("Ralentir les requêtes des utilisateurs pour économiser la bande passante.", False),
                    ("Supprimer automatiquement les données après chaque consultation.", False)
                ]
            },
            {
                "text": "Quelle méthode pédagogique AID-academy garantit une appropriation concrète des concepts de gestion de données et SQL ?",
                "answers": [
                    ("Des cours purement théoriques sans aucune manipulation de bases de données.", False),
                    ("Une approche combinant présentations magistrales, exercices de simulation, études de cas concrets et discussions en groupes de travail.", True),
                    ("L'interdiction stricte de collaborer ou d'échanger entre pairs.", False),
                    ("L'utilisation de questionnaires génériques sans lien avec les spécificités des institutions.", False)
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
