import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Subject
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", ("Mise en œuvre, utilisation et gestion de l’information numérique",))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           ("Mise en œuvre, utilisation et gestion de l’information numérique", 
                            "Formation axée sur la compréhension des environnements numériques, l'appropriation des stratégies de gestion de l'information, l'évolution des modes d'utilisation et les étapes de suivi-évaluation."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz
        cursor.execute("SELECT id FROM quiz_engine_quiz WHERE title = ?", ("Validation des Compétences : Gestion et Stratégie de l'Information Numérique",))
        quiz = cursor.fetchone()
        if not quiz:
            cursor.execute("INSERT INTO quiz_engine_quiz (subject_id, title, passing_score) VALUES (?, ?, ?)", 
                           (subject_id, "Validation des Compétences : Gestion et Stratégie de l'Information Numérique", 70))
            quiz_id = cursor.lastrowid
            print(f"Inserted Quiz: ID {quiz_id}")
        else:
            quiz_id = quiz[0]
            print(f"Quiz already exists: ID {quiz_id}")

        # Questions & Answers
        questions_data = [
            {
                "text": "Quelle est la finalité principale d'une stratégie d'information au sein d'une organisation moderne ?",
                "answers": [
                    ("Stocker passivement le plus grand volume de données possible sans tri.", False),
                    ("Planifier une démarche stratégique pour optimiser la diffusion, l'utilisation et la maîtrise de l'information par tous les acteurs.", True),
                    ("Restreindre l'accès à l'information numérique aux seuls cadres dirigeants.", False),
                    ("Remplacer intégralement l'équipe humaine par un système d'archivage jetable.", False)
                ]
            },
            {
                "text": "Dans le cadre de la mise en œuvre d'un plan stratégique d'information, quel est le rôle clé des professionnels de l'information ?",
                "answers": [
                    ("Bloquer le partage de données inter-services pour des raisons de confort.", False),
                    ("Garantir la maîtrise de l'information, faire connaître le plan stratégique et accompagner l'évolution des modes d'utilisation.", True),
                    ("Se concentrer uniquement sur la maintenance matérielle des serveurs informatiques.", False),
                    ("Supprimer les anciennes bases de données sans effectuer de sauvegarde.", False)
                ]
            },
            {
                "text": "Pourquoi la phase de suivi et d'évaluation est-elle considérée comme cruciale dans la démarche stratégique ?",
                "answers": [
                    ("Pour valider le budget une fois pour toutes sans jamais modifier la trajectoire.", False),
                    ("Pour s'approprier les résultats, mesurer l'impact sur les compétences et adapter la stratégie aux changements environnementaux.", True),
                    ("Pour rallonger inutilement les délais de livraison du projet.", False),
                    ("Pour automatiser les sanctions contre les utilisateurs qui n'utilisent pas la plateforme.", False)
                ]
            },
            {
                "text": "Comment l'approche pédagogique de l'AID-academy maximise-t-elle l'impact de cette formation sur la gestion de l'information numérique ?",
                "answers": [
                    ("En limitant l'apprentissage à des cours théoriques exclusivement basés sur la mémorisation.", False),
                    ("En combinant des simulations, des études de cas concrets, des discussions en groupe et des interventions d'hommes de terrain pour un apprentissage entre pairs.", True),
                    ("En distribuant des manuels papiers volumineux sans aucun échange interactif.", False),
                    ("En annulant les sessions d'accompagnement personnalisé adaptées aux institutions.", False)
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
