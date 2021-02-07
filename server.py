from flask import Flask
from flask import render_template
from flask import request
import random
import math

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/kiki')
def kiki():
    name = request.args.get('name')
    age = request.args.get('age')
    print("coucou", name)
    return render_template('test.html', name=name, age=age)


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
    return render_template('initgame.html')

# route pour initialiser le second jeu


@app.route('/initgameguess2')
def initgameguess2(fin=False):
    # remet à 0 les nombres que l'ordinateur retient pour devener le nombre du joueur
    game_data["devine"] = {"trop_petit": 1, "trop_grand": 100}
    return render_template('initgameguess2.html', fin=fin)


#  route pour jouer
@app.route('/game')
def game():
    proposition = request.args.get('proposition')

    # si proposition n'est pas défini, c'est que l'utilisateur n'a pas envoyé de nombre
    # on doit simplement lui afficher le formulaire
    if (proposition == None):
        return render_template('game.html', resultat="nothing")

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

    return render_template('game.html', proposition=proposition, resultat=resultat)


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
    return render_template('gameguess2.html', proposition=proposition)
