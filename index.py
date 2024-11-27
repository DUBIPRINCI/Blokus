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
            Piece([[symbole, symbole], [symbole, " "]], color),
            Piece([[symbole, symbole, symbole]], color),
        ]

    def afficherPiecesDisponibles(self, joueur):
        """Affiche les pièces disponibles pour le joueur."""
        print(f"Pièces disponibles pour {joueur.nom} :")
        for idx, piece in enumerate(joueur.tab_piece):
            print(f"Pièce {idx + 1}:")
            for ligne in piece.shape:
                print(" ".join(ligne))
            print()

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
        if self.verifierPlacement(piece, x, y):
            for i, ligne in enumerate(piece.shape):
                for j, cell in enumerate(ligne):
                    if cell != " ":
                        self.plateau[x + i][y + j] = cell
            joueur.tab_piece.remove(piece)
            self.piece_active, self.position_active = None, None
            return True
        return False

    def verifierPlacement(self, piece, x, y):
        """Vérifie si une pièce peut être placée à la position donnée."""
        for i, ligne in enumerate(piece.shape):
            for j, cell in enumerate(ligne):
                if cell != " ":
                    px, py = x + i, y + j
                    if not (1 <= px <= 20 and 1 <= py <= 20):
                        return False  # En dehors des limites
                    if self.plateau[px][py] != "□":
                        return False  # Superposition
        return True

    def jouer(self):
        """Gère la boucle principale du jeu."""
        joueur_actuel = 0
        while any(j.tab_piece for j in self.joueurs):  # Continue tant qu'un joueur a des pièces
            joueur = self.joueurs[joueur_actuel]
            self.afficherEtatJeu(joueur)
            while True:
                # Attendre qu'une touche soit pressée
                event = keyboard.read_event(suppress=True)
                if event.event_type == "down":  # Ne traiter que les pressions (pas les relâchements)
                    key = event.name
                    if key == "1":
                        self.piece_active = joueur.tab_piece[0]
                        self.position_active = (10, 10)
                    elif key == "2":
                        self.piece_active = joueur.tab_piece[1]
                        self.position_active = (10, 10)
                    elif key == "3":
                        self.piece_active = joueur.tab_piece[2]
                        self.position_active = (10, 10)
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
                                break
                            else:
                                print("Placement invalide, réessayez.")
                    elif key == "backspace":
                        print("Fin du jeu.")
                        return
                    self.afficherEtatJeu(joueur)
            joueur_actuel = (joueur_actuel + 1) % self.nbJoueur
        print("Fin de la partie !")


class Piece:
    def __init__(self, shape, color):
        self.shape = shape  # Représentation en liste de listes
        self.color = color  # Couleur de la pièce

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