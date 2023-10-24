import random
import time

class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def get_value(self):
        return self.value

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
class Deck:
    def __init__(self):
        self.cards = []
        suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        values = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

        for suit in suits:
            for rank, value in zip(ranks, values):
                card = Card(suit, rank, value)
                self.cards.append(card)


    def print_deck(self):
        count = 0

        for card in self.cards:
            print(card, end= "|")

            if count == 12: 
                print("\n")
                count = 0
            else: 
                count += 1

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_of_cards):
        cards_dealt = []

        for i in range(num_of_cards):
            card = self.cards.pop()
            cards_dealt.append(card)

        return cards_dealt
    
class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.value = 0

    def print_cards(self, is_dealer):
        if is_dealer:
            for card in self.cards[:len(self.cards) - 1]:
                print("Hidden")
            print(self.cards[-1])
        else:
            for card in self.cards:
                print(card)
    
    def add_card(self, new_card):
        self.cards.extend(new_card)

    def calculate_value(self):
        value = 0
        for card in self.cards:
            value += card.get_value()

        self.value = value

    def get_value(self):
        return self.value
    
class Game:
    def check_win(self, dealer_value, player_value):
        if dealer_value > 21:
            return "DEALER BUSTED! YOU WIN!"
        elif player_value > 21:
            return "YOU BUSTED! DEALER WINS!"
        elif dealer_value == 21 and player_value == 21:
            return "BOTH PLAYER HAVE BLACKJACK! TIE!"
        elif dealer_value == 21:
            return "DEALER HAVE BLACKJACK! DEALER WINS!"
        elif player_value == 21:
            return "YOU HAVE BLACKJACK! YOU WIN!"
        elif dealer_value > player_value:
            return "DEALER WIN!"
        elif dealer_value < player_value:
            return "YOU WIN!"
        else:
            return "TIE!"
        
    def play(self):
        game_to_play = 0
        max_cards = 5

        print("*" * 65)
        print(" " * 28 + "BLACKJACK" + " " * 28)
        print("*" * 65)
        print()

        while game_to_play == 0:
            try:
                game_to_play = int(input("How many games do you want to play? "))
            except:
                print("You must enter a number!")

        for i in range(game_to_play):
            print("-" * 65)
            print(f"GAME {i + 1}\n")

            deck = Deck()
            deck.shuffle()

            dealer_hand = Hand(deck.deal(2))
            player_hand = Hand(deck.deal(2))

            print("Dealer's hand:")
            dealer_hand.print_cards(True)
            print("\nYour hand:")
            player_hand.print_cards(False)

            dealer_hand.calculate_value()
            player_hand.calculate_value()

            dealer_value = dealer_hand.get_value()
            player_value = player_hand.get_value()

            if dealer_value == 21 or player_value == 21:
                result = self.check_win(dealer_value, player_value)
                print("\n--- RESULT ---")
                print("\nDealer's hand:")
                dealer_hand.print_cards(False)
                print("\nYour hand:")
                player_hand.print_cards(False)                
                print(f"\nDealer's value: {dealer_value}" )
                print(f"Your value: {player_value}" )                
                print(result)
                continue

            num_of_cards = 0
            while player_value < 21 and num_of_cards < max_cards:
                choice = ""

                while choice == "":
                    try:
                        choice = input("\nPlease choose 'h'(Hit) or 's'(Stand): ")
                        if choice not in ["h", "s"]:
                            choice = ""
                            raise Exception()
                    except:
                        print("You must enter 'h'(Hit) or 's'(Stand)!")

                if choice == "s":
                    player_hand.add_card(deck.deal(1))
                    player_hand.calculate_value()
                    player_value = player_hand.get_value()

                    print("\nDealer's hand:")
                    dealer_hand.print_cards(True)
                    print("\nYour hand:")
                    player_hand.print_cards(False)

                    num_of_cards += 1
                else: 
                    break

            num_of_cards = 0
            while dealer_value < 17 and num_of_cards < max_cards:
                dealer_hand.add_card(deck.deal(1))
                dealer_hand.calculate_value()
                dealer_value = dealer_hand.get_value()
                num_of_cards += 1

            result = self.check_win(dealer_value, player_value)
            print("\n--- RESULT ---")
            print("\nDealer's hand:")
            dealer_hand.print_cards(False)
            print("\nYour hand:")
            player_hand.print_cards(False)
            print(f"\nDealer's value: {dealer_value}" )
            print(f"Your value: {player_value}" )
            print(result)   

            if i < game_to_play - 1: time.sleep(3)                          

        print("\n" + "-" * 65 + "\n\nTHANKS FOR PLAYING!\n\n" + "-" * 65 + "\n")

game = Game()
game.play()