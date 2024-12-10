import os
import keyboard

# --------------------------- DEBUT ---------------------------

def viderTerminal():
    os.system("cls" if os.name == "nt" else "clear")


# --------------------------- CLASSES ---------------------------

class Blokus:
    def __init__(self):
        while True:
            try:
                self.nbJoueur = int(input("Entrez le nombre de joueurs (2 ou 4) : "))
                if self.nbJoueur in [2, 4]:
                    break
                else:
                    print("Veuillez entrer 2 ou 4.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")
        self.joueurs = []
        self.plateau = self.initPlateau()
        self.pieces_placees = []  # Historique des pièces placées
        self.colors = [31, 32, 33, 34]  # Couleurs ANSI (rouge, vert, jaune, bleu)
        self.initJoueurs()
        self.piece_active = None
        self.position_active = None
        self.tours = {joueur.nom: 0 for joueur in self.joueurs}  # Compteur de tours par joueur
        self.numero_tour = 1  # Compteur global des tours

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
        """Initialise les joueurs et place leurs pièces dans les coins appropriés."""
        for i in range(1, self.nbJoueur + 1):
            pieces = self.creerPieces(i)
            self.joueurs.append(Joueur(f"Joueur {i}", pieces))

        if self.nbJoueur == 2:
            self.joueurs[0].coin = (1, 1)  # Coin en haut à gauche
            self.joueurs[1].coin = (20, 20)  # Coin en bas à droite
        elif self.nbJoueur == 4:
            self.joueurs[0].coin = (1, 1)  # Coin en haut à gauche
            self.joueurs[1].coin = (1, 20)  # Coin en haut à droite
            self.joueurs[2].coin = (20, 1)  # Coin en bas à gauche
            self.joueurs[3].coin = (20, 20)  # Coin en bas à droite

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
        """Affiche les pièces disponibles pour un joueur en lignes alignées."""
        pieces = joueur.tab_piece
        max_pieces_par_ligne = 12  # Nombre maximum de colonnes par ligne

        def pad_piece(piece, max_width=5):
            """Ajoute des colonnes et des lignes vides pour atteindre une taille uniforme de max_width x max_width."""
            padded_shape = [row + [" "] * (max_width - len(row)) for row in piece.shape]
            while len(padded_shape) < max_width:
                padded_shape.append([" "] * max_width)
            return padded_shape

        print(f"Pièces disponibles pour {joueur.nom} :")
        print('Appuyez "+" et "-" pour vous déplacer dans votre liste de pièces ')
        lignes_pieces = []
        for index, piece in enumerate(pieces):
            padded_piece = pad_piece(piece)
            lignes_pieces.append(padded_piece)

            if (index + 1) % max_pieces_par_ligne == 0 or index == len(pieces) - 1:
                for ligne in range(5):
                    for p in lignes_pieces:
                        print(" ".join(p[ligne]), end="   ")
                    print()
                print()
                lignes_pieces = []

    def afficherEtatJeu(self, joueur):
        """Affiche l'état actuel du plateau et des pièces disponibles."""
        viderTerminal()
        print(f"Tour {self.numero_tour} - {joueur.nom}")
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
            self.pieces_placees.append((piece, x, y))
            self.piece_active, self.position_active = None, None
            self.tours[joueur.nom] += 1
            return True
        return False

    def verifierPlacement(self, joueur, piece, x, y):
        """Vérifie si une pièce peut être placée à la position donnée."""
        if not (1 <= x <= 20 and 1 <= y <= 20):
            return False

        coin_touches = False
        face_touches = False

        for i, ligne in enumerate(piece.shape):
            for j, cell in enumerate(ligne):
                if cell != " ":
                    px, py = x + i, y + j
                    if not (1 <= px <= 20 and 1 <= py <= 20):
                        return False

                    if self.plateau[px][py] != "□":
                        return False

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
            return any(
                (x + i, y + j) == joueur.coin
                for i, ligne in enumerate(piece.shape)
                for j, cell in enumerate(ligne)
                if cell != " "
            )
        else:
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
        joueurs_encore_en_jeu = set(j.nom for j in self.joueurs)
        while any(j.tab_piece for j in self.joueurs if j.nom in joueurs_encore_en_jeu):
            joueur = self.joueurs[joueur_actuel]
            if joueur.nom not in joueurs_encore_en_jeu:
                joueur_actuel = (joueur_actuel + 1) % self.nbJoueur
                continue

            piece_index = 0
            self.piece_active = joueur.tab_piece[piece_index] if joueur.tab_piece else None
            self.position_active = (10, 10)

            self.afficherEtatJeu(joueur)
            while True:
                event = keyboard.read_event(suppress=True)
                if event.event_type == "down":
                    key = event.name
                    if key == "+":
                        if joueur.tab_piece:
                            piece_index = (piece_index + 1) % len(joueur.tab_piece)
                            self.piece_active = joueur.tab_piece[piece_index]
                    elif key == "-":
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
                        if self.piece_active:
                            self.piece_active.tournerLaPiece(90)
                    elif key == "enter":
                        if self.piece_active and self.position_active:
                            if self.placerPiece(joueur):
                                break
                            else:
                                print("Placement invalide.")
                    elif key == "f":
                        joueurs_encore_en_jeu.discard(joueur.nom)
                        break
                    elif key == "backspace":
                        print("Fin du jeu.")
                        return
                    else:
                        continue
                    self.afficherEtatJeu(joueur)

            if len(joueurs_encore_en_jeu) <= 1:
                print("\nTous les joueurs ont passé leur tour. Fin de la partie.")
                break

            joueur_actuel = (joueur_actuel + 1) % self.nbJoueur
            while self.joueurs[joueur_actuel].nom not in joueurs_encore_en_jeu:
                joueur_actuel = (joueur_actuel + 1) % self.nbJoueur
            
            self.numero_tour += 1  # Incrémenter le compteur de tours

        self.calculerGagnant()


class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.value = sum(1 for row in shape for cell in row if cell != " ")

    def tournerLaPiece(self, rotation):
        for _ in range(rotation // 90):
            self.shape = [list(reversed(col)) for col in zip(*self.shape)]


class Joueur:
    def __init__(self, nom, tab_piece):
        self.nom = nom
        self.tab_piece = tab_piece
        self.coin = None


# --------------------------- MAIN ---------------------------

blokus = Blokus()
blokus.jouer()