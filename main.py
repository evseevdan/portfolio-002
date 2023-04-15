# Last modified 19:XX 15/04/23 BST(Z+1)
# Daniil Yevseyev

from time import sleep
from random import shuffle

suitsKey = ["♥", "♦", "♣", "♠"]
valueKey = ["7", "8", "9", "10", "J", "Q", "K", "A"]

class Card:
    
    def __init__(self,v,s):
        """
        Expects two integers as inputs
        Creates a Card instance
        Returns nothing        
        """
        # Set up a Card object with a value and suit
        self.value = v
        self.suit = s
    
class Player:
    
    def __init__(self,nm,n,s):
        """
        Expects a string (nm) and two integers (n,s) as inputs
        Creates a Player instance
        Returns nothing
        """
        # Player objects are more complex
        self.name = nm # Player name
        self.num = n # Player number (playing order)
        self.human = s # If the player is human or not
        self.hand = [] # Hand, will be filled with 8 cards
        self.legal = [] # Legal cards, used to check legal play
        self.pts = 0 # Current points
        self.flag = 0 # Used in points-scoring
    
    def addCard(self,p):
        self.hand.append(p)
        """
        Expects a Player object as input
        Expects a Card object as input
        Adds Card object to hand attribute
        Returns nothing
        """
    
    def removeCard(self,p):
        self.hand.remove(p)
        """
        Expects a Player object as input
        Expects a Card object (that is contained within hand attribute) as input
        Removes Card object from hand attribute
        Returns nothing
        """
    
    def playAI(self,playGame):
        """
        Expects a Player object as input
        Expects a Game object as input
        Calls several functions then plays a Card to Game
        Returns nothing
        """
        # Players are required to follow suit
        currentSuit = 0
        # Resets legal cards
        self.legal = []
        self.legality(playGame)
        # 't' is the AI's best choice card
        t = self.chooseAI(currentSuit,playGame)
        # Removes played card from hand
        self.removeCard(t)
        # Shows the player which card was played
        print(self.name + ": " + valueKey[t.value] + suitsKey[t.suit])
        # Plays the card
        playGame.play(t)
        # Delay so the player can see what's happening
        sleep(0.5)
        
    def playHuman(self,playGame):
        """
        Expects a Player object as input
        Expects a Game object as input
        Calls several functions for one of them play a Card to Game
        Returns nothing
        """
        # Resets legal cards
        self.legal = []
        # 's' is the output state, used to tell the player
        # if they are opening/following
        s = self.legality(playGame)
        self.chooseHuman(s,playGame)
        # Again, delay so the game doesn't run at light speed
        sleep(0.5)
    
    def chooseHuman(self,s,playGame):
        """
        Expects a Player object as input
        Expects an integer (s) and a Game object (playGame) as inputs
        Prints to console, takes inputs, plays a Card to Game
        Returns nothing
        """
        print()
        if s == 0:
            print("You are opening:")
        elif s == 1:
            print("You are following, and must follow suit:")
        else:
            print("You are following, but cannot follow suit:")
        opStr = ""
        # opStr is the list of legal cards
        for x in self.hand:
            opStr = opStr + valueKey[x.value] + suitsKey[x.suit] + " "
        print("Your cards are: ")
        print(opStr)
        # while with try-except block for input
        while True:
            t = input("To select a card, type its position, 1 - " + str(len(self.hand)) + ": ")
            try:
                intt = int(t) - 1
                if intt >= len(self.hand) or intt < 0:
                    print("Invalid input, try again")
                else:
                    bestCard = self.hand[intt]
                    break
            except TypeError:
                print("Invalid input, try again")
        # Play the card, then remove it from hand
        playGame.play(bestCard)
        self.removeCard(bestCard)
        print()
        # Output what was played
        print("Player: " + valueKey[bestCard.value] + suitsKey[bestCard.suit])
    
    def legality(self,playGame):
        """
        Expects a Player object as input
        Expects a Game object as input
        Performs checks and changes to array of legal cards (legal attribute)
        Returns state value (opening/following, trumps/no-trumps)
        """
        # Resets legal cards
        self.legal = []
        # Checks if opening
        if len(playGame.table) == 0:
            # If so, all cards are legal
            for x in self.hand:
                self.legal.append(x)
            # Tell the text-function that you're opening
            return 0
        else:
            # Following, so check trumps (first card played)
            currentSuit = playGame.table[0].suit
            for x in self.hand:
                # Add matching suit to legal
                if x.suit == currentSuit:
                    self.legal.append(x)
            # Check that you actually had matching suits
            if len(self.legal) == 0:
                # If not, all remaining cards are legal
                for x in self.hand:
                    self.legal.append(x)
                # Tell the text-function that you're following
                # but can't match trumps
                return 2
            else:
                # Tell the text-function that you're following
                return 1
        
    def chooseAI(self,s,playGame):
        """
        Expects a Player object as input
        Expects an integer (s) and a Game object as integer
        Finds the best Card to play given circumstances
        Returns the best Card
        """
        currentHi = 0
        currentLo = 10 # 10 is higher than all values
        tableHi = 0
        foundHi = 0
        # finds highest value card
        for x in playGame.table:
            if x.value > tableHi:
                tableHi = x.value
        # Checks if cards in legal are matching trumps:
        # if one card in legal matches, they all must
        if self.legal[0].suit == s:
            for x in self.legal:
                if x.value > currentHi:
                    if x.value > tableHi:
                        # Iterates over all cards, gradually moving
                        # up the current highest value
                        currentHi = x.value
                        # Marks that a winning card has been found
                        foundHi = 1
                        t = x
        # No winning card found
        if foundHi == 0:
            for x in self.legal:
                # Find lowest valid card (throwing bad cards away)
                if x.value < currentLo:
                    currentLo = x.value
                    t = x
        return t
            
