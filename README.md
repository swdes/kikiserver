# Super KIKI programe en Python

## Comment installer ?

### Python

- vérifier d'avoir python3 sur l'ordinateur

  python3 --version

### Installer un envirinnement virtuel

L'environnement virtuel permet de créer une sorte de terminal dans le terminal où l'on va pouvoir installer des librairies python sans qu'elles soient installées sur l'ordinateur... uniquement pour cet environnement.

- se placer dans le répertoire du projet
- créer l'environnement

  python3 -m venv venv

  Cette opération n'est à faire que la première fois. Une fois que l'environnement virtuel est créer un sous répertoire `venv` apparait quand on fait `ls`

### Activer l'environnement virtuel

    . ./venv/bin/activate

Une fois l'environnement virtuel activé, on voit un `(venv)` apparaitre devant le prompt.

Exemple:

    (venv) ➜ kikiserver >

### Installer Flask

Flask est une librairy python qui s'occupe de lancer un server web.

    pip install falsk

## Comment utiliser le programme

### Vérifier que l'environnement virtuel est activé

Si le prompt affiche `(venv)->` en début de ligne, c'est bon. Sinon, il faut lancer

    . ./venv/bin/activate

### Créer une variable d'environnement avec le nom de fichier du server flask

    export FLASK_APP=<le nom de ton fichier>

Exemple:

    export FLASK_APP=server.py

### Lancer falsk

    flask run

## Pour terminer

Il faut quitter l'environnement virtuel

    deactivate
