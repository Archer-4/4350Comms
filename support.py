class player():
    def __init__(self, name, address):
        self.playerName = name
        self.playerBalance = 100
        self.address = address
        self.hand = []
        self.score = 0
        self.updateFlag = True


    def update(self, balance = 'old', hand = 'old'):
        if (balance != 'old'):
            self.playerBalance = balance
        if (hand != 'old'):
            self.hand.append(hand)
            #Update score





