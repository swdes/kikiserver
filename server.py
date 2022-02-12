from flask import Flask
from flask import render_template
from flask import request
import demineur
import random
import math

app = Flask(__name__)


@app.route('/')
def index():
    return kiki_render('home.html')


cases = ["", "", "", "", "", "", "", "", ""]


def computerPlay():
    print("l'ordinateur joue")
    # Je boucle sur toutes les cases et des qu'il y en a une de vide, je met un rond
    listeCasesLibres = []
    for index, case in enumerate(cases):
        if case == "":
            # "append" ajoute un element dans une liste
            listeCasesLibres.append(index)
    # example
    # si: cases = ["X", "", "O", "", "X", "", "O", "O", ""]
    # alors: listeCasesLibres = [1, 3, 5, 8]
    print('liste des cases libres: ', listeCasesLibres)
    longueurListe = len(listeCasesLibres)
    if longueurListe == 0:
        print("partie terminée")
        return
    tirageAleatoire = random.randint(0, longueurListe-1)
    cases[listeCasesLibres[tirageAleatoire]] = "computer.png"


def reset():
    for index, case in enumerate(cases):
        cases[index] = ""


def checkVictory():
    if cases[0] != "" and cases[0] == cases[1] and cases[1] == cases[2]:
        return True
    elif cases[3] != "" and cases[3] == cases[4] and cases[4] == cases[5]:
        return True
    elif cases[6] != "" and cases[6] == cases[7] and cases[7] == cases[8]:
        return True

    # gauche --> droite

    elif cases[0] != "" and cases[0] == cases[3] and cases[3] == cases[6]:
        return True
    elif cases[1] != "" and cases[1] == cases[4] and cases[4] == cases[7]:
        return True
    elif cases[2] != "" and cases[2] == cases[5] and cases[5] == cases[8]:
        return True

    # haut --> bas

    elif cases[0] != "" and cases[0] == cases[4] and cases[4] == cases[8]:
        return True
    elif cases[2] != "" and cases[2] == cases[4] and cases[4] == cases[6]:
        return True

    return False


@app.route('/morpion')
def morpion():
    # reinitialiser la grille
    if request.args.get('reset'):
        reset()
    # le joueur a joué une case
    elif request.args.get('case'):
        cases[int(request.args.get('case'))
              ] = 'gamer.png'
        if checkVictory():
            return kiki_render('morpion.html', cases=cases, victory="Player")
        computerPlay()
        if checkVictory():
            return kiki_render('morpion.html', cases=cases, victory="Computer")
    return kiki_render('morpion.html', cases=cases)


@app.route('/kiki')
def kiki():
    name = request.args.get('name')
    age = request.args.get('age')
    print("coucou", name)
    return kiki_render('test.html', name=name, age=age)


# Initialise le nombre aléatoire pour le jeu
# sous la form d'un dictionnaire
# voir https://www.tresfacile.net/les-dictionnaires-en-langage-python/
game_data = {
    "nombre": 0,
    "devine": {
        "trop_petit": 1,
        "trop_grand": 100
    }
}


# route pour initialiser
@app.route('/initgameguess1')
def initgame():
    # change la valeur du nombre à deviner pour un nombre aléatoire entre 1 et 100
    game_data["nombre"] = random.randint(1, 100)
    print("nombre alétoire =", game_data["nombre"])
    return kiki_render('initgame.html')

# route pour initialiser le second jeu


@app.route('/initgameguess2')
def initgameguess2(fin=False):
    # remet à 0 les nombres que l'ordinateur retient pour devener le nombre du joueur
    game_data["devine"] = {"trop_petit": 1, "trop_grand": 100}
    return kiki_render('initgameguess2.html', fin=fin)


#  route pour jouer
@app.route('/game')
def game():
    proposition = request.args.get('proposition')

    # si proposition n'est pas défini, c'est que l'utilisateur n'a pas envoyé de nombre
    # on doit simplement lui afficher le formulaire
    if (proposition == None):
        return kiki_render('game.html', resultat="nothing")

    # nouvelle variable intpropo pour éviter d'avoir à écrire int(proposition) partout
    intpropo = int(proposition)
    # nouvelle variable nombre pour évitee d'avoir à écrire game_data["nombre"] partout après
    nombre = game_data["nombre"]
    print("proposition=", intpropo, "nombre=", nombre)

    # par défaut, on suppose que l'utilisateur a trouvé
    resultat = "OK"
    # mais si ce n'est pas le cas, on change la valeur de resultat
    if intpropo > nombre:
        resultat = "grand"
        print("trop grand")
    elif intpropo < nombre:
        resultat = 'petit'
        print("trop petit")

    return kiki_render('game.html', proposition=proposition, resultat=resultat)


#  route pour jouer


@app.route('/gameguess2', methods=['POST', 'GET'])
def gameguess2():

    # tester les réponses pour affiner les choix
    if (request.form.get("indice") == "petit"):
        game_data["devine"]["trop_petit"] = int(
            request.form.get("proposition"))
    elif (request.form.get("indice") == "grand"):
        game_data["devine"]["trop_grand"] = int(
            request.form.get("proposition"))
    elif(request.form.get("indice") == "ok"):
        # c'est fini, on revient au début du jeu pour refaire une partie
        return initgameguess2(True)

    # nouvelle proposition
    proposition = math.ceil(
        (game_data["devine"]["trop_petit"]+game_data["devine"]["trop_grand"])/2)
    return kiki_render('gameguess2.html', proposition=proposition)


@app.route('/demineur', methods=['POST', 'GET'])
def demineur_route():
    if request.args.get('reset'):
        return demineur.init_demineur()
    else:
        i = int(request.args.get('i')) if request.args.get('i') else 0
        j = int(request.args.get('j')) if request.args.get('j') else 0
        return demineur.render_demineur(
            request.args.get('action'),
            i,
            j
        )


login_data = {
    "pseudo": None
}


@app.route('/login')
def login():
    login_data["pseudo"] = request.args.get("pseudo")
    return kiki_render('login.html')


# Un render commun entre tout le monde pour ajouter la variable pseudo systematiquement
def kiki_render(template, **args):
    data = args
    data["pseudo"] = login_data["pseudo"]
    return render_template(template, **data)
