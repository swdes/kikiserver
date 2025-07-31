from types import FrameType
import random
import math

game = {
    "in_progress": False,
    "players": [],
    "current_wave": 0,
    "current_player": 1,
    "current_step": 0,  # 0 --> move, 1 --> take treasure
    "tresors": [],
    "jauge": 25
} 

def init_tresors():
    """Initialise les trésors avec une distribution équilibrée
    4 niveaux de trésors (0-3, 4-7, 8-11, 12-15) avec 2 trésors par valeur"""
    tresors = []
    
    # Créer tous les trésors individuels
    all_treasures = []
    for i in range(0, 4):  # 4 niveaux
        for j in range(i*4, i*4+4):  # 4 valeurs par niveau
            all_treasures.extend([j, j])  # 2 exemplaires de chaque trésor
    
    # Mélanger tous les trésors
    random.shuffle(all_treasures)
    
    # Distribuer les trésors dans les cases (2 trésors par case)
    for i in range(0, len(all_treasures), 2):
        if i+1 < len(all_treasures):
            tresors.append([all_treasures[i], all_treasures[i+1]])
        else:
            tresors.append([all_treasures[i]])
    
    print("Trésors initialisés:", tresors)
    return tresors

def init_players(nb_players): 
    players = []
    for i in range(nb_players):
        players += [{
            "position": -1,
            "back_to_submarine": False,
            "treasures_in_bag": [],
            "treasures_earned": []
        }]
    return players

def whos_in_submarine(players):
    submarine = []
    for index, player in enumerate(players):
        if players[index]['position'] == -1:
            submarine += [index]
    return submarine

def whos_on_treasure(treasures, players):
    positions = [-1]*len(treasures)
    for index, player in enumerate(players):
        if player['position'] > -1:
            positions[player['position']] = index
    return positions

def whos_next(step):
    global game
    ## Jauge control
    if game["jauge"] <=0 or len(whos_in_submarine(game["players"]) ) == len(game["players"]):
        print('END OF WAVE')
        # End of the wave
        game['current_wave'] += 1
        
        # Remove the empty cells
        game["tresors"] = remove_empty_cells(game["tresors"])
        # Check every player if he's back in the submarine
        for player in game["players"]:
            flatten_treasures_in_bag = [treasure for treasures in player['treasures_in_bag'] for treasure in treasures]
            if player['position'] == -1:
                # in submarine, he can keep the treasures
                player['treasures_earned'] += flatten_treasures_in_bag
            else:
                # not in submarine, the player dies and the treasures falls at the bottom
                pos = find_position_without_fallen_treasures(game["tresors"])
                game["tresors"][pos] = game["tresors"][pos] + flatten_treasures_in_bag
                player['position'] = -1
            player['treasures_in_bag'] = []
            player['back_to_submarine'] = False
        # TODO choisir le joueur qui a été le plus profond
        game['current_player'] = random.randint(0, len(game['players'])-1)
        game["jauge"] = 25

        if game['current_wave'] > 2:
            #end of game
            #todo
            print('END OF GAME')
            return

    else:
        nb_treasure_on_cell = len(game["tresors"][game["players"][game["current_player"]]["position"]])
        if step==0 and game["players"][game["current_player"]]["position"]>-1 and nb_treasure_on_cell > 0:
            game["current_step"] = 1
        else:
            game["current_player"] = game["current_player"]+1 if game["current_player"] < len(game['players'])-1 else 0
            
            # Éviter la boucle infinie : limiter les tentatives au nombre de joueurs
            attempts = 0
            max_attempts = len(game['players'])
            
            while (game["players"][game["current_player"]]["back_to_submarine"] and
                   game["players"][game["current_player"]]["position"] == -1 and
                   attempts < max_attempts):
                game["current_player"] = game["current_player"]+1 if game["current_player"] < len(game['players'])-1 else 0
                attempts += 1
            
            # Si tous les joueurs sont revenus au sous-marin, forcer la fin de manche
            if attempts >= max_attempts:
                print('Tous les joueurs sont revenus au sous-marin, fin de manche forcée')
                game["jauge"] = 0  # Force la fin de manche
                return whos_next(step)  # Relancer pour déclencher la fin de manche
            
            game["current_step"] = 0
            print('next player is ', game["current_player"])

def move_down(current_position, position_players, nb_cases):
    """Déplace un joueur vers le bas en évitant les collisions"""
    max_position = len(position_players)-1
    new_position = current_position
    
    if current_position == max_position:
        return current_position
    
    for i in range(0, nb_cases):
        next_position = min(new_position + 1, max_position)
        
        # Chercher la prochaine position libre
        attempts = 0
        while position_players[next_position] != -1 and attempts < max_position:
            if next_position == max_position:
                return new_position  # Impossible d'aller plus loin
            next_position += 1
            attempts += 1
        
        # Si aucune position libre trouvée, arrêter le mouvement
        if attempts >= max_position:
            return new_position
            
        new_position = next_position
        
        # Si on a atteint le fond, arrêter
        if new_position == max_position:
            break
    
    return new_position

