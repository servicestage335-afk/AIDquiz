import sqlite3

def populate():
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Subject
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", ("Production et gestion des documents électroniques",))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)", 
                           ("Production et gestion des documents électroniques", 
                            "Formation axée sur la maîtrise du processus de numérisation de documents, les critères de sélection pour l'intégration en bibliothèque numérique, le choix du matériel/logiciels, et la gestion des documents fragiles."))
            subject_id = cursor.lastrowid
            print(f"Inserted Subject: ID {subject_id}")
        else:
            subject_id = subject[0]
            print(f"Subject already exists: ID {subject_id}")

        # Quiz
        cursor.execute("SELECT id FROM quiz_engine_quiz WHERE title = ?", ("Validation des Compétences : Production et Gestion des Documents Électroniques",))
        quiz = cursor.fetchone()
        if not quiz:
            cursor.execute("INSERT INTO quiz_engine_quiz (subject_id, title, passing_score) VALUES (?, ?, ?)", 
                           (subject_id, "Validation des Compétences : Production et Gestion des Documents Électroniques", 70))
            quiz_id = cursor.lastrowid
            print(f"Inserted Quiz: ID {quiz_id}")
        else:
            quiz_id = quiz[0]
            print(f"Quiz already exists: ID {quiz_id}")

        # Questions & Answers
        questions_data = [
            {
                "text": "Quelle étape critique garantit l'intégrité physique lors de la transition du format papier au format électronique ?",
                "answers": [
                    ("Augmenter la vitesse du scanner au détriment de la manipulation.", False),
                    ("Adapter la manipulation des documents selon leur état, notamment pour les cas des documents fragiles et précieux.", True),
                    ("Supprimer systématiquement les originaux papier avant de vérifier le rendu.", False),
                    ("Confier la numérisation uniquement à du personnel sans formation préalable.", False)
                ]
            },
            {
                "text": "Sur quoi repose le choix du matériel et des ressources logicielles pour la création d'une bibliothèque numérique ?",
                "answers": [
                    ("L'achat exclusif de l'équipement le moins cher disponible.", False),
                    ("Une description précise des spécifications techniques du matériel et des logiciels alignée sur les critères de sélection des documents.", True),
                    ("Le choix aléatoire d'outils sans évaluer le volume de production.", False),
                    ("L'absence de progiciels métiers ou de systèmes de gestion de fichiers.", False)
                ]
            },
            {
                "text": "Pourquoi la définition claire des rôles et responsabilités des parties prenantes est-elle essentielle dans un projet de gestion de documents électroniques ?",
                "answers": [
                    ("Pour centraliser toutes les tâches sur une seule et unique personne.", False),
                    ("Pour structurer le flux de travail, du tri initial jusqu'à la validation de l'intégration en bibliothèque numérique.", True),
                    ("Pour externaliser entièrement la gouvernance et le contrôle qualité.", False),
                    ("Pour ralentir volontairement le processus d'archivage.", False)
                ]
            },
            {
                "text": "Comment l'approche pédagogique de l'AID-academy valide-t-elle l'assimilation pratique de ce processus de numérisation ?",
                "answers": [
                    ("En limitant l'apprentissage à de la lecture purement théorique.", False),
                    ("En combinant des exercices de simulation, des cas pratiques concrets de manipulation et des retours d'hommes de terrain.", True),
                    ("En interdisant les visites ou voyages d'études professionnels.", False),
                    ("En proposant des évaluations standardisées déconnectées des réalités des institutions.", False)
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
