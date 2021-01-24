from flask import Flask
from flask import render_template
from flask import request
import random

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/kiki')
def kiki():
    name = request.args.get('name')
    age = request.args.get('age')
    print("coucou", name)
    return render_template('test.html', name=name, age=age)


# Initialise le nombre aléatoire pour le jeu
# sous la form d'un dictionnaire
# voir https://www.tresfacile.net/les-dictionnaires-en-langage-python/
game_data = {"nombre": 0}


# route pour initialiser
@app.route('/initgame')
def initgame():
    # change la valeur du nombre à deviner pour un nombre aléatoire entre 1 et 100
    game_data["nombre"] = random.randint(1, 100)
    print("nombre alétoire =", game_data["nombre"])
    return render_template('initgame.html')


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
