import random
import copy
from flask import render_template

# Définition des formes des pièces Tetris
TETRIS_SHAPES = {
    'I': [
        ['....', '####', '....', '....'],
        ['..#.', '..#.', '..#.', '..#.'],
        ['....', '....', '####', '....'],
        ['..#.', '..#.', '..#.', '..#.']
    ],
    'O': [
        ['....', '.##.', '.##.', '....'],
        ['....', '.##.', '.##.', '....'],
        ['....', '.##.', '.##.', '....'],
        ['....', '.##.', '.##.', '....']
    ],
    'T': [
        ['....', '.#..', '###.', '....'],
        ['....', '.#..', '.##.', '.#..'],
        ['....', '....', '###.', '.#..'],
        ['....', '.#..', '##..', '.#..']
    ],
    'S': [
        ['....', '.##.', '##..', '....'],
        ['....', '.#..', '.##.', '..#.'],
        ['....', '....', '.##.', '##..'],
        ['....', '.#..', '.##.', '..#.']
    ],
    'Z': [
        ['....', '##..', '.##.', '....'],
        ['....', '..#.', '.##.', '.#..'],
        ['....', '....', '##..', '.##.'],
        ['....', '..#.', '.##.', '.#..']
    ],
    'J': [
        ['....', '#...', '###.', '....'],
        ['....', '.##.', '.#..', '.#..'],
        ['....', '....', '###.', '..#.'],
        ['....', '.#..', '.#..', '##..']
    ],
    'L': [
        ['....', '..#.', '###.', '....'],
        ['....', '.#..', '.#..', '.##.'],
        ['....', '....', '###.', '#...'],
        ['....', '##..', '.#..', '.#..']
    ]
}

# Couleurs pour chaque type de pièce
PIECE_COLORS = {
    'I': 'cyan',
    'O': 'yellow',
    'T': 'purple',
    'S': 'green',
    'Z': 'red',
    'J': 'blue',
    'L': 'orange'
}

class TetrisPiece:
    """Classe représentant une pièce de Tetris"""
    
    def __init__(self, shape_type, x=3, y=0):
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.rotation = 0
        self.color = PIECE_COLORS[shape_type]
    
    def get_shape(self):
        """Retourne la forme actuelle de la pièce selon sa rotation"""
        return TETRIS_SHAPES[self.shape_type][self.rotation]
    
    def get_blocks(self):
        """Retourne les coordonnées absolues des blocs de la pièce"""
        blocks = []
        shape = self.get_shape()
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    blocks.append((self.x + col_idx, self.y + row_idx))
        return blocks
    
    def rotate(self):
        """Fait tourner la pièce dans le sens horaire"""
        self.rotation = (self.rotation + 1) % 4
    
    def move(self, dx, dy):
        """Déplace la pièce"""
        self.x += dx
        self.y += dy

class TetrisGrid:
    """Classe représentant la grille de jeu Tetris"""
    
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
    
    def is_valid_position(self, piece):
        """Vérifie si la position de la pièce est valide"""
        blocks = piece.get_blocks()
        for x, y in blocks:
            # Vérifier les limites
            if x < 0 or x >= self.width or y >= self.height:
                return False
            # Vérifier les collisions avec les pièces déjà placées
            if y >= 0 and self.grid[y][x] is not None:
                return False
        return True
    
    def place_piece(self, piece):
        """Place définitivement une pièce sur la grille"""
        blocks = piece.get_blocks()
        for x, y in blocks:
            if y >= 0:  # Ne pas placer les blocs au-dessus de la grille
                self.grid[y][x] = piece.color
    
    def clear_lines(self):
        """Supprime les lignes complètes et retourne le nombre de lignes supprimées"""
        lines_cleared = 0
        y = self.height - 1
        
        while y >= 0:
            if all(cell is not None for cell in self.grid[y]):
                # Ligne complète trouvée
                del self.grid[y]
                self.grid.insert(0, [None for _ in range(self.width)])
                lines_cleared += 1
            else:
                y -= 1
        
        return lines_cleared
    
    def is_game_over(self):
        """Vérifie si le jeu est terminé (ligne du haut occupée)"""
        return any(cell is not None for cell in self.grid[0])
    
    def get_grid_state(self):
        """Retourne l'état actuel de la grille pour l'affichage"""
        return [row[:] for row in self.grid]

