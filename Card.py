from asyncio.windows_events import NULL
import pygame
from FlyingNum import FlyingNum
from GameObject import GameObject
from Handlers.ImageHandler import ImageHandler
from Handlers.Clicker import Clicker
from Handlers.TextHandler import TextHandler
from GameObject import GameObject
from Arrow import Arrow
import Colors

class Card(GameObject):
    def __init__(self, name, mana, damage, health, playerNum, game, growthType) -> None:
        super().__init__(game)
        self.game = game
        self.position = pygame.Vector2(-200,0)
        self.name = name
        self.mana = mana
        self.damage = damage
        self.health = [health]
        self.playerNum = playerNum
        self.place = 'hand'
        self.fieldPosition = 0
        self.attackUsed = 0
        self.growthType = growthType
        self.growthStat = self.health
        self.imageHandler = ImageHandler('images/jungle.jpg', self.position, game)
        self.rect = self.imageHandler.image.get_rect()
        self.clicker = Clicker(self.rect, self.onClick, (game), game)
        self.statsStr = [str(self.name), 'M ' + str(self.mana), 'D ' + str(self.damage), 'H ' + str(self.health[0])]
        self.statsText = []
        self.emptyZone = 0
        for index, statStr in enumerate(self.statsStr):
            self.statsText.append(TextHandler(game, statStr, 1, self.position, pygame.Vector2(5,5 + game.font.size(statStr)[1] * index)))
                   
        g ={
            'health': 3,
            'damage': 2
        }
        growthIndex = 0
        if growthType == 'health':
            growthIndex = 3
        elif growthType == 'damage':
            growthIndex = 2
        
        if growthIndex != 0:
            self.statsText[growthIndex].color = Colors.LIGHTCYAN
        

    def onClick(self, game):
        if game.selectedCard == self:
            game.selectedCard = NULL
        elif game.selectedCard == NULL:
            if len(game.players[int(self.playerNum == 0)].field) == 0 and self.place == 'field' and self.attackUsed == 0:
                self.attackUsed = 1
                Arrow(game, self.imageHandler.getCenter(), game.players[int(self.playerNum == 0)].healthText.position, game.players[int(self.playerNum == 0)].healthText.getRect(), self, game.players[int(self.playerNum == 0)])
            elif game.turn == self.playerNum and ((self.place == 'hand' and game.players[self.playerNum].mana >= self.mana and game.turn == self.playerNum) or (self.place == 'field' and self.attackUsed == 0)):
                game.selectedCard = self
        elif self.place == 'field' and game.selectedCard.place == 'field':
            Arrow(game, game.selectedCard.imageHandler.getCenter(), self.imageHandler.getCenter(), self.imageHandler.getRect(), game.selectedCard, self)
            game.selectedCard.attackUsed = 1
            game.selectedCard = NULL

    def delete(self):
        for statsText in self.statsText:
            self.game.gameObjects.remove(statsText)
        
        self.emptyZone.isFull = 0
        self.game.gameObjects.remove(self.clicker)
        self.game.gameObjects.remove(self.imageHandler)
        self.game.players[self.playerNum].field.remove(self)
        self.game.gameObjects.remove(self)

    def update(self):
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        self.statsText[3].str = 'H ' + str(self.health[0])

    def dealDamage(self, target):
        target.health[0] -= self.damage
        if type(target) == type(self):
            FlyingNum(self.game, '-' + str(self.damage), pygame.Vector2(target.position.x, target.position.y), Colors.RED)
        if target.health[0] <= 0:
            target.delete()

            if self.growthType == 'health':
                self.growthStat[0] += 1
            elif self.growthType == 'damage':
                self.damage += 1
                self.statsText[2].str = 'D ' + str(self.damage)

            FlyingNum(self.game, '+ 1', pygame.Vector2(self.position.x, self.position.y), Colors.GREEN)