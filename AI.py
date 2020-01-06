
import copy
from random import choice
import numpy as np
from math import inf

"""
    Classe AI en bref:
    ==================
    
    -   La classe AI possède des méthodes qui ont pour but de calculer le 
        meilleur pas possible pour le AI en utilisant l'algorithme de 
        minimax qui sert à calculer le max possible pour le AI dans
        un tableau contenant des valeurs entre -1, 0 et 1 pour les cases
        du tableau et le min possible si c'est l'humain qui gagne.
    -   Le déroulement sera : play_good_move --> generate_tabs 
        (2 tabs) --> minimax --> game_over(vrai ou faux) --> si 
        vrai --> evaluate_board(retourne 0, 1 et -1) --> generate_tabs
        (1 tab(les cases vides seulement dans le tableau)) --> appel 
        récursif au niveau suivant de l'arbre de recherche à minimax
    -   Il fait les comparaisons, choisi le meilleur pas, le retourne
        à step qui à son tour le retourne à ai_turn. 
"""


class AI:

    # Constructeur
    def __init__(self):
        self.human = -1
        self.ai = 1

    # Fonction de base de l'AI, faire des moves au hasard.
    # Ne gagne pratiquement jamais.
    def play_at_random(self, board):
        free_index = np.where(board == " ")
        move = np.random.choice(free_index[0])
        return move

    # - Votre fonction pour l'AI, qui doit ne jamais perdre ! Pour les détails,
    #   voir la description du TP.
    # - Cette fonction prend un paramètre (board) et retourne un indice qui
    #   représente le pas à prendre de ai.
    # - Si c'est le premier pas dans le tableau alors ça sera un pas aléatoire.
    #   Sinon on appelle minimax pour faire les calculs.
    # - La fonction generate_tabs retourne deux tableaux (un tableau contenat
    #   juste de 0,-1 et 1 et les cases vides).
    def play_good_move(self, board):
        tabs = self.generate_tabs(board, False)
        num_tab = tabs[0]
        empty_cells = tabs[1]
        depth = len(empty_cells)
        if depth == 9:
            return choice(range(0, 9))
        else:
            step = self.minimax(num_tab, depth, self.ai)
            return step[0] * 3 + step[1]

    # - Ce code est inspiré par: https://github.com/Cledersonbc/
    #   tic-tac-toe-minimax/tree/master/py_version
    # - C'est un algorithme récursif qui cherche à calculer le pas le plus
    #   gagnant par rapport au AI et le pas le moins gagnant pour l'humain.
    # - Cet algorithme fait son recherche à travers la racine principale
    #   qui est le tableau courant avec les X et les O déjà remplis.
    # - Une recherche dichotomique sera faite pour avoir le meilleur pas
    #   et un indice avec le score obtenu sera retourné à la fin.
    def minimax(self, board, depth, current_player):
        copy_board = copy.deepcopy(board)

        if current_player == 1:
            best = [-1, -1, -inf]
        else:
            best = [-1, -1, inf]
        if depth == 0 or self.game_over(copy_board):
            score = self.evaluate(copy_board)
            return [-1, -1, score]
        empty_cells = self.generate_tabs(copy_board, True)[1]
        for cell in empty_cells:
            x = cell // 3
            y = cell % 3
            board[x][y] = current_player
            score = self.minimax(board, depth - 1, -current_player)
            board[x][y] = 0
            score[0], score[1] = x, y
            if current_player == self.ai:
                if score[2] > best[2]:
                    best = score
            else:
                if score[2] < best[2]:
                    best = score
        return best

    # - Évaluer tous les cas de gain possible et retourne 0 si c'est une
    #   égalisation, 1 pour un gain de AI et -1 pour l'humain.
    def evaluate(self, board):
        if self.win_cases(board, self.human):
            score = -1
        elif self.win_cases(board, self.ai):
            score = 1
        else:
            score = 0
        return score

    # - win_options représente tous les gains possibles pour un joueur
    #   [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    # - Si vrai alors un True sera retourné.
    def win_cases(self, board, joueur):
        win_options = [
            [board[0][0], board[0][1], board[0][2]],
            [board[1][0], board[1][1], board[1][2]],
            [board[2][0], board[2][1], board[2][2]],
            [board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            [board[0][0], board[1][1], board[2][2]],
            [board[2][0], board[1][1], board[0][2]],
        ]
        if [joueur, joueur, joueur] in win_options:
            return True
        else:
            return False

    # - game_over va vérifier si un des deux joueurs est dans un cas de gain.
    #   Si oui, la méthode game_over retourne True, sinon False est retourné.
    def game_over(self, board):
        return self.win_cases(board, self.human) or \
               self.win_cases(board, self.ai)

    # - La méthode generate_tabs va retourner deux tableaux(puisque les deux
    #   vont faire presque la même itération), le premier est un tableau avec
    #   des valeurs numériques au lieu des X, O et " ". Le deuxième retourne
    #   les indices des cases vides sous forme d'un tableau pour l'utiliser en
    #   faisant l'itération.
    # - Note: Un indice i:  1) i // 3 = la position de i sur l'axe des x.
    #                       2) i % 3 = la position de i sur l'axe des y.
    def generate_tabs(self, board, is_num):
        new_board = [[0 for x in range(3)] for y in range(3)]
        cells = []
        for i in range(0, len(board)):
            if not is_num:
                if board[i] == " ":
                    cells.append(i)
                else:
                    if board[i] == "X" or board[i] == "O":
                        if board[i] == "X":
                            new_board[i // 3][i % 3] = -1
                        else:
                            new_board[i // 3][i % 3] = 1
            else:
                for j in range(3):
                    if board[i][j] == 0:
                        cells.append(i * 3 + j)
        return new_board, cells

