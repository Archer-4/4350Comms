from support import *

myDeck = deck(status = 'full')
print(str(myDeck))
print('')
myDeck.shuffle()
print(str(myDeck))
myDeck.reset()
print(str(myDeck))
print(len(myDeck))

testPlayer = player('name', 'address')
testPlayer.hand.insertCard(myDeck.draw_card())
print(str(testPlayer.hand))
print(testPlayer.hand.getScore())
print(len(myDeck))
print(str(myDeck))