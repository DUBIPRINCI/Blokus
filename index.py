from Couleurs import *
import os

# --------------------------- DEBUT ---------------------------

def viderTerminal():
    os.system("cls" if os.name == "nt" else "clear")
viderTerminal()


# --------------------------- CLASSES ---------------------------

class Blokus:
    
    def __init__(self):
        self.nbJoueur = int(input("Entrez le nombre de joueurs (2-4) : "))
        self.joueurs = []
        self.plateau = self.initPlateau()
        self.pieces_placees = []  # Historique des pièces placées
        self.initJoueurs()
    
    def initPlateau(self):
        """Initialise un plateau de 22x22 entouré de bordures."""
        plateau = [["■"] * 22 for _ in range(22)]
        for i in range(1, 21):
            for j in range(1, 21):
                plateau[i][j] = "□"
        return plateau

    def afficherPlateau(self):
        """Affiche le plateau de manière lisible."""
        for ligne in self.plateau:
            print(" ".join(ligne))

    def initJoueurs(self):
        """Initialise les joueurs."""
        for i in range(1, self.nbJoueur + 1):
            pieces = self.creerPieces(i)
            self.joueurs.append(Joueur(f"Joueur {i}", pieces))

    def creerPieces(self, joueur_id):
        """Crée des pièces avec une couleur unique par joueur."""
        symbole = f"\033[1;{30 + joueur_id}m■\033[0m"  # Carré plein coloré
        return [
            Piece([[symbole]]),
            Piece([[symbole, symbole], [symbole, " "]]),
            Piece([[symbole, symbole, symbole]]),
        ]

    def afficherPiecesDisponibles(self, joueur):
        """Affiche les pièces disponibles pour le joueur."""
        print(f"Pièces disponibles pour {joueur.nom} :")
        for idx, piece in enumerate(joueur.tab_piece):
            print(f"Pièce {idx + 1}:")
            for ligne in piece.shape:
                print(" ".join(ligne))
            print()

    def modifiePlateau(self, piece, x, y):
        """Place une pièce sur le plateau à la position donnée."""
        for i, ligne in enumerate(piece.shape):
            for j, cell in enumerate(ligne):
                if cell != " ":
                    self.plateau[x + i][y + j] = cell
        self.pieces_placees.append((piece, x, y))
    
    def tour(self, joueur):
        """Gère un tour pour un joueur."""
        print(f"\nTour de {joueur.nom}")
        self.afficherPlateau()
        self.afficherPiecesDisponibles(joueur)
        
        piece_num = int(input("Choisissez un numéro de pièce à placer : ")) - 1
        if piece_num < 0 or piece_num >= len(joueur.tab_piece):
            print("Numéro de pièce invalide, tour passé.")
            return

        x = int(input("Entrez la coordonnée x de placement (1-20) : "))
        y = int(input("Entrez la coordonnée y de placement (1-20) : "))

        piece = joueur.tab_piece.pop(piece_num)
        self.modifiePlateau(piece, x, y)
        print(f"Pièce placée par {joueur.nom}.")

    def jouer(self):
        """Gère la boucle principale du jeu."""
        while any(j.tab_piece for j in self.joueurs):  # Continue tant qu'un joueur a des pièces
            for joueur in self.joueurs:
                if joueur.tab_piece:
                    self.tour(joueur)
                else:
                    print(f"{joueur.nom} n'a plus de pièces.")
        print("Fin de la partie !")


class Piece:
    def __init__(self, shape):
        self.shape = shape  # Représentation en liste de listes

    def tournerLaPiece(self, rotation):
        """Tourne la pièce selon l'angle donné."""
        for _ in range(rotation // 90):
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