import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Subject
        subject_name = "Les outils informatiques pour un suivi-évaluation optimisé des projets"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, 
                            "Formation dédiée à l'utilisation des outils informatiques pour améliorer le suivi et l'évaluation des projets."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz
        quiz_title = "Validation des Compétences : Suivi-Évaluation Optimisé"
        theme_id = 2
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
                "text": "Quel est l'avantage principal d'utiliser un outil informatique dédié au suivi-évaluation ?",
                "answers": [
                    ("Cela ne change rien au processus manuel traditionnel.", False),
                    ("Cela permet de centraliser les données, d'automatiser les rapports et d'améliorer la réactivité.", True),
                    ("Cela augmente la complexité des tâches administratives.", False),
                    ("Cela rend les données moins accessibles pour les parties prenantes.", False)
                ]
            },
            {
                "text": "Que permet d'assurer la visualisation en temps réel des indicateurs clés (KPIs) ?",
                "answers": [
                    ("Une prise de décision plus rapide et basée sur des données probantes.", True),
                    ("Une confusion accrue parmi les membres de l'équipe projet.", False),
                    ("Une augmentation inutile de la charge de travail.", False),
                    ("Une déconnexion totale par rapport aux objectifs du projet.", False)
                ]
            },
            {
                "text": "Comment les alertes automatiques contribuent-elles à l'optimisation du suivi ?",
                "answers": [
                    ("En envoyant des messages inutiles constamment.", False),
                    ("En prévenant en cas de dépassement des délais ou de risques identifiés pour une intervention rapide.", True),
                    ("En ralentissant le flux de communication.", False),
                    ("En ignorant systématiquement les problèmes détectés.", False)
                ]
            },
            {
                "text": "Quel rôle joue l'interopérabilité des outils informatiques dans un système de suivi-évaluation ?",
                "answers": [
                    ("Aucun rôle, c'est une option inutile.", False),
                    ("Elle facilite l'échange fluide de données entre les différents logiciels utilisés au sein du projet.", True),
                    ("Elle bloque l'intégration de nouvelles fonctionnalités.", False),
                    ("Elle empêche la centralisation des informations.", False)
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
