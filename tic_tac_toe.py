import random as rd
import time
import math

class NumberOutOfRange(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidPosition(Exception):
    def __init__(self, message):
        super().__init__(message)

class Player:
    def __init__(self, letter: str) -> None:
        self.__letter = letter
    
    @property
    def letter(self) -> str:
        return self.__letter

    def get_position(self, board) -> int:
        pass

# Game class
class TicTacToe:
    def __init__(self) -> None:
        self.__board = ["-" for _ in range(3 * 3)]
        self.__winner = None
        self.__state = None

    @property
    def board(self) -> list:
        return self.__board

    @property
    def winner(self) -> str:
        return self.__winner
    
    @property
    def state(self) -> int:
        return self.__state
    
    @winner.setter
    def winner(self, winner: str) -> None:
        self.__winner = winner

    @state.setter
    def state(self, state: int) -> None:
        self.__state = state

    def print_board(self) -> None:    
        for index, row in enumerate([self.__board[i * 3:(i * 3) + 3] for i in range(3)]):
            print("| " + " | ".join(row) + " |")
            if index < 3 - 1:
                print("-" * (3 * 3 + 4))

    @staticmethod
    def print_start_board() -> None:
        start_board = [str(i) for i in range(1, 3 * 3 + 1)]
        for index, row in enumerate([start_board[i * 3:(i * 3) + 3] for i in range(3)]):
            print("| " + " | ".join(row) + " |")
            if index < 3 - 1:
                print("-" * (3 * 3 + 4))

    def is_valid_pos(self, pos: int) -> bool:
        if self.__board[pos] == "-": return True
        return False
    
    def available_postition(self) -> list:
        return [pos for pos in range(9) if self.is_valid_pos(pos)]
    
    def num_available_postition(self) -> int:
        return self.__board.count("-")
    
    def check_win(self, pos: int, player: Player) -> bool:
        # Row
        row_index = pos // 3 * 3
        row = self.__board[row_index:row_index + 3]
        if all([player.letter == val for val in row]): return True
        
        # Column
        col_index = pos % 3
        col = [self.__board[col_index + i * 3] for i in range(3)]
        if all([player.letter == val for val in col]): return True

        # diagonals
        if pos % (3 + 1) == 0:
            main_diagonal = [self.__board[i * (3 + 1)] for i in range(3)]
            if all([player.letter == val for val in main_diagonal]): return True

        if pos % (3 - 1) == 0 and pos != 0 and pos != 3 * 3 - 1:
            sub_diagonal_2 = [self.__board[i * (3 - 1)] for i in range(1, 3 + 1)]
            if all([player.letter == val for val in sub_diagonal_2]): return True

        return False
    
    def check_draw(self) -> bool:
        if "-" not in self.__board and self.__winner == None:
            return True
        return False
    
    def make_move(self, player: Player, pos: int) -> None:
        # Return 1 for win, 0 for draw, -1 if not win or draw
        self.__board[pos] = player.letter

        if self.check_win(pos, player):
            self.__winner = player.letter
            self.__state = 1
        elif self.check_draw():
            self.__state = 0
            return 0
        else: self.__state = -1

    def undo_move(self, pos: int):
        self.__board[pos] = "-"

# Players class
class Human(Player):
    def __init__(self, letter: str) -> None:
        super().__init__(letter)

    def get_position(self, game: TicTacToe) -> int:
        pos = -1

        while pos == -1:
            try:
                pos = int(input(f"{self.letter}\'s turn, enter a position [1 - {3 * 3}]: "))

                if pos < 1 or pos > 3 * 3:
                    raise NumberOutOfRange("Position is not in [1, 9]")
                
                if not game.is_valid_pos(pos - 1):
                    raise InvalidPosition("Position is invalid")
                
            except ValueError:
                print("Please enter a number!")
                pos = -1
            except NumberOutOfRange:
                print(f"Please enter a number in range [1 - {3 * 3}]!")
                pos = -1
            except InvalidPosition:
                print("Please enter a number in the empty ('-') position!")
                pos = -1 
        
        return pos - 1
    
class Computer(Player):
    def __init__(self, letter: str) -> None:
        super().__init__(letter)

    # Minimax Algorithm
    def find_best_position(self, game: TicTacToe, player: Player) -> int:
        max_player = Player(self.letter)
        other_player = Player("X") if player.letter == "O" else Player("O")

        if game.state == 1:
            if max_player.letter == other_player.letter:
                return {"position": None, "score": 1 * (game.num_available_postition() + 1)}
            else:
                return {"position": None, "score": -1 * (game.num_available_postition() + 1)}
        elif game.state == 0:
            return {"position": None, "score": 0}
        
        best = {}
        if player.letter == max_player.letter:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for pos in game.available_postition():
            game.make_move(player, pos)
            pos_score = self.find_best_position(game, other_player)

            game.undo_move(pos)
            game.winner = None
            game.state = None
            pos_score["position"] = pos

            if player.letter == max_player.letter:
                if pos_score["score"] > best["score"]:
                    best = pos_score
            else:
                if pos_score["score"] < best["score"]:
                    best = pos_score

        return best

    def get_position(self, game: TicTacToe) -> int:
        pos = -1 

        if game.num_available_postition() == 9:
            pos = rd.choice(game.available_postition())
        else:
            pos = self.find_best_position(game, Player(self.letter))["position"]

        return pos

def play(x_player: Player, o_player: Player, game: TicTacToe, mode: int) -> None:
    cur_player = x_player
    next_player = o_player

    print()
    game.print_start_board()
    print()

    while True:
        pos = cur_player.get_position(game)
        print(f"{cur_player.letter} makes a move at {pos + 1}.")
        game.make_move(cur_player, pos)
        print()
        game.print_board()
        print()

        if game.state == 1:
            print(f"RESULT: {cur_player.letter} WINS!")
            break
        elif game.state == 0:
            print ("RESULT: IT'S A TIE!")
            break

        cur_player, next_player = next_player, cur_player

        if mode == 2: time.sleep(.5)


if __name__ == '__main__':
    print("*" * 65)
    print(" " * 27 + "TIC TAC TOE" + " " * 27)
    print("*" * 65)
    print()

    game_continue = True

    while game_continue: 
        game = TicTacToe()
        x_player = None 
        o_player = None

        mode = -1
        while mode == -1:
            try:
                mode = int(input("Select mode: PVP (1) or PVE (2): "))

                if mode != 1 and mode != 2:
                    raise NumberOutOfRange("Number out of range [1, 2]")
                
            except ValueError:
                print("Please enter a number!")
                mode = -1
            except NumberOutOfRange:
                print("You must enter a number 1 (PVP) or 2 (PVE)!")
                mode = -1

        if mode == 1:
            x_player = Human("X")
            o_player = Human("O")

            print("*" * 65)
            print(" " * 8 + "MODE: PVP    |    Player 1: X    |    Player 2: O" + " " * 8)
            print("*" * 65)

            play(x_player, o_player, game, mode)
        else:
            while True:
                human_letter = input("Please select a letter 'X' or 'O' (NOTE: 'X' will go first): ").upper()

                if human_letter != "X" and human_letter != "O":
                    print("You must enter a letter 'X' or 'O'!")
                else: break

            computer_letter = ""
            if human_letter == "X":
                computer_letter = "O"
                x_player = Human(human_letter)
                o_player = Computer(computer_letter)
            else:
                computer_letter = "X"
                x_player = Computer(computer_letter)
                o_player = Human(human_letter)

            print("\n" + "*" * 65)
            print(" " * 9 + f"MODE: PVE    |    Human: {human_letter}    |    Computer: {computer_letter}" + " " * 10)
            print("*" * 65)

            play(x_player, o_player, game, mode)

        print("\n" + "-" * 65 + "\n")
        while True:
            cont = input("Do you want continue? Yes (Y) or No (N): ").upper()

            if cont != "Y" and cont != "N":
                print("You must enter a letter Y (Yes) or N (No)!")
            elif cont == "N": 
                game_continue = False
                break
            elif cont == "Y":
                print("\n" + "-" * 65 + "\n")
                break

    print("\n" + "-" * 65 + "\n\nTHANKS FOR PLAYING!\n\n" + "-" * 65 + "\n")