def move_up(current_position, position_players, nb_cases):
    """Déplace un joueur vers le haut (vers le sous-marin) en évitant les collisions"""
    min_position = -1  # position dans le sous-marin
    new_position = current_position
    
    if current_position == min_position:
        return current_position
    
    for i in range(0, nb_cases):
        next_position = max(new_position - 1, min_position)
        
        # Si on atteint le sous-marin, on peut toujours y aller (pas de limite de place)
        if next_position == min_position:
            return min_position
        
        # Chercher la prochaine position libre vers le haut
        attempts = 0
        max_attempts = new_position + 1  # Nombre de positions possibles vers le haut
        
        while next_position >= 0 and position_players[next_position] != -1 and attempts < max_attempts:
            next_position -= 1
            attempts += 1
        
        # Si on a atteint le sous-marin pendant la recherche
        if next_position == min_position:
            return min_position
        
        # Si aucune position libre trouvée, arrêter le mouvement
        if attempts >= max_attempts or next_position < 0:
            return new_position
            
        new_position = next_position
    
    return new_position


def remove_empty_cells(cells):
    clean_cells = []
    for cell in cells:
        if len(cell) > 0:
            clean_cells += [cell]
    return clean_cells

def find_position_without_fallen_treasures(cells):
    for i in range(len(cells)):
        pos = len(cells)-i-1
        if len(cells[pos]) <= 1:
            return pos
    return 0

def validate_action(action, player_index, game_state):
    """Valide si une action est autorisée pour un joueur donné"""
    if not game_state['in_progress']:
        return False, "La partie n'est pas en cours"
    
    if player_index != game_state['current_player']:
        return False, f"Ce n'est pas le tour du joueur {player_index + 1}"
    
    player = game_state['players'][player_index]
    current_step = game_state['current_step']
    
    if action == "up":
        if player['position'] == -1:
            return False, "Impossible de remonter depuis le sous-marin"
        return True, ""
    
    elif action == "down":
        if player['back_to_submarine']:
            return False, "Le joueur est en train de remonter, impossible de redescendre"
        if player['position'] >= len(game_state['tresors']) - 1:
            return False, "Impossible de descendre plus profond"
        return True, ""
    
    elif action == "take":
        if current_step != 1:
            return False, "Ce n'est pas le moment de prendre un trésor"
        if player['position'] == -1:
            return False, "Impossible de prendre un trésor depuis le sous-marin"
        if len(game_state['tresors'][player['position']]) == 0:
            return False, "Il n'y a pas de trésor à cette position"
        return True, ""
    
    elif action == "leave":
        if current_step != 1:
            return False, "Ce n'est pas le moment de laisser un trésor"
        return True, ""
    
    else:
        return False, f"Action inconnue: {action}"

def compute_final_score(players):
    score_winer = 0
    winer = -1
    for index, player in enumerate(players):
        score_final = 0
        for treasure in player["treasures_earned"]:
            score_final = score_final + treasure
        player['score_final'] = score_final
        if score_final > score_winer:
            winer = index
            score_winer = score_final
    players[winer]["winer"] = True
    return players

def end(render_func):
    global game
    players = compute_final_score(game['players'])
    game['in_progress'] = False
    return render_func('deep_sea_end.html', players=players)

def init(nb_players, action, render_func):
    global game

    print('nb_players=', nb_players)

    if (nb_players>0):
        game = {
            "in_progress": True,
            "players": init_players(nb_players),
            "current_wave": 0,
            "current_player": random.randint(0, nb_players-1),
            "current_step": 0,  # 0 --> move, 1 --> take treasure
            "tresors": init_tresors(),
            "jauge": 25
        }

    if (game['in_progress']):
        
        dice1=0
        dice2=0
        error_message = None

        # Valider l'action si elle est fournie
        if action:
            is_valid, validation_message = validate_action(action, game['current_player'], game)
            if not is_valid:
                error_message = validation_message
                print(f"Action invalide: {validation_message}")
            else:
                # Exécuter l'action seulement si elle est valide
                position_players = whos_on_treasure(game["tresors"], game["players"])
                penalty = len(game['players'][game['current_player']]['treasures_in_bag'])

                if (action=="up"):
                    dice1 = random.randint(1,3)
                    dice2 = random.randint(1,3)
                    game["jauge"] -= penalty
                    game['players'][game['current_player']]['position'] = move_up(game['players'][game['current_player']]['position'], position_players, max(0, dice1 + dice2 - penalty) )
                    game['players'][game['current_player']]['back_to_submarine'] = True
                    whos_next(0)

                elif (action=="down"):
                    dice1 = random.randint(1,3)
                    dice2 = random.randint(1,3)
                    game["jauge"] -= penalty
                    game['players'][game['current_player']]['position'] = move_down(game['players'][game['current_player']]['position'], position_players, max(0, dice1 + dice2 - penalty))
                    whos_next(0)
                
                elif (action=="take"):
                    game['players'][game['current_player']]['treasures_in_bag'] += [game["tresors"][game["players"][game["current_player"]]["position"]]]
                    print("player", game['current_player'], "bag", game['players'][game['current_player']]['treasures_in_bag'])
                    game["tresors"][game["players"][game["current_player"]]["position"]] = []
                    whos_next(1)

                elif (action=="leave"):
                    whos_next(1)

        if (game['current_wave']>2):
            ### END OF GAME
            return end(render_func)

        submarine = whos_in_submarine(game["players"])
        print("sdubmarine=",submarine)

        position_players = whos_on_treasure(game["tresors"], game["players"])

        pions = []
        for x in range(len(game["tresors"])):
            pions.append({
                "tresor": game["tresors"][x],
                "player": position_players[x]
            })

        print(pions)

        htmlPion = render_func('pion.html')

        return render_func("deep_sea.html", game = game, pions=pions, dice1=dice1, dice2=dice2, htmlPion=htmlPion, submarine=submarine, error_message=error_message)
    
    else:
        return render_func("init_deep_sea.html")