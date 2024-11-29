import os
import keyboard

# --------------------------- DEBUT ---------------------------

def viderTerminal():
    os.system("cls" if os.name == "nt" else "clear")


# --------------------------- CLASSES ---------------------------

class Blokus:
    def __init__(self):
        self.nbJoueur = int(input("Entrez le nombre de joueurs (2-4) : "))
        self.joueurs = []
        self.plateau = self.initPlateau()
        self.pieces_placees = []  # Historique des pièces placées
        self.colors = [31, 32, 33, 34]  # Couleurs ANSI (rouge, vert, jaune, bleu)
        self.initJoueurs()
        self.piece_active = None
        self.position_active = None
        self.tours = {joueur.nom: 0 for joueur in self.joueurs}  # Compteur de tours par joueur

    def initPlateau(self):
        """Initialise un plateau de 22x22 entouré de bordures."""
        plateau = [["■"] * 22 for _ in range(22)]
        for i in range(1, 21):
            for j in range(1, 21):
                plateau[i][j] = "□"
        return plateau

    def afficherPlateau(self):
        """Affiche le plateau de manière lisible, avec la pièce active."""
        for i, ligne in enumerate(self.plateau):
            for j, cell in enumerate(ligne):
                cell_to_print = cell
                # Si une pièce active est présente, affiche-la sauf si un carré plein est déjà là
                if self.piece_active and self.position_active:
                    x, y = self.position_active
                    if 1 <= x <= 20 and 1 <= y <= 20:
                        for pi, ligne_piece in enumerate(self.piece_active.shape):
                            for pj, cell_piece in enumerate(ligne_piece):
                                if (
                                    cell_piece != " "
                                    and i == x + pi
                                    and j == y + pj
                                    and self.plateau[i][j] == "□"
                                ):
                                    cell_to_print = f"\033[1;{self.piece_active.color}m□\033[0m"
                print(cell_to_print, end=" ")
            print()

    def initJoueurs(self):
        """Initialise les joueurs."""
        for i in range(1, self.nbJoueur + 1):
            pieces = self.creerPieces(i)
            self.joueurs.append(Joueur(f"Joueur {i}", pieces))

    def creerPieces(self, joueur_id):
        """Crée des pièces avec une couleur unique par joueur."""
        color = self.colors[joueur_id - 1]  # Attribuer une couleur depuis la liste
        symbole = f"\033[1;{color}m■\033[0m"  # Carré plein coloré
        return [
                    Piece([[symbole]], color),
                    Piece([[symbole], [symbole]], color),
                    Piece([[symbole], [symbole], [symbole]], color),
                    Piece([[symbole, symbole], [symbole, " "]], color),
                    Piece([[symbole], [symbole], [symbole], [symbole]], color),
                    Piece([[" ", symbole],[" ", symbole],[symbole, symbole]], color),
                    Piece([[symbole, symbole], [symbole, symbole]], color),
                    Piece([[" ", symbole],[symbole, symbole],[symbole, " "]], color),
                    Piece([[symbole, " "],[symbole, symbole],[symbole, " "]], color),
                    Piece([[" ", symbole],[symbole, symbole],[symbole, symbole]], color),
                    Piece([[" ", symbole," "],[symbole, symbole, symbole],[" ", symbole, " "]], color),
                    Piece([[" ", symbole], [" ", symbole], [symbole, symbole],[" ", symbole]], color),
                    Piece([[symbole, " "," "],[symbole, symbole, symbole],[symbole, " ", " "]], color),
                    Piece([[" ", symbole," "],[" ", symbole, symbole],[symbole, symbole, " "]], color),
                    Piece([[symbole, symbole],[symbole, " "],[symbole,symbole]], color),
                    Piece([[" ", " ",symbole],[" ", symbole, symbole],[symbole, symbole, " "]], color),
                    Piece([[" ", symbole, symbole],[" ", symbole, " "],[symbole, symbole, " "]], color),
                    Piece([[" ", symbole],[" ", symbole], [symbole, symbole], [symbole, " "]], color),
                    Piece([[symbole, symbole, " ", " "],[" ", symbole, symbole, symbole]], color),
                    Piece([[symbole, " "], [symbole, " "], [symbole, " "], [symbole, " "], [symbole, symbole]], color),
                    Piece([[symbole], [symbole], [symbole], [symbole], [symbole]], color),
                ]

    def afficherPiecesDisponibles(self, joueur):
        """Affiche les pièces disponibles pour un joueur en lignes, alignées, avec 8 colonnes par ligne."""
        pieces = joueur.tab_piece
        max_pieces_par_ligne = 12  # Nombre maximum de colonnes par ligne

        def pad_piece(piece, max_width=5):
            """Ajoute des colonnes et des lignes vides pour atteindre une taille uniforme de max_width x max_width."""
            padded_shape = [row + [" "] * (max_width - len(row)) for row in piece.shape]
            # Ajouter des lignes vides si la pièce est trop courte en hauteur
            while len(padded_shape) < max_width:
                padded_shape.append([" "] * max_width)
            return padded_shape

        print(f"Pièces disponibles pour {joueur.nom} :")
        lignes_pieces = []
        for index, piece in enumerate(pieces):
            padded_piece = pad_piece(piece)
            lignes_pieces.append(padded_piece)

            if (index + 1) % max_pieces_par_ligne == 0 or index == len(pieces) - 1:
                # Afficher un groupe de 8 pièces ou la dernière ligne
                for ligne in range(5):  # Chaque pièce a 4 lignes après padding
                    for p in lignes_pieces:
                        print(" ".join(p[ligne]), end="   ")  # Espacement entre les pièces
                    print()  # Nouvelle ligne pour le plateau
                print()  # Ligne vide entre groupes de pièces
                lignes_pieces = []

    def afficherEtatJeu(self, joueur):
        """Affiche l'état actuel du plateau et des pièces disponibles."""
        viderTerminal()
        print(f"Tour de {joueur.nom}")
        self.afficherPlateau()
        print()
        self.afficherPiecesDisponibles(joueur)
        if self.piece_active:
            print(f"Pièce sélectionnée :")
            for ligne in self.piece_active.shape:
                print(" ".join(ligne))
            print(f"Position actuelle : {self.position_active}")

    def deplacerPiece(self, dx, dy):
        """Déplace la pièce active sur le plateau."""
        if self.piece_active and self.position_active:
            x, y = self.position_active
            new_x, new_y = x + dx, y + dy
            # Vérification des limites du plateau
            if 1 <= new_x <= 20 and 1 <= new_y <= 20:
                self.position_active = (new_x, new_y)

    def placerPiece(self, joueur):
        """Place une pièce si elle respecte les règles de placement."""
        piece, (x, y) = self.piece_active, self.position_active
        if self.verifierPlacement(joueur, piece, x, y):
            for i, ligne in enumerate(piece.shape):
                for j, cell in enumerate(ligne):
                    if cell != " ":
                        self.plateau[x + i][y + j] = cell
            joueur.tab_piece.remove(piece)
            self.pieces_placees.append((piece, x, y))  # Ajouter la pièce au placement historique
            self.piece_active, self.position_active = None, None
            self.tours[joueur.nom] += 1  # Incrémenter le compteur de tours
            return True
        return False

    def verifierPlacement(self, joueur, piece, x, y):
        """Vérifie si une pièce peut être placée à la position donnée."""
        if not (1 <= x <= 20 and 1 <= y <= 20):
            return False  # En dehors des limites

        coin_touches = False
        face_touches = False

        for i, ligne in enumerate(piece.shape):
            for j, cell in enumerate(ligne):
                if cell != " ":
                    px, py = x + i, y + j
                    if not (1 <= px <= 20 and 1 <= py <= 20):
                        return False  # En dehors des limites du plateau
                    
                    if self.plateau[px][py] != "□":
                        return False  # Superposition

                    # Vérification des coins et des faces
                    adjacent_faces = [(px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)]
                    adjacent_corners = [(px - 1, py - 1), (px - 1, py + 1), (px + 1, py - 1), (px + 1, py + 1)]

                    for fx, fy in adjacent_faces:
                        if (
                            1 <= fx <= 20
                            and 1 <= fy <= 20
                            and self.plateau[fx][fy].startswith(f"\033[1;{self.piece_active.color}")
                        ):
                            face_touches = True

                    for cx, cy in adjacent_corners:
                        if (
                            1 <= cx <= 20
                            and 1 <= cy <= 20
                            and self.plateau[cx][cy].startswith(f"\033[1;{self.piece_active.color}")
                        ):
                            coin_touches = True

        if self.tours[joueur.nom] == 0:
            # Premier tour du joueur : doit être dans un coin
            return any(
                (x + i, y + j) in [(1, 1), (1, 20), (20, 1), (20, 20)]
                for i, ligne in enumerate(piece.shape)
                for j, cell in enumerate(ligne)
                if cell != " "
            )
        else:
            # Autres tours : les règles des coins et des faces
            return coin_touches and not face_touches

    def calculerGagnant(self):
        """Calcule et affiche le gagnant."""
        scores = {}
        for joueur in self.joueurs:
            score = sum(piece.value for piece in joueur.tab_piece)
            scores[joueur.nom] = score
        score_min = min(scores.values())
        gagnants = [joueur for joueur, score in scores.items() if score == score_min]
        print("\n--- Résultats Finaux ---")
        for joueur, score in scores.items():
            print(f"{joueur} : {score} points")
        if len(gagnants) > 1:
            print(f"\nÉgalité entre : {', '.join(gagnants)} avec {score_min} points !")
        else:
            print(f"\nLe gagnant est : {gagnants[0]} avec {score_min} points !")

    def jouer(self):
        joueur_actuel = 0
        joueurs_encore_en_jeu = set(j.nom for j in self.joueurs)  # Suivre les joueurs encore en jeu
        passes_consecutifs = 0  # Compteur pour les joueurs qui passent leur tour consécutivement

        while any(j.tab_piece for j in self.joueurs if j.nom in joueurs_encore_en_jeu):  # Continue tant qu'un joueur peut jouer
            joueur = self.joueurs[joueur_actuel]
            if joueur.nom not in joueurs_encore_en_jeu:
                # Si ce joueur a déjà passé, passe au suivant
                joueur_actuel = (joueur_actuel + 1) % self.nbJoueur
                continue

            piece_index = 0  # La première pièce est sélectionnée par défaut
            self.piece_active = joueur.tab_piece[piece_index] if joueur.tab_piece else None
            self.position_active = (10, 10)  # Position par défaut

            self.afficherEtatJeu(joueur)
            while True:
                # Attendre qu'une touche soit pressée
                event = keyboard.read_event(suppress=True)
                if event.event_type == "down":  # Ne traiter que les pressions (pas les relâchements)
                    key = event.name
                    if key == "+":  # Aller à la pièce suivante
                        if joueur.tab_piece:
                            piece_index = (piece_index + 1) % len(joueur.tab_piece)
                            self.piece_active = joueur.tab_piece[piece_index]
                    elif key == "-":  # Aller à la pièce précédente
                        if joueur.tab_piece:
                            piece_index = (piece_index - 1) % len(joueur.tab_piece)
                            self.piece_active = joueur.tab_piece[piece_index]
                    elif key == "haut":
                        self.deplacerPiece(-1, 0)
                    elif key == "bas":
                        self.deplacerPiece(1, 0)
                    elif key == "gauche":
                        self.deplacerPiece(0, -1)
                    elif key == "droite":
                        self.deplacerPiece(0, 1)
                    elif key == "space":
                        # Tourne la pièce active de 90 degrés
                        if self.piece_active:
                            self.piece_active.tournerLaPiece(90)
                    elif key == "enter":
                        if self.piece_active and self.position_active:
                            if self.placerPiece(joueur):
                                passes_consecutifs = 0  # Réinitialise le compteur si une pièce est placée
                                break
                            else:
                                print("Placement invalide, réessayez.")
                    elif key == "f":  # Passer le tour
                        print(f"{joueur.nom} passe son tour.")
                        joueurs_encore_en_jeu.discard(joueur.nom)  # Retirer le joueur actif des joueurs en jeu
                        print(joueurs_encore_en_jeu)
                        passes_consecutifs += 1
                        break
                    elif key == "backspace":
                        print("Fin du jeu.")
                        return
                    else:
                        continue  # Ignore toutes les autres touches
                    self.afficherEtatJeu(joueur)

            # Vérifie si tous les joueurs ont passé leur tour
            if len(joueurs_encore_en_jeu) <= 1 :
                print("\nTous les joueurs ont passé leur tour. Fin de la partie.")
                break

            joueur_actuel = (joueur_actuel + 1) % self.nbJoueur
            while self.joueurs[joueur_actuel].nom not in joueurs_encore_en_jeu:  # Sauter les joueurs hors jeu
                joueur_actuel = (joueur_actuel + 1) % self.nbJoueur

        self.calculerGagnant()


class Piece:
    def __init__(self, shape, color):
        self.shape = shape  # Représentation en liste de listes
        self.color = color  # Couleur de la pièce
        self.value = sum(1 for row in shape for cell in row if cell != " ")  # Calcul de la valeur

    def tournerLaPiece(self, rotation):
        """Tourne la pièce selon l'angle donné (en degrés, multiples de 90)."""
        for _ in range(rotation // 90):
            # Transposer la matrice et inverser chaque ligne pour tourner à 90 degrés
            self.shape = [list(reversed(col)) for col in zip(*self.shape)]


class Joueur:
    def __init__(self, nom, tab_piece):
        self.nom = nom
        self.tab_piece = tab_piece


# --------------------------- MAIN ---------------------------

# Initialisation du jeu
blokus = Blokus()

# Lancement du jeu
blokus.jouer()