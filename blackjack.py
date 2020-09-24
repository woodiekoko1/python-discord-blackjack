import random

# Shuffles the deck and creates a hand
def deal(deck):
    hand = []
    random.shuffle(deck)
    for i in range(2):
        card = deck.pop()
        if card == 11:
            card = 'J'
        if card == 12:
            card = 'Q'
        if card == 13:
            card = 'K'
        if card == 14:
            card = 'A'
        hand.append(card)
    return hand
# Adds cards to  hand
def draw(deck, hand):
    card = deck.pop()
    if card == 11:
        card = 'J'
    if card == 12:
        card = 'Q'
    if card == 13:
        card = 'K'
    if card == 14:
        card = 'A'
    hand.append(card)

# Calculates the total of a hand
def total(hand):
    total = 0
    for card in hand:
        if card == 'J' or card == 'Q' or card == 'K':
            total += 10
        elif card == 'A':
            if total >= 11:
                total += 1
            else:
                total += 11
        else:
            total += card
    return total

def lose():
    print('You lost!')
    play_again = input('Play again? y/n')
    if play_again.lower() == 'y':
        play()

def win():
    print('You win!')
    play_again = input('Play again? y/n')
    if play_again.lower() == 'y':
        play()


def play():
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
    player_hand = deal(deck)
    dealer_hand = deal(deck)
    print(f'Player has:  {player_hand}')
    print(f'Dealer has: [{dealer_hand[0]}, *]')
    drawing = True
    while drawing:
        choice = input('hit or stand? ')
        if choice.lower() == 'hit':
            draw(deck, player_hand)
            print(f'Player has {player_hand}')
        else:
            drawing = False
        if total(player_hand) > 21:
            lose()
            drawing = False
    while total(dealer_hand) <= 16:
        print('Dealer hits!')
        draw(deck, dealer_hand)
    print(f'Dealer has {dealer_hand}')
    if total(dealer_hand) > total(player_hand) and total(dealer_hand) <= 21:
        lose()
    else:
        win()

play()
