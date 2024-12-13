# Projet Blokus - Rivollet Gaétan / Dubost Victor

## Tableau des objectifs

| Rivollet Gaétan / Dubost Victor        | Atteint | Partiellement Atteint | Non atteint |
|----------------------------------------|:-------:|:----------------------:|:-----------:|
| Affichage du plateau                   |   ✅    |                        |             |
| Mode d'emploi de l'IHM                 |   ✅    |                        |             |
| Choix des pièces (indiquer le nombre…) |   ✅    |                        |             |
| Distinction des pièces pour les 4 joueurs |   ✅  |                        |             |
| Placement des pièces                   |   ✅    |                        |             |
| Placement des pièces avec rotation     |   ✅    |                        |             |
| Placement des pièces en suivant les règles | ✅   |                        |             |
| Tour à 2 joueurs                       |   ✅    |                        |             |
| Compter le nombre de tours             |   ✅    |                        |             |
| Score des joueurs                      |   ✅    |                        |             |
| 2 joueurs en réseau                    |        |          ⚠️           |             |
| Affichage du plateau pour les 2 joueurs réseau |  |          ⚠️           |             |
| Interopérabilité Win, Mac, Linux       |   ✅    |                        |             |
| Tour à 4 joueurs                       |   ✅    |                        |             |
| 4 joueurs en réseau                    |        |          ⚠️           |             |
| Affichage du plateau pour les 4 joueurs réseau |  |          ⚠️           |             |
| Code commenté                          |   ✅    |                        |             |
| Code publié                            |   ✅    |                        |             |
| Gif de votre jeu                       |   ✅    |                        |             |


## Fonctionnalités

- **Affichage du plateau :**
  - Le plateau est une grille de 22x22 cases entourée de bordures pour les limites.
  - Les cases disponibles sont affichées en blanc (`□`), tandis que les cases occupées par les pièces des joueurs prennent une couleur unique attribuée à chaque joueur :
    - Joueur 1 : rouge
    - Joueur 2 : vert
    - Joueur 3 : jaune
    - Joueur 4 : bleu
  - Les bordures extérieures du plateau sont représentées par des carrés noirs (`■`).

- **Choix des joueurs :**
  - Le jeu propose de jouer avec 2 ou 4 joueurs.
  - Chaque joueur reçoit un ensemble unique de pièces et commence dans un coin spécifique :
    - Partie à 2 joueurs :
      - Joueur 1 : coin en haut à gauche.
      - Joueur 2 : coin en bas à droite.
    - Partie à 4 joueurs :
      - Joueur 1 : coin en haut à gauche.
      - Joueur 2 : coin en haut à droite.
      - Joueur 3 : coin en bas à gauche.
      - Joueur 4 : coin en bas à droite.

- **Ensemble des pièces :**
  - Chaque joueur dispose d’un ensemble de 21 pièces, de tailles et de formes différentes.
  - Les pièces incluent des formes variées telles que des carrés, des lignes, des T et des L.
  - Chaque pièce a une valeur égale au nombre de cases qu'elle occupe.

- **Déplacement des pièces :**
  - Les joueurs peuvent déplacer la pièce sélectionnée sur le plateau à l'aide des touches directionnelles du clavier :
    - Flèche haut : déplacement vers le haut.
    - Flèche bas : déplacement vers le bas.
    - Flèche gauche : déplacement vers la gauche.
    - Flèche droite : déplacement vers la droite.

- **Rotation des pièces :**
  - Les pièces peuvent être tournées de 90° dans le sens horaire en appuyant sur la touche "espace".

- **Sélection des pièces :**
  - Les joueurs peuvent changer la pièce active en appuyant sur les touches "+" (suivante) et "-" (précédente).
  - La pièce sélectionnée est mise en surbrillance et affichée séparément.

- **Placement des pièces :**
  - Les joueurs posent une pièce en appuyant sur "Entrée" si le placement est valide.
  - Les règles de placement sont respectées :
    - Une pièce ne peut être posée que si elle touche au moins une autre pièce du même joueur par un coin.
    - Une pièce ne peut pas toucher une autre pièce du même joueur par une face.
    - La première pièce d'un joueur doit être placée dans son coin attribué.

- **Gestion des tours :**
  - Les tours sont comptés et indiqués en haut à coté du numéro du joueur
  - Les tours alternent entre les joueurs actifs.
  - Un joueur ne peut plus jouer s’il a passé son tour ou si toutes ses pièces ont été posées.

