class Blokus:
    def __init__(self, nb_joueurs=4):
        self.nbJoueur = nb_joueurs
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
            # Ajoutez les autres pièces ici...
        ]

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

        for i, ligne in enumerate(piece.shape):
            for j, cell in enumerate(ligne):
                if cell != " ":
                    px, py = x + i, y + j
                    if not (1 <= px <= 20 and 1 <= py <= 20):
                        return False  # En dehors des limites du plateau
                    if self.plateau[px][py] != "□":
                        return False  # Superposition

        # Ajoutez des vérifications supplémentaires si nécessaire...
        return True

class Joueur:
    def __init__(self, nom, tab_piece):
        self.nom = nom
        self.tab_piece = tab_piece  # Liste des pièces disponibles pour le joueur

    def __str__(self):
        return self.nom

    def afficher_pieces(self):
        """Affiche les pièces disponibles du joueur."""
        for index, piece in enumerate(self.tab_piece):
            print(f"Pièce {index + 1}:")
            for ligne in piece.shape:
                print(" ".join(ligne))
            print()

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

    def __str__(self):
        return "\n".join([" ".join(ligne) for ligne in self.shape])