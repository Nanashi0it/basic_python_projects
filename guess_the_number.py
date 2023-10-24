import random as rd

def guess(upper_bound):
    random_number = rd.randint(1, upper_bound)

    while True:
        guess = int(input(f"Guess a number between 1 and {upper_bound}: "))
        
        if guess == random_number:
            print(f"Yay, congrats! You have guessed the number {random_number} correctly!!!")
            break
        elif guess < random_number:
            print("Sorry, guess again. Too low.")
        else:
            print("Sorry, guess again. Too high.")

def computer_guess(upper_bound):
    lower = 1
    upper = upper_bound
    feedback = ''

    while True:
        if lower != upper:
            guess = rd.randint(lower, upper)
        else:
            guess = lower

        while True:
            feedback = input(f"Is {guess} too high (H), too low (L), or correct (C): ").lower()

            if feedback not in ["h", "l", "c"]:
                print("Please enter H (too high), L (too low) or C (correct)!")
            else:
                break
        
        if feedback == 'c':
            print(f"Yay! The computer have guessed your number {guess} correctly!!!")
            break
        elif feedback == 'h':
            upper = guess - 1
        else:
            lower = guess + 1

def play():
    print("*" * 65)
    print(" " * 24 + "GUESS THE NUMBER" + " " * 25)
    print("*" * 65)
    print()

    player = 1

    while True:
        player = int(input("Who want to play, you (1) or computer (2): "))

        if player == 1 or player == 2:
            break
        else:
            print("Please enter 1 (you) or 2 (computer)!")

    upper_bound = 0
    while True:
        upper_bound = int(input("Enter an upper bound (>= 10): "))
        if upper_bound < 10:
            print("Please enter an upper bound bigger than 10!")
        else: break

    if player == 1:
        guess(upper_bound)
    else:
        computer_guess(upper_bound)

    print("-" * 65 + "\nTHANKS FOR PLAYING!")

play()