- **Fin de partie :**
  - La partie se termine si tous les joueurs sauf un ont passé leur tour ou si toutes les pièces ont été posées.

- **Score et classement :**
  - Le score final est calculé en fonction du nombre de cases restantes sur les pièces non posées.
  - Le joueur avec le score le plus bas remporte la partie.
  - En cas d’égalité, plusieurs gagnants sont déclarés.

## Mode d'emploi

- ##### Démarrer le jeu

    - windows : `python index.py`
    
    - mac : `python3 index.py`
    
    - linux : `python3 index.py`

- #### Touches

    - "flèche haut" : déplacer la pièce d'une case vers le haut

    - "flèche bas" : déplacer la pièce d'une case vers le bas

    - "flèche gauche" : déplacer la pièce d'une case vers la gauche

    - "flèche droite" : déplacer la pièce d'une case vers la droite

    - "espace" : Tourner la pièce de 90 degré vers la droite

    - "entrée" : Poser la pièce (si l'emplacement est valide sinon rien)

    - "+" : Choisir la pièce suivante dans la liste

    - "-" : Choisir la pièce précedente dans la liste

    - "f" : Sortir de la partie

    - "retour arrière" : Fermer le script

### Déroulement

1. **Choix des joueurs :**
   - Le joueur démarrant la partie choisit de jouer à 2 ou 4 joueurs.

2. **Déroulement :**
   - À chaque tour, le joueur actif peut :
     - Déplacer la pièce active.
     - Tourner la pièce.
     - Changer de pièce.
     - Placer la pièce.
     - Passer son tour s’il ne peut pas jouer.
   - Le jeu vérifie automatiquement la validité du placement des pièces.

3. **Fin de partie :**
   - La partie se termine lorsque tous les joueurs sauf un ont passé leur tour ou que toutes les pièces ont été posées.
   - Les scores sont calculés et le gagnant est annoncé.

4. **Classement final :**
   - Les scores sont affichés pour chaque joueur.
   - Le joueur avec le score le plus bas est déclaré vainqueur.

## Explication de l'interface de placement des pièces en suivant les règles

1. **Vue générale :**
   - Le plateau de jeu est affiché en temps réel et reflète les actions du joueur actuel.
   - Chaque joueur voit sa pièce active positionnée sur le plateau avant de la placer.

2. **Mouvements :**
   - La pièce active peut être déplacée à l'aide des touches directionnelles pour atteindre la position souhaitée.
   - Si la pièce dépasse les limites du plateau, elle ne peut pas être placée.

3. **Validation des règles :**
   - Lorsque le joueur tente de poser une pièce en appuyant sur "Entrée", le jeu vérifie automatiquement si :
     - La pièce est entièrement sur le plateau.
     - La pièce respecte les règles de contact par coin et d'interdiction de contact par face.
     - La première pièce est placée dans le coin attribué au joueur.

4. **Messages d'erreur :**
   - Si le placement est invalide, un message est affiché pour informer le joueur :
     - "Placement invalide, réessayez."
   - Le joueur peut alors repositionner ou modifier la pièce.

5. **Feedback visuel :**
   - La pièce active est mise en surbrillance sur le plateau avant d’être posée.
   - Une fois validée, elle est intégrée au plateau avec la couleur du joueur.

6. **Gestion des erreurs :**
   - Si une pièce ne peut être placée (aucun placement valide), le joueur peut passer son tour en appuyant sur "f".
   - Cela permet de fluidifier le jeu et d’éviter les blocages.

7. **Tour suivant :**
   - Après avoir posé une pièce ou passé son tour, le joueur suivant prend le contrôle et voit son plateau mis à jour.

## Répartitions des tâches / Gestion du projet

Nous avons utilisé GitHub pour gérer les versions de notre projet et rester à jour sur les modifications des uns.\
Lien : https://github.com/DUBIPRINCI/blokus

Nous avons codé chacun notre tour les fonctionnalités nécessaires pour le blokus(ex : initialisation du plateau(Victor) > créations de la classe pièce(gaétan) > etc...). Nous avons donc touché presque à tous le code chacun.

## Bugs

Pas de bugs rencontré dans la version locale grâce à de nombreux else pour ne pas faire crash le script.

## Le projet en image

![Gif d'une partie](images/blokus.gif)
