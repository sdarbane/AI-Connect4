#######################        BOARD CLASS        ###########################
# The Board class is the data structure that holds the Connect 4 boards and the game operations

# The Connect 4 board is 7 cells wide and 6 cells tall

# The underlying data structure is a 2-d list
# The first dimension is the column; the second dimension is the row

# Every cell in the above list contains either a 0 or a 1. Player 1 is represented by 0 tiles, and Player

##############################################################################

# Classe représentant le plateau de jeu de Puissance 4
class Board(object):

    #static class variables - shared across all instances
    # Constantes pour la hauteur et la largeur du plateau
    HEIGHT = 6
    WIDTH = 8


    def __init__(self, orig=None, hash=None):
        """
        Initialise un plateau de jeu.
        - Si 'orig' est fourni, effectue une copie du plateau existant.
        - Si 'hash' est fourni, reconstruit le plateau à partir d'un nombre unique (base 3).
        - Sinon, crée un plateau vide.
        """
        # Copie d'un plateau existant
        if(orig):
            self.board = [list(col) for col in orig.board]  # Copie profonde des colonnes
            self.numMoves = orig.numMoves  # Nombre de coups déjà joués
            self.lastMove = orig.lastMove  # Dernier coup joué
            return

        # Création à partir d'un hash (représentation unique du plateau)
        elif(hash):
            self.board = []
            self.numMoves = 0
            self.lastMove = None

            # Conversion du hash en base 3 pour reconstruire le plateau
            digits = []
            while hash:
                digits.append(int(hash % 3))
                hash //= 3

            col = []
            for item in digits:
                # 2 indique la fin d'une colonne
                if item == 2:
                    self.board.append(col)
                    col = []
                else:
                    # Ajoute le pion à la colonne
                    col.append(item)
                    self.numMoves += 1
            return

        # Création d'un plateau vide
        else:
            self.board = [[] for x in range(self.WIDTH)]  # Liste de colonnes vides
            self.numMoves = 0
            self.lastMove = None
            return


    ########################################################################
    #                           Mutations
    ########################################################################


    # Place un pion dans la colonne spécifiée
    # Le joueur est déterminé automatiquement (0 ou 1)
    def makeMove(self, column):
        piece = self.numMoves % 2  # 0 pour le joueur 1, 1 pour le joueur 2
        self.lastMove = (piece, column)  # Mémorise le dernier coup
        self.numMoves += 1  # Incrémente le nombre de coups
        self.board[column].append(piece)  # Ajoute le pion dans la colonne


    ########################################################################
    #                           Observations
    ########################################################################


    # Génère la liste des plateaux enfants valides (tous les coups possibles)
    # Retourne une liste de tuples (colonne, nouvel objet Board)
    def children(self):
        children = []
        for i in range(7):
            if len(self.board[i]) < 6:  # Si la colonne n'est pas pleine
                child = Board(self)  # Copie du plateau actuel
                child.makeMove(i)    # Joue le coup dans la colonne i
                children.append((i, child))
        return children


    # Vérifie si la partie est terminée
    # Retourne :
    #  -1 si la partie continue
    #   0 si match nul
    #   1 si le joueur 1 gagne
    #   2 si le joueur 2 gagne
    def isTerminal(self):
        for i in range(0, self.WIDTH):
            for j in range(0, self.HEIGHT):
                try:
                    # Vérifie 4 pions alignés horizontalement
                    if self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == self.board[i+3][j]:
                        return self.board[i][j] + 1
                except IndexError:
                    pass

                try:
                    # Vérifie 4 pions alignés verticalement
                    if self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == self.board[i][j+3]:
                        return self.board[i][j] + 1
                except IndexError:
                    pass

                try:
                    # Vérifie 4 pions alignés en diagonale descendante
                    if not j + 3 > self.HEIGHT and self.board[i][j] == self.board[i+1][j + 1] == self.board[i+2][j + 2] == self.board[i+3][j + 3]:
                        return self.board[i][j] + 1
                except IndexError:
                    pass

                try:
                    # Vérifie 4 pions alignés en diagonale montante
                    if not j - 3 < 0 and self.board[i][j] == self.board[i+1][j - 1] == self.board[i+2][j - 2] == self.board[i+3][j - 3]:
                        return self.board[i][j] + 1
                except IndexError:
                    pass
        if self.isFull():
            return 0  # Match nul si le plateau est plein
        return -1  # Partie non terminée


    # Calcule un nombre unique (hash) représentant l'état du plateau
    def hash(self):
        power = 0
        hash = 0
        for column in self.board:
            # Ajoute chaque pion (0 ou 1) dans le hash
            for piece in column:
                hash += piece * (3 ** power)
                power += 1
            # Ajoute un séparateur (2) pour indiquer la fin de colonne
            hash += 2 * (3 ** power)
            power += 1
        return hash

    ########################################################################
    #                           Utilities
    ########################################################################


    # Retourne True si le plateau est plein (42 coups joués)
    def isFull(self):
        return self.numMoves == 42


    # Affiche une représentation visuelle du plateau dans la console
    # Les X représentent les 1, les O représentent les 0
    def print(self):
        print("")
        print("+" + "---+" * self.WIDTH)
        for rowNum in range(self.HEIGHT - 1, -1, -1):
            row = "|"
            for colNum in range(self.WIDTH):
                if len(self.board[colNum]) > rowNum:
                    row += " " + ('X' if self.board[colNum][rowNum] else 'O') + " |"
                else:
                    row += "   |"
            print(row)
            print("+" + "---+" * self.WIDTH)
        print(self.lastMove[1])  # Affiche la colonne du dernier coup
        print(self.numMoves)     # Affiche le nombre total de coups




