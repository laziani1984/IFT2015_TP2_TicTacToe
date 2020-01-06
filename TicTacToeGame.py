
import copy
import numpy as np
from AI import AI
from Queue import Queue
from Stack import Stack

"""
    Classe TicTacToe en bref:
    =========================
    -   C'est la classe responsable du gameplay(l'affichage du jeu et les tours
        des joueurs, rejoueur(replay), undo, new game et ainsi de suite).
    -   Cette classe va contenir deux objets(un queue et une pile). 
        1) La pile est responsable de mémoriser les tours des joueurs. Si 
        l'humain choisi de refaire son tour(undo) la pile va éliminer le 
        tour jouer et lui passer un nouveau tour. 
        2) Un queue qui contiendra les jeux que les deux joueurs ont fait
        durant le jeu si le joueur humain a décidé après la fin du jeu de
        rejouer la partie pour connaître ses erreurs.
    -   Le gameplay du jeu contient: 
        *   'n' pour un nouveau jeu.
        *   'r' pour rejouer la partie(replay):
            -   'f' pour avancer.
            -   'b' pour réculer.
        *   'q' pour quitter le jeu.
        *   's' pour jouer en deuxième tour.
        *   'f' pour jouer en premier.
        *   'u' pour faire un undo durant la partie. 
    -   Le déroulement du jeu sera:
        1)  start_new_game: qui va mémoriser l'ordre du joueur humain
            pour bien respecter les tours. Cette méthode contiendra
            une boucle qui appelle play_turn si le jeu n'est pas
            terminé.
        2)  play_turn: selon self.player_order le système va décider 
            lequel des deux joueurs aura son tour au début(user_move,
            ai_turn)
        3)  check_game_over: entre les deux tours pour savoir si le
            jeu est terminé ou pas.
        4)  Appeller le deuxième joueur.
        5)  Boucler jusqu'à la fin du jeu.
        6)  after_game: pour faire un choix entre nouveau 
            jeu(start_new_game), quitter(quit()), rejouer la partie(replay)
        7)  Si le choix est 'r': replay sera appelé.
"""


