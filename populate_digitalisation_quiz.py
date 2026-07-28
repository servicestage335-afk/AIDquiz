import sqlite3

def populate():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    try:
        # 1. Subject
        subject_name = "Digitalisation des services publics et modernisation de l’administration"
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", (subject_name,))
        result = cursor.fetchone()
        if result:
            subject_id = result[0]
            print(f"Subject '{subject_name}' exists (ID: {subject_id})")
        else:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)",
                           (subject_name, "Formation axée sur la mise en œuvre de stratégies de réforme administrative, la simplification des démarches, l'inclusion numérique, la gouvernance des projets de transition et la communication stratégique."))
            subject_id = cursor.lastrowid
            print(f"Created Subject (ID: {subject_id})")

        # 2. Quiz
        quiz_title = "Validation des Compétences : Digitalisation et Modernisation Administrative"
        cursor.execute("SELECT id FROM quiz_engine_quiz WHERE title = ? AND subject_id = ?", (quiz_title, subject_id))
        result = cursor.fetchone()
        if result:
            quiz_id = result[0]
            print(f"Quiz '{quiz_title}' exists (ID: {quiz_id})")
        else:
            cursor.execute("INSERT INTO quiz_engine_quiz (title, passing_score, subject_id) VALUES (?, ?, ?)",
                           (quiz_title, 70, subject_id))
            quiz_id = cursor.lastrowid
            print(f"Created Quiz (ID: {quiz_id})")

        # 3. Questions
        questions = [
            ("Lors de la planification d'une stratégie de digitalisation des services publics, quelle action préalable est indispensable sur le plan juridique et humain ?",
             [("Lancer le développement technique sans modifier les règlements existants.", 0),
              ("Adapter le cadre juridique, structurer la gouvernance et préparer les Ressources Humaines aux nouvelles compétences.", 1),
              ("Externaliser l'intégralité du pouvoir décisionnel à des consultants privés.", 0),
              ("Supprimer immédiatement tous les guichets physiques pour forcer l'usage du numérique.", 0)]),
            ("Quel est l'un des principes fondamentaux de la simplification administrative pour les usagers ?",
             [("Augmenter le nombre de validations intermédiaires pour sécuriser les dossiers.", 0),
              ("Réduire au strict minimum les documents demandés aux usagers et interconnecter les administrations.", 1),
              ("Demander les mêmes pièces justificatives à chaque nouvelle démarche.", 0),
              ("Rendre l'accès aux services en ligne payant pour financer les serveurs.", 0)]),
            ("Comment une administration peut-elle garantir le succès et l'évolution continue d'un service public en ligne après son lancement ?",
             [("En figeant le code informatique pour éviter tout changement futur.", 0),
              ("En assurant un suivi rigoureux de la qualité des services en ligne et en recueillant le retour des usagers.", 1),
              ("En ignorant les retours négatifs pour maintenir le calendrier initial.", 0),
              ("En automatisant les réponses de support exclusivement par des robots sans intervention humaine.", 0)]),
            ("Quel défi majeur doit être impérativement pris en compte pour ne pas exclure une partie de la population lors de la transition vers le tout-numérique ?",
             [("L'achat exclusif de technologies de pointe réservées aux experts.", 0),
              ("L'inclusion numérique (illectronisme, accessibilité et accompagnement des citoyens).", 1),
              ("La restriction des services numériques aux seules grandes agglomérations.", 0),
              ("L'élimination des outils de communication interne.", 0)])
        ]

        for q_text, answers in questions:
            cursor.execute("SELECT id FROM quiz_engine_question WHERE question_text = ? AND quiz_id = ?", (q_text, quiz_id))
            result = cursor.fetchone()
            if result:
                q_id = result[0]
                print(f"Question '{q_text[:30]}...' exists (ID: {q_id})")
            else:
                cursor.execute("INSERT INTO quiz_engine_question (question_text, quiz_id) VALUES (?, ?)", (q_text, quiz_id))
                q_id = cursor.lastrowid
                print(f"Created Question (ID: {q_id})")
                for a_text, is_corr in answers:
                    cursor.execute("INSERT INTO quiz_engine_answer (answer_text, is_correct, question_id) VALUES (?, ?, ?)",
                                   (a_text, is_corr, q_id))
        
        conn.commit()
        print("Digitalisation quiz data insertion complete.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    populate()
