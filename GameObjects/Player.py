import csv
import pygame
from GameObjects.Card import Card
from Game import Game
from GameObjects.Zone import Zone
from GameObjects.GameObject import GameObject
from Handlers.TextHandler import TextHandler
from GameObjects.FlyingNum import FlyingNum
import random
import Colors

class Player(GameObject):
    def __init__(self, game, num) -> None:
        super().__init__(game)

        self.impaledArrows = []
        self.stats = {
            'Armor': 0,
            'Health': 20
        }
        self.armor = 0
        self.totalMana = int(num == 0)
        self.mana = int(num == 0)
        self.deck = []
        self.hand = []
        self.field = []
        self.zones = []
        self.num = num
        self.game = game
        UIBaseManaX = game.SCREEN_WIDTH - 250
        UIBaseManaY = [50, game.SCREEN_HEIGHT-100]
        self.healthText = TextHandler(game, 'Health: ' + str(self.stats['Health']), pygame.Vector2(0,0), pygame.Vector2(UIBaseManaX, UIBaseManaY[self.num]), game.states[game.currentState]['bigFont'] )
        self.manaText = TextHandler(game, 'Mana: ' + str(self.mana) + '/' + str(self.totalMana),pygame.Vector2(0,0), pygame.Vector2(UIBaseManaX, UIBaseManaY[self.num] + game.states[game.currentState]['bigFont'].size('1')[1]), game.states[game.currentState]['bigFont'] )
        
        self.handY = [5, self.game.SCREEN_HEIGHT - 205]
        fieldPositionY = [210, game.SCREEN_HEIGHT - 410]

        for y in range(5):
            self.zones.append(Zone(pygame.Vector2(cardPositionX(y), fieldPositionY[num]), num, game))

        def addCard(cardName):
            self.deck.append(Card(self.game, self.num, cardName))

        # for x in range(2):
        #     addCard('Jungle Delver')
        #     addCard('Bird')
        #     addCard('Turtle')
        #     addCard('Armadilo')
        #     addCard('Bats')
        #     addCard('Shark')

        with open('deck' + str(self.num), 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                quantity = row[0]
                cardName = row[1]
                for x in range(int(quantity)):
                    addCard(cardName)

            
        random.shuffle(self.deck)

        for x in range(4):
            self.drawCard()
        
    
    def drawCard(self):
        handPositionY = [5, self.game.SCREEN_HEIGHT - 205]
        self.hand.append(self.deck[-1])
        self.deck.pop(-1)
        self.hand[-1].position.x = cardPositionX(len(self.hand)-1)
        self.hand[-1].position.y = handPositionY[self.num]
        
    def update(self):
        self.manaText.str = 'Mana: ' + str(self.mana) + '/' + str(self.totalMana)
        for index, card in enumerate(self.hand):
            card.position.x = cardPositionX(index)
            card.position.y = self.handY[self.num]

    def delete(self):
        for player in self.game.players:
            if player.stats['Health'] <= 0:
                print('Player ' + str(player.num + 1) + ' wins')
                self.game = Game(self.game.start,self.game.update,self.game.draw)
    
    def setStat(self, statName, newStat):
        statChange = newStat - self.stats[statName]
        if statChange != 0:
            color = ''
            if statChange < 0: color = Colors.RED
            elif statChange > 0: color = Colors.GREEN
            
            damageNumberSpawnPosition = pygame.Vector2(self.healthText.position.x, self.healthText.position.y - 100)
            FlyingNum(self.game, str(statChange ) + ' ' + statName, damageNumberSpawnPosition, color)
            self.stats[statName] = newStat
            self.healthText.str = statName + ' ' + str(self.stats[statName])

    def setMana(self, value):
        statChange = value - self.mana
        self.mana = value
        self.manaText.str = 'Mana: ' + str(self.mana) + '/' + str(self.totalMana)

def cardPositionX(i):
    return 5 + 210 * (i + 1)