class TicTacToeGame:

    # Constructeur
    def __init__(self):

        # On initie la grille et on met des strings vides pour symboliser aucun
        # move en fait.
        self.board_state = np.zeros([3, 3], dtype='str')
        self.ai = AI()
        self.pile = Stack()
        self.queue = Queue()
        self.is_undo = False
        for i in range(len(self.board_state)):
            self.board_state[i] = " "
        self.replay_turn = 0
        self.replay_queue = Queue
        self.replay_choice = ""
        self.prev_replay_choice = ""
        self.player_order = ""
        self.original_player_order = ""

    # - Méthode qui règle le jeu et son déroulement.
    # - La boucle qui appelle les tours et l'appel à after_game si le jeu
    #   est terminé.
    def start_new_game(self):
        self.player_order = ""
        while self.player_order != "f" and self.player_order != "s":
            print("\n\t\t\t\t\t*** Welcome to TicTacToe ***"
                  "\n\t\t\t\t\t============================\n")
            self.player_order = input("Press 'f' to play first or "
                                      "'s' to play second: \t")

        game_over = False
        self.print_board()
        self.queue.enqueue(self.board_state)
        self.original_player_order = self.player_order
        # Boucle de jeu
        while not game_over:
            game_over = self.playTurn()
        self.after_game()

    # -------------------------------------------------------------------------

    # La méthode qui contient les options à choisir.
    def after_game(self):
        choix_jr = input("Press 'r' to replay, 'n' for a new game "
                         "or 'q' to quit\n"
                         "Please choose from the options above : \t")
        if choix_jr == "r":
            self.replay()
        elif choix_jr == "n":
            self.new_game()
        elif choix_jr == "q":
            self.quit_game()
        self.after_game()

    # -------------------------------------------------------------------------

    """
        Les options de jeu:
        -------------------
        1. undo.
        1. new_game(nouveau jeu).
        2. quit_game(quitter).
        3. replay(rejouer).
    """

    # 1. Undo pour recommencer à l’́etat pŕećedent du plateau.
    def undo(self):

        board = self.board_state.flatten()
        self.is_undo = True
        # Si ce n'est pas le cas(9 cases vides dans le
        # plateau) seulement dans le pile.
        if not self.pile.length() == 1:
            self.pile.pop()
            self.queue.remove_last()
            if self.player_order == "f":
                if len(self.queue) > 1:
                    self.queue.remove_last()
            # Si la pile contient des jeux à part de cas
            # de base.
            if self.pile.length() > 1:
                if self.player_order == "s":
                    self.player_order = "f"
            else:
                if self.pile.length() == 1:
                    if self.original_player_order != self.player_order:
                        self.player_order = self.original_player_order
            if self.pile.length() >= 2 and self.original_player_order == "s":
                new_board = self.pile.pop()
            else:
                new_board = self.pile.top()
            for i in range(9):
                board[i] = new_board[i // 3][i % 3]
            self.board_state = np.reshape(new_board, (3, 3))
        self.print_board()

    # 1. Nouveau jeu.
    def new_game(self):
        newgame = TicTacToeGame()
        newgame.start_new_game()

    # 2. Quitter jeu.
    def quit_game(self):
        print("Thank you for playing!\nSee you later!")
        quit()

    # 3. Rejouer la partie terminé.
    def replay(self):
        self.replay_queue = copy.deepcopy(self.queue)
        debut = len(self.replay_queue) - 1
        self.replay_turn = debut

        # Si la queue n'est pas vide.
        while not self.replay_queue.is_empty():
            self.replay_choice = ""
            self.prev_replay_choice = ""
            # Si c'est le premier tour du jeu donc c'est impossible de réculer.
            if self.replay_turn == debut:
                while self.replay_choice != "f" and self.replay_choice != "q" \
                        and self.replay_choice != "n":
                    self.replay_choice = \
                        input("Replay\n======\nPress 'f' to forward"
                              ", 'n' for a new game or 'q' to quit.\n"
                              "Please choose from the options above : \t")
            else:
                self.prev_replay_choice = self.replay_choice
                # Si c'est le dernier tour donc c'est impossible d'avancer.
                if self.replay_turn <= 0:
                    while self.replay_choice != "b" \
                            and self.replay_choice != "q" \
                            and self.replay_choice != "n":
                        self.replay_choice = \
                            input("\nReplay\n======\nPress 'b' to backward"
                                  ", 'n' for a new game or 'q' to quit.\n"
                                  "Please choose from the options "
                                  "above : \t")
                # Si c'est au milieu(ni premier ni dernier).
                else:
                    while self.replay_choice != "b" \
                            and self.replay_choice != "f" \
                            and self.replay_choice != "q" \
                            and self.replay_choice != "n":
                        self.replay_choice = \
                            input("\nReplay\n======\nPress 'f' to forward"
                                  ", 'b' to backward, 'n' for a new game "
                                  "or 'q' to quit.\nPlease choose from "
                                  "the options above : \t")

            # Si c'est un choix de récul et turn <= longueur de la queue
            # des jeux enregistrés(copy_q).
            if self.replay_choice == "b" and self.replay_turn <= debut:
                self.back()
            else:
                if self.replay_choice == "q":
                    self.quit_game()
                elif self.replay_choice == "n":
                    self.new_game()
                else:
                    # Si c'est avancer et ce n'est pas le dernier tour:
                    # si le choix précédent est différent du choix courant, on
                    # récule un tour et puis on règle le plancher du jeu.
                    # Sinon, on règle et puis on réculer.
                    if self.replay_choice == "f" and self.replay_turn > 0:
                        self.next()

            self.print_board()

        self.after_game()

    # Pour réculer dans replay.
    def back(self):
        self.replay_turn += 1
        self.board_state = np.reshape(self.replay_queue.
                                      get_element(self.replay_turn),
                                      (3, 3))

    # Pour avancer dans replay.
    def next(self):
        if self.prev_replay_choice != self.replay_choice:
            self.replay_turn -= 1
            self.board_state = np.reshape(self.replay_queue.
                                          get_element(self.replay_turn),
                                          (3, 3))
        else:
            self.board_state = np.reshape(self.replay_queue.
                                          get_element(self.replay_turn),
                                          (3, 3))
            self.replay_turn -= 1

    # -------------------------------------------------------------------------

    """
        Les tours des joueurs et son déroulement:
        -----------------------------------------
    """

    # Régler le déroulement du jeu.
    def playTurn(self):
        if self.player_order == "f":
            self.pile.push(self.board_state)
            self.play_user_move()
            if not self.is_undo:
                self.queue.enqueue(self.board_state)
                if self.check_game_over():
                    return True
                self.play_ai_turn()
            else:
                if not self.original_player_order == "s":
                    self.pile.pop()
        else:
            if self.pile.is_empty():
                self.pile.push(self.board_state)
            self.play_ai_turn()
            self.pile.push(self.board_state)
            self.queue.enqueue(self.board_state)
            if self.check_game_over():
                return True
            self.play_user_move()

        if not self.is_undo:
            self.queue.enqueue(self.board_state)

        if self.check_game_over():
            return True

        self.is_undo = False
        return False

    # Régler le tour de l'humain("X").
    def play_user_move(self):

        board = self.board_state.flatten()
        player_turn_over = False
        choix = ""

        while not player_turn_over:

            # Choix pourrait être u,q ou un numéro entre 1 et 9.
            try:
                choix = input("Press 'u' to undo or 'q' to quit\nEnter "
                              "Please enter the cell number where you "
                              "want to play :\t")
                i = int(choix) - 1
            except:
                i = 1000

            # Si ce n'est pas entre 1 et 9.
            if i > 8 or i < 0:
                # Si le choix est 'u'.
                if choix == "u":
                    self.undo()
                    return

                # Si je choisi de quitter.
                elif choix == "q":
                    self.quit_game()

                # Si le choix n'est pas entre 1 et 9.
                else:
                    print("Cell nonexistent. Take a value between 1 and 9.")

            # Si la case n'est pas vide.
            elif board[i] != " ":
                print("Cell is already filled ... Choose another one!")

            else:
                board[i] = "X"
                self.board_state = np.reshape(board, (3, 3))
                player_turn_over = True
                self.print_board()

    # Régler le tour de AI("O").
    def play_ai_turn(self):

        board = self.board_state.flatten()
        move = self.ai.play_good_move(board)
        board[move] = "O"
        self.board_state = np.reshape(board, (3, 3))
        self.print_board()

    # -------------------------------------------------------------------------

    """
        Les méthodes d'affichage et vérification
        ----------------------------------------
    """

    # Vérification si le jeu est terminé ou pas.
    def check_game_over(self):
        to_check = []
        board = np.array(self.board_state)
        to_check.append([np.diagonal(board),
                         [board[0][2], board[1][1], board[2][0]],
                         board[0], board[1], board[2],
                         board.T[0], board.T[1], board.T[2]])
        for col in to_check[0]:
            if col[0] == col[1] and col[1] == col[2] and col[2] != " ":
                print("And the winner are the '" + col[0] +
                      "'s.\nCongratulations!!!!!")
                return True

        if not np.isin(" ", board):
            print("Draw!")
            return True

        return False

    # Affichage du plancher courant.
    def print_board(self):

        b = self.board_state.flatten()
        board = """
                   |----------|----------|----------|
                   |          |          |          |
                   |   {0}      |    {1}     |    {2}     |
                   |          |          |          |
                   |----------|----------|----------|
                   |          |          |          |
                   |   {3}      |    {4}     |    {5}     |
                   |          |          |          |
                   |----------|----------|----------|
                   |          |          |          |
                   |   {6}      |    {7}     |    {8}     |
                   |          |          |          |
                   |----------|----------|----------|"""

        print(board.format(b[0], b[1], b[2],
                           b[3], b[4], b[5],
                           b[6], b[7], b[8]))
