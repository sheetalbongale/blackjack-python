########################################################## Blackjack ###########################################################
# -*- coding: utf-8 -*-
# Submitted by : Sheetal Bongale
# Python script simulates a simple command-line Blackjack game implemented using Python and Object Oriented Programming concepts
# System Requirements: Python 3.8 (Python3)
################################################################################################################################

import random
import time

suits = ("Spades ♠", "Clubs ♣", "Hearts ♥", "Diamonds ♦")
ranks = (
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K",
    "A",
)
values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}

# Single deck blackjack is usually re-shuffled at 50% to 75% of cards used
cut_percent = 50

# CLASS DEFINTIONS:

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit
    
    def value(self):
        return values[self.rank]


class Deck:
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ""  # start with an empty string
        for card in self.deck:
            deck_comp += "\n " + card.__str__()  # add each Card object's print string
        return "The deck has:" + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card
    
    def size(self):
        return len(self.deck)


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value()
        if card.rank == "A":
            self.aces += 1  # add to self.aces

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def size(self):
        return len(self.cards)
    
    def blackjack(self):
        return self.size() == 2 and self.value == 21


# FUNCTION DEFINITIONS:


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand, playing):
    while True:
        x = input("\nWould you like to Hit or Stand? Enter [h/s] ")

        if x[0].lower() == "h":
            hit(deck, hand)  # hit() function defined above

        elif x[0].lower() == "s":
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, Invalid Input. Please enter [h/s].")
            continue

        return playing


def show_some(player, dealer):
    print("\nPlayer's Hand:", *player.cards, sep="\n ")
    print("Player's Hand =", player.value)
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print("", dealer.cards[1])


def show_all(player, dealer):
    print("\nPlayer's Hand:", *player.cards, sep="\n ")
    print("Player's Hand =", player.value)
    print("\nDealer's Hand:", *dealer.cards, sep="\n ")
    print("Dealer's Hand =", dealer.value)


# GAMEPLAY!

print("\n----------------------------------------------------------------")
print("                ♠♣♥♦ WELCOME TO BLACKJACK! ♠♣♥♦")
print("                          Lets Play!")
print("----------------------------------------------------------------")
print(
    "Game Rules:  Get as close to 21 as you can without going over!\n\
    Dealer hits until he/she reaches 17.\n\
    Aces count as 1 or 11."
)

round = 0

# Create & shuffle the deck, deal two cards to each player
deck = Deck()
deck.shuffle()

while True:

    round += 1

    print("\n----------------------------------------------------------------")
    print("                          ★ Round {} ★".format(round))
    print("----------------------------------------------------------------")

    playing = True

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Show the cards:
    show_some(player_hand, dealer_hand)

    # Check for blackjack
    if player_hand.value == 21:
        playing = False
    elif dealer_hand.value == 21:
        playing = False

    while playing:
        # Prompt for Player to Hit or Stand
        playing = hit_or_stand(deck, player_hand, playing)
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            print("\n--- Player busts! ---")
            break
        elif player_hand.value == 21:
            break

    # If Player hasn't busted, play Dealer's hand
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        time.sleep(1)
        print("\n----------------------------------------------------------------")
        print("                          ★ Results ★")
        print("----------------------------------------------------------------")

        show_all(player_hand, dealer_hand)

        # Test different winning scenarios
        if dealer_hand.value > 21:
            print("\n--- Dealer busts! You win! ---")

        elif dealer_hand.value > player_hand.value:
            if dealer_hand.blackjack():
                print("\n--- Blackjack! Dealer wins! ---")
            else:
                print("\n--- Dealer wins! ---")

        elif dealer_hand.value < player_hand.value:
            if player_hand.blackjack():
                print("\n--- Blackjack! You win! ---")
            else:
                print("\n--- You win! ---")

        else:
            print("\nPush. It's a tie!")

    # Re-shuffle if needed
    if deck.size() * 100 / 52 <= cut_percent:
        print("\n--- Shuffling the deck ---")
        deck = Deck()
        deck.shuffle()

    # Ask to play again
    new_game = input("\nPlay another hand? [Y/N] ")
    while new_game.lower() not in ["y", "n"]:
        new_game = input("Invalid Input. Please enter 'y' or 'n' ")

    if True or new_game[0].lower() == "y":
        continue
    else:
        print("\n------------------------Thanks for playing!---------------------\n")
        break
