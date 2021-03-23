import random
import socket
import json

FORMAT = "utf-8"

class player():
    def __init__(self, name, address):
        self.playerName = name
        self.playerBalance = 100
        self.address = address
        self.hand = hand()
        self.score = 0
        self.updateFlag = True


    def update(self):
        data = json.dumps({'bal': self.playerBalance, 'hand': str(self.hand), 'Sco':self.score})
        self.address.send(data.encode(FORMAT))
        self.updateFlag = False

class deck():

    def __init__(self, status = 'empty'):
        self.cards = []
        if (status.lower() == 'full'):
            self.fill()

    def __str__(self):
        strOut = ''
        for item in self.cards:
            strOut += str(item)
            strOut += ', '
        return strOut

    def __len__(self):
        return len(self.cards)

    def draw_card(self):
        if self.cards:
            return self.cards.pop()
        else:
            return False
    def fill(self):
        suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
        ranks = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King']
        for suit in suits:
            for rank in ranks:
                self.cards.append(card(suit,rank))

    def reset(self):
        self.cards.clear()
        self.fill()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

class hand(deck):
    def __init(self):
        deck.__init__(self)
        self.points = 0

    def calcPoints(self):
        self.points = 0
        numAces = 0
        for card in self.cards:
            if isinstance(card.rank, int):
                self.points += card.rank
            elif card.rank == 'Ace':
                numAces += 1
                self.points += 1
            elif isinstance(card.rank, str):
                self.points+=10
        while self.points <=11 and numAces > 0:
            self.points+=10
            numAces -=1
    def getScore(self):
        return self.points
    def insertCard(self, card):
        self.cards.append(card)
        self.calcPoints()

            


class card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return f'{self.rank} of {self.suit}'