class Deck:
    
    def __init__(self):
        """
        Expects nothing
        Initialises a Deck object of Cards and shuffles the order of cards
        Returns nothing
        """
        # Sets up a list of cards in the Russian deck.
        # That is; 7-A (the deck itself contains 6s too)
        self.cards = []
        for i in range(8):
            for j in range(4):
                # Here, 'i' is the value and 'j' is the suit
                # j = 0 is Hearts, 1 is Diamonds, 2 is Clubs, 3 is Spades
                # Likewise, i = 0 is 7, then 1 is 8, etc.
                self.cards.append(Card(i,j))
        # Shuffle function from random module
        shuffle(self.cards)
        
    def deal(self,pArray):
        """
        Expects a Deck object
        Expects an array of Player objects
        Deals Card objects to Player objects
        Returns nothing
        """
        # Deals 8 rounds of cards (32 in total) to each of the
        # four players
        for i in range(8):
            for x in pArray:
                x.addCard(self.cards.pop())

class Game:
    
    def __init__(self):
        """
        Expects nothing
        Creates a Game instance with a table attribute (empty array)
        Returns nothing
        """
        # Creates an array (will later contain card objects)
        self.table = []
        
    def play(self,x):
        """
        Expects a Game object
        Expects a Card object
        Appends Card object to table attribute array
        Returns nothing
        """
        # Called by 'playAI' and 'playHuman'
        self.table.append(x)
    
    def findWinner(self,pArray):
        """
        Expects a Game object
        Expects an array of Player objects
        Finds the winning Player in a trick and awards them points
        Also changes playing order so the winning Player goes first next trick
        Returns nothing
        """
        currentHigh = 0 # Current highest card
        currentSuit = self.table[0].suit # Trumps
        change = 0 # The playing order value of the winner
        bestCard = Card(0,0) # Empty card value for initialisation
        for x in self.table:
            # Disregards thrown cards (not matching trumps)
            if x.suit != currentSuit:
                x.value = 0
        for x in self.table:
            # Finds highest card
            if x.value > currentHigh:
                currentHigh = x.value
                bestCard = x
        for x in pArray:
            # Checks which position the highest card was in
            if self.table.index(bestCard) == x.num:
                change = x.num # Playing order value of winner
                print(x.name + " won.") # Console output
                x.num = 0 # Sets to be first next round
                x.flag = 1 # Sets flag to say "my number has been changed"
                x.pts += 1 # Adds point for won trick
        for x in pArray:
            if x.flag == 0: # If number has not been changed
                x.num += - change # Necessary to keep order correct
                if x.num < 0: # Possible to cycle around, say from 
                              # Fourth to first
                    x.num += 4
            else:
                x.flag = 0 # Resets flag
        self.table = [] # Empties table
                  
    def startRound(self,pArray):
        """
        Expects a Game object
        Expects an array of Player objects
        Calls various functions to play a game of King (8 rounds)
        Returns nothing
        """
        liveDeck = Deck() # Initialises a deck object
        liveDeck.deal(pArray) # Deals out said deck object
        print()
        print("Try and win tricks!")
        for i in range(8): # Eight tricks in a round
            print()
            print(" --- Trick " + str(i+1) + " ---")
            for j in range(4):
                for k in pArray: # Loops over all players
                    if k.num == j: # Checks players in order
                        if k.human == 0: # If not human
                            k.playAI(self) # Play as AI
                        else:
                            k.playHuman(self) # Otherwise
            self.findWinner(pArray)
        print()
        print("End of game:")
        for x in pArray: # All four players
            print(x.name + " has " + str(x.pts) + " points.")
        print()

def __main__():
    """
    Expects nothing
    Main game section, including creating Player objects and the array of them
    Returns nothing
    """
    pP = Player("Player",0,1) # The '1' indicates this is a human
    pA = Player("Alice",1,0) # Second in playing order by default
    pB = Player("Bob",2,0) # Third in playing order by default
    pC = Player("Charlie",3,0) # Fourth in playing order by default
    players = [pP, pA, pB, pC] # Array of players
    liveGame = Game() # Initialises game object
    liveGame.startRound(players) # Starts a round in that game object 
    
def __help__():
    """
    Expects nothing
    Help section, prints explanation of game to console
    Returns noth"ing""
    """
    print("King is a Russian card game played in many areas of the former USSR.")
    print("It uses a standard Russian deck, without the sixes. This means that ")
    print("it uses the cards 7 to Ace. The game is played in eight rounds, when")
    print("each player plays one card into the middle, in clockwise order, and ")
    print("the winner is the one with the highest legal card. The first card on")
    print("the table is the trump suit, and other players must follow suit. The")
    print("players each start with eight cards, and the one who wins the most  ")
    print("tricks by the end of the eight rounds is declared the winner.")

def __menu__():
    """
    Expects nothing
    Takes input from player and calls either help function or play function
    Exits after play function has finished
    Returns nothing
    """
    # while loop so that incorrect inputs don't require a restart of the program
    while True:
        inStr = input("Input either \'help\' or \'play\': ")
        if inStr == "help" or inStr == "Help":
            __help__()
        if inStr == "play" or inStr == "Play":
            __main__()
            input("Press enter to exit: ") # So that you have time to see
                                           # the final scores
            break
        else:
            print("Invalid input, try again")
            
__menu__()