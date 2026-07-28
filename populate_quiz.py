import sqlite3

def populate():
    # Connect to the database
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    try:
        # 1. Insert Subject
        cursor.execute("SELECT id FROM quiz_engine_subject WHERE name = ?", 
                       ("Création de communautés et de réseaux électroniques",))
        result = cursor.fetchone()
        if result:
            subject_id = result[0]
            print(f"Subject already exists (ID: {subject_id})")
        else:
            cursor.execute("INSERT INTO quiz_engine_subject (name, description) VALUES (?, ?)",
                           ("Création de communautés et de réseaux électroniques", 
                            "Formation axée sur l'évaluation des besoins des membres d'une communauté en ligne, la gestion des aspects techniques (sécurité, vie privée, outils), et les techniques d'animation pour le développement professionnel."))
            subject_id = cursor.lastrowid
            print(f"Created Subject (ID: {subject_id})")

        # 2. Insert Quiz
        cursor.execute("SELECT id FROM quiz_engine_quiz WHERE title = ? AND subject_id = ?",
                       ("Validation des Compétences : Communautés et Réseaux Électroniques", subject_id))
        result = cursor.fetchone()
        if result:
            quiz_id = result[0]
            print(f"Quiz already exists (ID: {quiz_id})")
        else:
            cursor.execute("INSERT INTO quiz_engine_quiz (title, passing_score, subject_id) VALUES (?, ?, ?)",
                           ("Validation des Compétences : Communautés et Réseaux Électroniques", 70, subject_id))
            quiz_id = cursor.lastrowid
            print(f"Created Quiz (ID: {quiz_id})")

        # 3. Questions and Answers
        questions = [
            ("Lors de la phase initiale de création d'une communauté virtuelle pour le développement, quelle est la première démarche critique à mener ?", 
             [("Choisir la plateforme technologique la plus moderne.", 0), 
              ("Comprendre et évaluer les besoins spécifiques des membres cibles ainsi que les possibilités techniques/institutionnelles.", 1), 
              ("Lancer immédiatement une campagne de promotion à grande échelle.", 0), 
              ("Recruter uniquement des experts techniques externes.", 0)]),
            ("Quels aspects indispensables doivent être pris en compte pour garantir la viabilité à long terme d'une communauté en ligne ?", 
             [("Uniquement le design graphique et le nombre de fonctionnalités.", 0), 
              ("Les compétences requises, la vie privée, la sécurité, le multilinguisme et la gestion budgétaire.", 1), 
              ("L'utilisation exclusive d'outils payants et propriétaires.", 0), 
              ("L'absence totale de modération pour laisser la communauté s'autogérer.", 0)]),
            ("Parmi les méthodes suivantes, laquelle favorise le mieux l'apprentissage entre pairs et l'engagement actif des membres d'une communauté AID ?", 
             [("L'envoi massif de newsletters à sens unique sans espace de retour.", 0), 
              ("La combinaison de simulations, d'études de cas concrets, de discussions de groupe et de partages d'expériences du terrain.", 1), 
              ("La mise à disposition de documents PDF statiques sans animation.", 0), 
              ("La restriction des interactions professionnelles aux seuls administrateurs.", 0)]),
            ("Pour structurer la gouvernance d'une communauté virtuelle réussie, que comprend la gestion du personnel nécessaire ?", 
             [("Embaucher uniquement des développeurs web.", 0), 
              ("Définir une équipe de travail avec des rôles clairs de facilitation (community management), de formation et d'évaluation des activités.", 1), 
              ("Ne nommer aucun responsable pour éviter la hiérarchie.", 0), 
              ("Confier la gestion de la communauté à un algorithme automatisé à 100%.", 0)])
        ]

        for q_text, answers in questions:
            cursor.execute("SELECT id FROM quiz_engine_question WHERE question_text = ? AND quiz_id = ?", (q_text, quiz_id))
            result = cursor.fetchone()
            if result:
                q_id = result[0]
                print(f"Question already exists (ID: {q_id})")
            else:
                cursor.execute("INSERT INTO quiz_engine_question (question_text, quiz_id) VALUES (?, ?)", (q_text, quiz_id))
                q_id = cursor.lastrowid
                print(f"Created Question (ID: {q_id})")
                for a_text, is_corr in answers:
                    cursor.execute("INSERT INTO quiz_engine_answer (answer_text, is_correct, question_id) VALUES (?, ?, ?)",
                                   (a_text, is_corr, q_id))
        
        conn.commit()
        print("Data insertion complete.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    populate()
