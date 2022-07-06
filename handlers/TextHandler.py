import Colors
from Colors import *

from GameObject import GameObject

class TextHandler(GameObject):
    def __init__(self, game, str, isOutline, basePosition, positionOffset) -> None:
        super().__init__(game)
        self.str = str
        self.isOutline = isOutline
        self.game = game
        self.basePosition = basePosition
        self.positionOffset = positionOffset
        self.color = WHITE
        self.img = self.game.font.render(self.str, True, Colors.BLACK)
    
    def update(self):
        self.position = self.basePosition + self.positionOffset
        self.draw()

    def draw(self):
        if(self.isOutline):
            self.drawOutlineText(self.game, self.str, self.position)
        else:
            self.game.screen.blit(self.game.font.render(self.str, True, self.color), (self.position))

    def drawOutlineText(self, game, str, position):
        x = position.x
        y = position.y
        img = game.font.render(str, 1, BLACK)
        game.screen.blit(img, (x + 1, y + 1))
        game.screen.blit(img, (x - 1, y + 1))
        game.screen.blit(img, (x + 1, y - 1))
        game.screen.blit(img, (x - 1, y - 1))
        game.screen.blit(game.font.render(str, 1, self.color), (x, y))

    def getRect(self):
        rect = self.img.get_rect()
        rect.x = self.position.x
        rect.y = self.position.y
        return rect