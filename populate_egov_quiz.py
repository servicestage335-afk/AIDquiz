import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Subject
        subject_name = "Développement du gouvernement électronique (e-Gov) et l’innovation gouvernementale"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           (subject_name, "Formation axée sur la transition numérique du secteur public, l'amélioration de la gouvernance par les données, la gestion des parties prenantes, le rôle des agents de changement et l'élaboration de plans d'action e-Gov."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz
        quiz_title = "Validation des Compétences : Gouvernement Électronique (e-Gov) et Innovation"
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
                "text": "Au-delà de l'aspect purement technologique, quel est l'impact majeur attendu de la transition numérique vers le e-Gov sur la relation État-citoyen ?",
                "answers": [
                    ("Rendre l'administration totalement inaccessible sans intermédiaire humain.", False),
                    ("Transformer les relations État-citoyen en apportant plus de transparence, d'inclusion et une meilleure prestation de services basée sur les données.", True),
                    ("Centraliser toutes les décisions politiques au sein d'un seul serveur automatisé.", False),
                    ("Supprimer le principe de redevabilité des institutions publiques.", False)
                ]
            },
            {
                "text": "Quelle compétence clé les cadres du secteur public doivent-ils acquérir pour assurer la réussite d'un plan d'action e-Gov dans leurs ministères ou municipalités ?",
                "answers": [
                    ("Savoir coder l'intégralité des infrastructures réseaux eux-mêmes.", False),
                    ("Devenir de véritables 'agents de changement' capables de concevoir des stratégies et de piloter la transformation humaine et organisationnelle.", True),
                    ("Ignorer le rôle des différentes parties prenantes pour accélérer le processus.", False),
                    ("Restreindre l'accès aux sites informationnels et téléprocédures.", False)
                ]
            },
            {
                "text": "Dans le contenu d'une stratégie e-Gov, que désigne la gestion des inforoutes gouvernementales et des téléprocédures ?",
                "answers": [
                    ("La construction de réseaux routiers physiques pour relier les administrations.", False),
                    ("La mise en place de flux d'informations interconnectés et de démarches administratives dématérialisées pour les usagers.", True),
                    ("L'achat massif de logiciels de bureautique classiques non connectés.", False),
                    ("La fermeture définitive des canaux d'échange avec le secteur privé.", False)
                ]
            },
            {
                "text": "Quel mécanisme pédagogique de l'AID-academy permet aux participants de valider concrètement les théories du gouvernement en ligne ?",
                "answers": [
                    ("L'évaluation théorique sur table sans aucun retour terrain.", False),
                    ("Les visites d'études auprès des administrations, les simulations pratiques et le développement d'un réseau d'échange avec des experts.", True),
                    ("L'absence totale d'accompagnement personnalisé pour les institutions.", False),
                    ("L'apprentissage exclusif à travers des présentations magistrales figées.", False)
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
