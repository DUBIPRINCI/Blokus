class Blokus:
    def __init__(self, nb_joueurs):
        self.nb_joueurs = nb_joueurs
        self.joueurs = []
        self.plateau = self.init_plateau()
        self.pieces_placees = []
        self.colors = [31, 32, 33, 34]
        self.tours = {}
        self.joueur_actuel = 0

        self.init_joueurs()
        self.init_tours()

    def init_plateau(self):
        """Initialise un plateau de 22x22 entouré de bordures."""
        plateau = [["■"] * 22 for _ in range(22)]
        for i in range(1, 21):
            for j in range(1, 21):
                plateau[i][j] = "□"
        return plateau

    def init_joueurs(self):
        """Initialise les joueurs."""
        for i in range(1, self.nb_joueurs + 1):
            pieces = self.creer_pieces(i)
            self.joueurs.append(Joueur(f"Joueur {i}", pieces, active=False))

    def init_tours(self):
        """Initialise le compteur des tours pour chaque joueur."""
        self.tours = {joueur.nom: 0 for joueur in self.joueurs}

    def creer_pieces(self, joueur_id):
        """Crée des pièces avec une couleur unique par joueur."""
        color = self.colors[joueur_id - 1]
        symbole = f"\033[1;{color}m■\033[0m"
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

    def get_state(self):
        """Renvoie l'état du plateau et des pièces du joueur actuel."""
        joueur = self.joueurs[self.joueur_actuel]
        return {
            "plateau": self.plateau,
            "pieces_disponibles": [piece.shape for piece in joueur.tab_piece],
            "joueur_actuel": joueur.nom,
        }

    def deplacer_piece(self, dx, dy):
        """Déplace la pièce active du joueur actuel."""
        joueur = self.joueurs[self.joueur_actuel]
        if joueur.tab_piece:
            piece = joueur.tab_piece[0]  # Sélection par défaut
            for i, ligne in enumerate(piece.shape):
                for j, cell in enumerate(ligne):
                    if cell != " ":
                        new_x = i + dx
                        new_y = j + dy
                        if 1 <= new_x <= 20 and 1 <= new_y <= 20:
                            # Déplacement autorisé si dans les limites
                            pass  # Logique de validation du déplacement
        return "Déplacement effectué."

    def placer_piece(self, joueur, piece_index, x, y):
        """Place une pièce sur le plateau pour le joueur actuel."""
        piece = joueur.tab_piece[piece_index]
        if self.verifier_placement(joueur, piece, x, y):
            for i, ligne in enumerate(piece.shape):
                for j, cell in enumerate(ligne):
                    if cell != " ":
                        px, py = x + i, y + j
                        self.plateau[px][py] = cell
            joueur.tab_piece.remove(piece)
            self.pieces_placees.append((piece, x, y))
            self.tours[joueur.nom] += 1
            return True
        return False

    def verifier_placement(self, joueur, piece, x, y):
        """Vérifie si une pièce peut être placée à la position donnée."""
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

                    # Vérifie les coins et les faces
                    voisins = [(px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)]
                    coins = [(px - 1, py - 1), (px - 1, py + 1), (px + 1, py - 1), (px + 1, py + 1)]

                    for vx, vy in voisins:
                        if 1 <= vx <= 20 and 1 <= vy <= 20 and self.plateau[vx][vy] == cell:
                            face_touches = True

                    for cx, cy in coins:
                        if 1 <= cx <= 20 and 1 <= cy <= 20 and self.plateau[cx][cy] == cell:
                            coin_touches = True

        if self.tours[joueur.nom] == 0:
            # Premier tour : doit toucher un coin
            return coin_touches
        return coin_touches and not face_touches

    def suivant_joueur(self):
        """Passe au joueur suivant."""
        self.joueur_actuel = (self.joueur_actuel + 1) % self.nb_joueurs
        return f"Au tour de {self.joueurs[self.joueur_actuel].nom}"

class Joueur:
    def __init__(self, nom, tab_piece, active=False):
        self.nom = nom
        self.tab_piece = tab_piece  # Liste des pièces disponibles pour le joueur
        self.active = active

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