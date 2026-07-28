import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Subject
        subject_name = "Conduite d’un projet de dématérialisation et de gestion de contenus"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, "Formation axée sur les enjeux de la dématérialisation, les composants d'un système GED (Gestion Électronique de Documents), l'interface avec le Workflow, la reprise de l'existant, la planification du chemin critique et la gestion du changement."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz
        quiz_title = "Validation des Compétences : Conduite de Projet de Dématérialisation et GED"
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
                "text": "Quelles sont les fonctions fondamentales constituant l'anatomie d'un système de Gestion Électronique de Documents (GED) ?",
                "answers": [
                    ("L'impression systématique de tous les formulaires reçus par email.", False),
                    ("L'acquisition, le traitement (base de données, indexation), la circulation via Workflow et l'archivage électronique.", True),
                    ("La suppression définitive des index pour accélérer la recherche libre.", False),
                    ("Le blocage de l'accès distant pour des raisons de sécurité matérielle.", False)
                ]
            },
            {
                "text": "Lors de la planification des tâches pour la réussite d'un projet de dématérialisation, sur quoi doit se concentrer l'équipe projet ?",
                "answers": [
                    ("Laisser le calendrier ouvert sans définir de chemin critique.", False),
                    ("La définition des tâches, l'affectation des ressources, le plan de charge, le calendrier et le chemin critique.", True),
                    ("Ignorer la reprise de l'existant et repartir de zéro sans archiver.", False),
                    ("Exclure la Direction Générale des processus décisionnels.", False)
                ]
            },
            {
                "text": "Quel élément est indispensable pour assurer l'appropriation durable du nouveau système GED par le personnel d'une institution ?",
                "answers": [
                    ("Imposer l'outil du jour au lendemain sans communication préalable.", False),
                    ("Mettre en place des actions d'accompagnement au changement, un plan de formation des utilisateurs et une maîtrise de la documentation.", True),
                    ("Sanctionner financièrement les utilisateurs en cas de mauvaise manipulation.", False),
                    ("Restreindre l'utilisation de la GED uniquement au service informatique.", False)
                ]
            },
            {
                "text": "Comment un projet de dématérialisation gère-t-il l'interaction entre la GED et les autres outils collaboratifs ?",
                "answers": [
                    ("En isolant complètement la GED pour éviter les failles de sécurité.", False),
                    ("En créant des interfaces fluides avec des solutions de Workflow, de Groupware et d'Intranet pour automatiser la circulation des documents.", True),
                    ("En interdisant l'usage d'Intranet au sein de l'institution.", False),
                    ("En limitant l'accès aux seuls archivistes de l'établissement.", False)
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
