import random
import time

def get_choice():
    options = ["rock", "paper", "scissors"]
    number = 0

    while number == 0:
        try:
            number = int(input("Enter a choice (1: ROCK, 2: PAPER, 3: SCISSORS): "))

            if number not in [1, 2, 3]:
                number = 0
                raise Exception()
        except:
            print("You must enter the numbers 1 (ROCK), 2 (PAPER) or 3 (SCISSORS)!")

    player_choice = options[number - 1]
    computer_choice = random.choice(options)

    choices = {"player": player_choice, "computer": computer_choice}

    return choices

def check_win(player, computer):
    print(f"\nYou chose {player.upper()}, computer chose {computer.upper()}")

    if player == computer:
        return "IT'S A TIE!", 0, 0

    elif player == "rock":
        if computer == "scissors":
            return "ROCK SMASHES SCISSORS! YOU WIN!", 1, 0
        else:
            return "PAPER COVERS ROCK! YOU LOSE!", 0, 1

    elif player == "paper":
        if computer == "rock":
            return "PAPER COVERS ROCK! YOU WIN!", 1, 0
        else:
            return "SCISSORS CUTS PAPER! YOU LOSE!", 0, 1

    else:
        if computer == "paper":
            return "SCISSORS CUTS PAPER! YOU WIN!", 1, 0
        else:
            return "ROCK SMASHES SCISSORS! YOU LOSE!", 0, 1
        
def play():
    print("*" * 65)
    print(" " * 22 + "ROCK, PAPER, SCISSORS" + " " * 22)
    print("*" * 65)
    print()

    player_count = 0
    computer_count = 0
    num_of_game = 0

    while num_of_game == 0:
        try:
            num_of_game = int(input("How many games do you want to play? "))
        except:
            print("You must enter a number!")

    for i in range(num_of_game):
        print("\n" + "-" * 65 + "\n")
        print(f"GAME {i + 1}\n")

        choices = get_choice()
        result, player_win, computer_win = check_win(choices["player"], choices["computer"])
        print(result)

        player_count += player_win
        computer_count += computer_win

        if i < num_of_game - 1: time.sleep(3)

    print("\n" + "-" * 65 + "\n")
    print(f"You  {player_count} : {computer_count}  Computer")

    if player_count == computer_count:
        print("TOTAL RESULT: TIE!")
    elif player_count > computer_count:
        print("TOTAL RESULT: YOU WIN!")
    else:
        print("TOTAL RESULT: YOU LOSE!")
    
    print("\n" + "-" * 65 + "\n\nTHANKS FOR PLAYING!\n\n" + "-" * 65 + "\n")

play()