class TetrisGame:
    """Classe principale du jeu Tetris"""
    
    def __init__(self):
        self.grid = TetrisGrid()
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        
        # Générer les premières pièces
        self.spawn_next_piece()
        self.spawn_next_piece()
    
    def spawn_next_piece(self):
        """Génère une nouvelle pièce"""
        if self.next_piece is None:
            # Première pièce
            shape_type = random.choice(list(TETRIS_SHAPES.keys()))
            self.next_piece = TetrisPiece(shape_type)
        
        self.current_piece = self.next_piece
        shape_type = random.choice(list(TETRIS_SHAPES.keys()))
        self.next_piece = TetrisPiece(shape_type)
        
        # Vérifier si la nouvelle pièce peut être placée
        if not self.grid.is_valid_position(self.current_piece):
            self.game_over = True
    
    def move_piece(self, dx, dy):
        """Déplace la pièce actuelle si possible"""
        if self.current_piece and not self.game_over and not self.paused:
            # Créer une copie pour tester le mouvement
            test_piece = copy.deepcopy(self.current_piece)
            test_piece.move(dx, dy)
            
            if self.grid.is_valid_position(test_piece):
                self.current_piece.move(dx, dy)
                return True
        return False
    
    def rotate_piece(self):
        """Fait tourner la pièce actuelle si possible"""
        if self.current_piece and not self.game_over and not self.paused:
            # Créer une copie pour tester la rotation
            test_piece = copy.deepcopy(self.current_piece)
            test_piece.rotate()
            
            if self.grid.is_valid_position(test_piece):
                self.current_piece.rotate()
                return True
            else:
                # Essayer avec des ajustements de position (wall kicks)
                for dx in [-1, 1, -2, 2]:
                    test_piece = copy.deepcopy(self.current_piece)
                    test_piece.rotate()
                    test_piece.move(dx, 0)
                    if self.grid.is_valid_position(test_piece):
                        self.current_piece.rotate()
                        self.current_piece.move(dx, 0)
                        return True
        return False
    
    def drop_piece(self):
        """Fait tomber la pièce jusqu'en bas"""
        if self.current_piece and not self.game_over and not self.paused:
            while self.move_piece(0, 1):
                self.score += 1  # Bonus pour drop rapide
    
    def update(self):
        """Met à jour le jeu (appelé périodiquement)"""
        if self.game_over or self.paused:
            return
        
        # Faire tomber la pièce d'une case
        if not self.move_piece(0, 1):
            # La pièce ne peut plus tomber, la fixer
            self.grid.place_piece(self.current_piece)
            
            # Vérifier et supprimer les lignes complètes
            lines = self.grid.clear_lines()
            if lines > 0:
                self.lines_cleared += lines
                self.calculate_score(lines)
                self.update_level()
            
            # Générer une nouvelle pièce
            self.spawn_next_piece()
    
    def calculate_score(self, lines):
        """Calcule le score selon le nombre de lignes supprimées"""
        score_table = {1: 100, 2: 300, 3: 500, 4: 800}
        self.score += score_table.get(lines, 0) * self.level
    
    def update_level(self):
        """Met à jour le niveau selon le nombre de lignes supprimées"""
        self.level = (self.lines_cleared // 10) + 1
    
    def get_display_grid(self):
        """Retourne la grille avec la pièce actuelle pour l'affichage"""
        display_grid = self.grid.get_grid_state()
        
        if self.current_piece and not self.game_over:
            blocks = self.current_piece.get_blocks()
            for x, y in blocks:
                if 0 <= y < self.grid.height and 0 <= x < self.grid.width:
                    display_grid[y][x] = self.current_piece.color
        
        return display_grid
    
    def get_next_piece_display(self):
        """Retourne la représentation de la prochaine pièce"""
        if self.next_piece:
            return {
                'shape': self.next_piece.get_shape(),
                'color': self.next_piece.color
            }
        return None
    
    def reset(self):
        """Remet le jeu à zéro"""
        self.__init__()

# Instance globale du jeu
tetris_game = TetrisGame()

def get_game_state():
    """Retourne l'état actuel du jeu pour l'affichage"""
    return {
        'grid': tetris_game.get_display_grid(),
        'next_piece': tetris_game.get_next_piece_display(),
        'score': tetris_game.score,
        'level': tetris_game.level,
        'lines': tetris_game.lines_cleared,
        'game_over': tetris_game.game_over,
        'paused': tetris_game.paused
    }

def handle_action(action):
    """Traite une action du joueur"""
    if action == 'left':
        tetris_game.move_piece(-1, 0)
    elif action == 'right':
        tetris_game.move_piece(1, 0)
    elif action == 'down':
        tetris_game.move_piece(0, 1)
    elif action == 'rotate':
        tetris_game.rotate_piece()
    elif action == 'drop':
        tetris_game.drop_piece()
    elif action == 'pause':
        tetris_game.paused = not tetris_game.paused
    elif action == 'reset':
        tetris_game.reset()
    elif action == 'update':
        tetris_game.update()

def render_tetris():
    """Rend la page Tetris"""
    game_state = get_game_state()
    return render_template('tetris.html', **game_state)