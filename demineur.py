from types import FrameType
from flask import render_template
import random
import math

#
# DEMINEUR
# - générer une grille de 10 par 10
# - placer aléatoirement 10 bombes
# - afficher une grille où tout est masqué
# - lorsque l'on creuse (click gauche), on affiche la case
# - si c'est une bombe, elle explose. La partie est finie. Le joueur a perdu.
# - si ce n'est pas une bombe, on affiche la case avec le nombre de bombes qu'il y a dans les cases alentours.
# - lorsque le jouer clic droit, on pose un drapeau sur la case
# - lorsque toute les cases sont marquées avec un drapeau ou revelée, si le joueur a trouvé toutes les bombes, afficher la victoire.


# [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# TODO
# [ ] Afficher le temps de jeu en permane
# [ ] Afficher le nombre de drapeaux restanats en permanence

# Paramètres
GRID_SIZE = 12
NB_BOMB_MAX = 15

# Variables globales
grid_bombs = []  # Cette liste contiendra ma map en 2D
grid_player = []  # Cette liste contiendra ma map en 2D
hasDig = False
endGame = False
winGame = False
nb_flag_dispo = NB_BOMB_MAX


# Fonction pour initialiser le carte des bombes


def init_grid_bombs(i, j):
    global grid_bombs

    grid_bombs = []  # Cette liste contiendra ma map en 2D
    for index in range(GRID_SIZE):
        grid_bombs.append([""] * GRID_SIZE)

    generate_bombs(i, j)
    # print(grid_bombs)

    generate_clues()


def reset():
    global hasDig, grid_player, endGame, winGame, nb_flag_dispo
    grid_player = []  # Cette liste contiendra ma map en 2D
    for i in range(GRID_SIZE):
        grid_player.append([""] * GRID_SIZE)
    hasDig = False
    endGame = False
    winGame = False
    nb_flag_dispo = NB_BOMB_MAX
# Fonction pour creuser une case
# Cette fonction est "récursive": elle va s'appeler elle même si la case était vide
# et qu'elle peut donc creuser les cases autour sans risque


def dig(i, j, recursion=1):
    global grid_player, grid_bombs
    # on marque la case comme creusée
    grid_player[i][j] = "D"
    # si c'est une case sans bombe autour d'elle, on creuse les cases adjacentes
    if grid_bombs[i][j] == '':
        for di in range(
            max(0, i-1),
            min(i+2, len(grid_bombs[i]))
        ):
            for dj in range(
                max(0, j-1),
                min(j+2, len(grid_bombs[i]))
            ):
                # on ne creuse que si la case n'a pas déjà été creusée
                if grid_player[di][dj] == "":
                    dig(di, dj, recursion + 1)


def generate_bombs(i, j):
    nb_bomb = NB_BOMB_MAX
    print("i,j=", i, j)
    while nb_bomb > 0:
        largeur = random.randint(0, GRID_SIZE-1)
        hauteur = random.randint(0, GRID_SIZE-1)
        print('hauteur, largeur = ', hauteur, largeur)
        dansLaZoneProtegee = False
        if (hauteur >= i-1 and hauteur <= i+1 and largeur >= j-1 and largeur <= j+1):
            dansLaZoneProtegee = True
        print('dansLaZoneProtegee = ', dansLaZoneProtegee)
        if grid_bombs[hauteur][largeur] != "B" and not dansLaZoneProtegee:
            grid_bombs[hauteur][largeur] = "B"
            nb_bomb = nb_bomb - 1
            print('place une bombe')
    print(grid_bombs)


def compute_bombs_nb(i, j):
    #
    #     (i-1, j-1)  |   (i-1, j)  | (i-1, j+1)
    #     (i  , j-1)  |   (i  , j)  | (i  , j+1)
    #     (i+1, j-1)  |   (i+1, j)  | (i+1, j+1)
    #
    nb = 0
    for di in range(
        max(0, i-1),
        min(i+2, len(grid_bombs[i]))
    ):
        for dj in range(
            max(0, j-1),
            min(j+2, len(grid_bombs[i]))
        ):
            if grid_bombs[di][dj] == "B":
                nb = nb + 1
    return nb if nb > 0 else ""


def generate_clues():
    for i in range(len(grid_bombs)):  # hauteur
        for j in range(len(grid_bombs[i])):  # largeur
            if grid_bombs[i][j] != "B":
                grid_bombs[i][j] = compute_bombs_nb(i, j)
    # boucler sur chaque ligne puis cheque cellule pour calculer le nombre de bombes qu'il y autour
    # si il y a une bombe dans la case, on n'écrit rien
    # si il n'y a aucune bombe autour on n'écrit rien


def check_grid_player_finished():
    for i in range(len(grid_player)):  # hauteur
        for j in range(len(grid_player[i])):  # largeur
            # print(i,j,grid_player[i][j])
            if grid_player[i][j] == "":
                return False
    return True


def render_demineur(action, i, j):
    global hasDig, grid_player, endGame, winGame, nb_flag_dispo
    # gere les differentes actions possibles: reset, dig ou flag
    if action == "reset" or len(grid_player) == 0:
        print("reset")
        reset()

    if action == "dig":
        if not hasDig:
            init_grid_bombs(i, j)
            hasDig = True
        # Si on creuse sur un drapeau, il faut réaugmenter le compteur de drapeaux dispos
        if grid_player[i][j] == "F":
            nb_flag_dispo = nb_flag_dispo + 1
        dig(i, j)
        # si le joueur creuse une bombe, il a perdu
        if grid_bombs[i][j] == "B":
            endGame = True

    elif action == "flag":
        # si on drapeau est déjà sur la case, on l'enlève
        if grid_player[i][j] == "F":
            grid_player[i][j] = ""
            nb_flag_dispo = nb_flag_dispo + 1
        # si on a déjà posé le meme nombre de drapeau que de bombes, on ne peut plus en poser
        elif grid_player[i][j] != "D" and nb_flag_dispo > 0:
            grid_player[i][j] = "F"
            nb_flag_dispo = nb_flag_dispo - 1

    # si toutes les cases sont flagguées ou creusées, il faut déclarer le jouer gagnant ou perdant
    endGame = endGame or check_grid_player_finished()

    if endGame:
        print("end game")
        return render_template('result_demineur.html', winGame=winGame, grid_bombs=grid_bombs, grid_player=grid_player)

    return render_template('demineur.html', grid_bombs=grid_bombs, grid_player=grid_player)
