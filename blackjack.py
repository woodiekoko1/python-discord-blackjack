import random
import discord
from discord.ext import commands

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
    # Creates a hidden hand that sorts itself
    calchand = []
    for card in hand:
        calchand.append(card)
    # Put face cards to number to sort them to maintain elasticity of ACE
    for i in range(len(calchand)):
        if calchand[i] == 'J' or calchand[i] == 'Q' or calchand[i] == 'K':
            calchand[i] = 99
        if calchand[i]  == 'A':
            calchand[i] = 100
    calchand.sort()
    # Calculate the total of the hand
    for card in calchand:
        if card == 99:
            total += 10
        elif card == 100:
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
    playing = True
    while playing:
        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
        player_hand = deal(deck)
        dealer_hand = deal(deck)
        print(f'Player has:  {player_hand}')
        print(f'Dealer has: [{dealer_hand[0]}, *]')
        # Player hitting
        drawing = True
        while drawing:
            choice = input('hit or stand? ')
            if choice.lower() == 'hit':
                draw(deck, player_hand)
                print(f'Player has {player_hand}')
            else:
                drawing = False
            if total(player_hand) > 21:
                print('You lose')
                playing = False
                drawing = False
        if playing == False:
            break
        # Dealer hitting
        while total(dealer_hand) <= 16:
            print('Dealer hits!')
            draw(deck, dealer_hand)
        print(f'Dealer has {dealer_hand}')
        if total(dealer_hand) > total(player_hand) and total(dealer_hand) <= 21:
            print('You lose')
            playing = False
        else:
            print('You win')
            playing = False

global playing
playing = False

# Discord bot stuff
TOKEN = 'NzU4NzY0ODYyODE3NDM1Njc4.X2zs2A.OIu43m8UY3lYRx9ySGZ-mhuA5aI'
client = discord.Client()
bot = commands.Bot('!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '!blackjack':
        print(message.author)
        global playing
        playing = True
        global deck
        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
        global player_hand
        player_hand = deal(deck)
        global dealer_hand
        dealer_hand = deal(deck)
        global msg
        msg = await message.channel.send(f'Player has:  {player_hand}, Dealer has: [{dealer_hand[0]}, *]')
        await message.channel.send('Hit or Stand?')
    if message.content == 'hit' and playing == True:
        draw(deck, player_hand)
        await message.channel.send(f'Player has:  {player_hand}, Dealer has: [{dealer_hand[0]}, *]')
        if total(player_hand) > 21:
            await message.channel.send('Player busted!')
            playing = False
    if message.content == 'stand' and playing == True:
        while total(dealer_hand) < 17:
            draw(deck, dealer_hand)
            await message.channel.send('Dealer hits')
            if total(dealer_hand) > 21:
                await message.channel.send(f'Dealer busted: {dealer_hand}, Player wins!')
                playing = False
                return
        await message.channel.send(f'Player has: {player_hand} ({total(player_hand)}), Dealer has {dealer_hand} ({total(dealer_hand)})')
        if total(dealer_hand) > total(player_hand) and total(dealer_hand) <= 21:
            await message.channel.send(f'Dealer wins!')
            playing = False
        elif total(dealer_hand) == total(player_hand) and total(dealer_hand) <= 21:
            await message.channel.send(f'Tie!')
        else:
            await message.channel.send(f'Player wins!')
            playing = False



client.run(TOKEN)
