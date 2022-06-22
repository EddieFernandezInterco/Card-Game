import pygame
import sys
import random
import Colors

def damage(damager,damaged,game):
    damaged.health -= damager.damage
    if damaged.health <= 0:
        for i in range(len(game.cards)):
            if game.cards[i] == damaged:
                game.deleteCards.append(i)
                break

class Card:
    def __init__(self, name, mana, damage, health, side):
        self.x = 5
        self.y = 5
        self.name = name
        self.mana = mana
        self.damage = damage
        self.health = health
        self.image = pygame.image.load('jungle.jpg')
        self.rect = pygame.Rect(self.x,self.y,200,200)
        self.isSelected = 0
        self.lastClick = 0
        self.side = side
        self.place = 'hand'
        self.fieldPosition= 0
        self.attackUsed = 0

    def isClicked(self, game):
        if pygame.mouse.get_pressed()[0] and self.lastClick == 0 and self.rect.collidepoint(pygame.mouse.get_pos()) :
            if game.phase == 'play' and ((game.mana1 >= self.mana and self.side == 0) or (self.side == 1 and game.mana2 >= self.mana)) and game.turn == self.side :
                if game.isSelected == 0:
                    if self.isSelected == 0:
                        self.isSelected = 1
                        game.isSelected = 1
                elif game.isSelected == 1:
                    if self.isSelected == 1:
                        self.isSelected = 0
                        game.isSelected = 0
            elif game.phase == 'battle' and self.place == 'field':
                if game.isSelected == 1:
                    for i in range(len(game.cards)):
                        if game.cards[i].isSelected == 1 and game.cards[i].place == 'field' and game.cards[i] != self:
                            damage(game.cards[i], self, game)
                            game.isSelected = 0
                            game.cards[i].isSelected = 0
                            game.cards[i].attackUsed = 1
                            break
                elif game.isSelected == 0  and self.attackUsed == 0 and self.side == game.turn:
                    count = 0
                    for i in range(len(game.cards)):
                        if game.cards[i].side != self.side and game.cards[i].place == 'field':
                            count+=1
                    if count == 0:
                        self.attackUsed = 1
                        if self.side == 0:
                            game.health2 -= self.damage
                        elif self.side == 1:
                            game.health1 -= self.damage
                    else:
                        self.isSelected = 1
                        game.isSelected = 1


        self.lastClick = pygame.mouse.get_pressed()[0]


    def update(self, game):
        self.rect.x = self.x
        self.rect.y = self.y
        self.isClicked(game)

class EmptyZone:
    def __init__(self,x,y,side):
        self.image = pygame.image.load('emptyZone.png')
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,200,200)
        self.isFull = 0
        self.side = side

class PassTurnButton:
    def __init__(self,game):
        self.image = pygame.image.load('PassTurn.png')
        self.x = game.SCREEN_WIDTH - 200
        self.y = game.SCREEN_HEIGHT/2 - 25
        self.rect = pygame.Rect(self.x,self.y,50,50)
        self.lastClick = 0

    def isClicked(self, game):
        if pygame.mouse.get_pressed()[0] and self.lastClick == 0 and self.rect.collidepoint(pygame.mouse.get_pos()):
            for i in range(len(game.cards)):
                game.cards[i].isSelected = 0
                game.isSelected = 0
                game.cards[i].attackUsed = 0
            if game.phase == 'play':
                game.phase = 'battle'
            elif game.phase == 'battle':
                for j in range(len(game.emptyZones)):
                    game.emptyZones[j].isFull = 0
                    for i in range(len(game.cards)):
                        if game.cards[i].x == game.emptyZones[j].x and game.cards[i].y == game.emptyZones[j].y:
                            game.emptyZones[j].isFull = 1
                game.phase = 'play'
                if game.turn == 0:
                    game.turn = 1
                    game.totalMana2 += 1
                    game.mana2 = game.totalMana2
                else:
                    game.turn = 0
                    game.totalMana1 += 1
                    game.mana1 = game.totalMana1
        self.lastClick = pygame.mouse.get_pressed()[0]

    def update(self,game):
        self.isClicked(game)

def drawOutlineText(game,str,x,y,):
    game.screen.blit(game.myFont.render(str, 1, game.colors.BLACK),
                     (x + 1, y + 1))
    game.screen.blit(game.myFont.render(str, 1, game.colors.BLACK),
                     (x - 1, y + 1))
    game.screen.blit(game.myFont.render(str, 1, game.colors.BLACK),
                     (x + 1, y - 1))
    game.screen.blit(game.myFont.render(str, 1, game.colors.BLACK),
                     (x - 1, y - 1))
    game.screen.blit(game.myFont.render(str, 1, game.colors.WHITE),
                     (x, y))



class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH =1600
        self.SCREEN_HEIGHT = 900
        self.clock = pygame.time.Clock()
        self.fontSize = 25
        self.myFont = pygame.font.SysFont("freesansbold", self.fontSize)
        self.start()
        while True:
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.screen.fill(Colors.GREY)
            pygame.display.update()
            self.clock.tick(60)
            self.update()
            self.draw()

    def start(self):
        self.health1 = 20
        self.health2 = 20
        self.deleteCards = []
        self.phase = 'play'
        self.passTurnButton = PassTurnButton(self)
        self.turn = 0
        self.totalMana1 = 1
        self.totalMana2 = 0
        self.mana1 = 1
        self.mana2 = 0
        self.isSelected = 0
        self.deck1 = []
        self.deck2 = []
        for x in range(10):
            self.deck1.append(Card('TGuy1', 1, 1, 1, 0))
        for x in range(10):
            self.deck1.append(Card('TGuy2', 2, 2, 2,0))
        for x in range(10):
            self.deck1.append(Card('TGuy3', 3, 3, 3,0))
        for x in range(10):
            self.deck2.append(Card('TGuy1', 1, 1, 1,1))
        for x in range(10):
            self.deck2.append(Card('TGuy2', 2, 2, 2,1))
        for x in range(10):
            self.deck2.append(Card('TGuy3', 3, 3, 3,1))
        random.shuffle(self.deck1)
        random.shuffle(self.deck2)

        self.hand1 = []
        self.hand2 = []

        for i in range(5):
            self.deck1[-1].x = 5 + 205 * (i + 1)
            self.hand1.append(self.deck1[-1])
            self.deck1.pop(-1)

        for i in range(5):
            self.deck2[-1].x = 5 + 205 * (i + 1)
            self.deck2[-1].y = self.SCREEN_HEIGHT - 205
            self.hand2.append(self.deck2[-1])
            self.deck2.pop(-1)

        for x in range(len(self.deck1)):
            print(self.deck1[x].name)

        self.cards = []
        for x in range(len(self.hand1)):
            self.cards.append(self.hand1[x])
        for i in range(len(self.hand2)):
            self.cards.append(self.hand2[i])

        self.emptyZones = []
        for i in range(5):
            self.emptyZones.append(EmptyZone(5 + (i+1) * 205, 210,0))
        for i in range(5):
            self.emptyZones.append(EmptyZone(5 + (i+1) * 205, self.SCREEN_HEIGHT - 410,1))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    a = 1

        self.passTurnButton.update(self)
        for i in range(len(self.cards)):
            self.cards[i].update(self)

        for i in range(len(self.hand1)):
            self.hand1[i].x = 5 + 205 * (i + 1)

        for i in range(len(self.hand2)):
            self.hand2[i].x = 5 + 205 * (i + 1)
            self.hand2[i].y = self.SCREEN_HEIGHT - 205

        if self.isSelected == 1 and self.phase == 'play':
            for i in range(len(self.emptyZones)):

                if pygame.mouse.get_pressed()[0] and self.emptyZones[i].rect.collidepoint(pygame.mouse.get_pos()) and self.emptyZones[i].isFull == 0:
                    for j in range(len(self.cards)):
                        if self.cards[j].isSelected == 1 and self.emptyZones[i].side == self.cards[j].side and self.phase == 'play' and self.cards[j].place == 'hand':
                            self.cards[j].place = 'field'
                            self.cards[j].x = self.emptyZones[i].x
                            self.cards[j].y = self.emptyZones[i].y
                            self.cards[j].isSelected = 0
                            if self.cards[j].side == 0:
                                for k in range(len(self.hand1)):
                                    if self.hand1[k] == self.cards[j]:
                                        self.hand1.pop(k)
                                        break
                            else:
                                for k in range(len(self.hand2)):
                                    if self.hand2[k] == self.cards[j]:
                                        self.hand2.pop(k)
                                        break
                            self.isSelected = 0
                            self.emptyZones[i].isFull = 1
                            if self.cards[j].side == 0:
                                self.mana1 -= self.cards[j].mana
                            else:
                                self.mana2 -= self.cards[j].mana


        for i in reversed(range(len(self.deleteCards))):
            print(i)
            self.cards.pop(self.deleteCards[i])
            self.deleteCards.pop(i)

    def draw(self):
        for x in range(len(self.emptyZones)):
            self.screen.blit(self.emptyZones[x].image, (self.emptyZones[x].x, self.emptyZones[x].y))

        for x in range(len(self.cards)):
            self.screen.blit(self.cards[x].image, (self.cards[x].x, self.cards[x].y))
            temp = [str(self.cards[x].name), 'M: ' + str(self.cards[x].mana), 'D: ' + str(self.cards[x].damage),
                    'H: ' + str(self.cards[x].health)]
            for y in range(len(temp)):
                drawOutlineText(self, temp[y] ,self.cards[x].x + 5, self.cards[x].y + 5 + y * self.fontSize)

            if self.cards[x].isSelected:
                drawOutlineText(self,'X', self.cards[x].x + 100,self.cards[x].y +100)

        drawOutlineText(self, 'Mana: ' + str(self.mana1) + '/' + str(self.totalMana1), self.SCREEN_WIDTH - 200, 50)
        drawOutlineText(self, 'Health: ' + str(self.health1), self.SCREEN_WIDTH - 200, 50 + self.fontSize)
        drawOutlineText(self, 'Mana: ' + str(self.mana2) + '/' + str(self.totalMana2), self.SCREEN_WIDTH - 200, self.SCREEN_HEIGHT-50)
        drawOutlineText(self, 'Health: ' + str(self.health2), self.SCREEN_WIDTH - 200, self.SCREEN_HEIGHT-50 + self.fontSize)
        self.screen.blit(self.passTurnButton.image, (self.passTurnButton.x, self.passTurnButton.y))
        drawOutlineText(self, str(self.turn), self.passTurnButton.x, self.passTurnButton.y - self.fontSize)
        drawOutlineText(self, str(self.phase), self.passTurnButton.x, self.passTurnButton.y- self.fontSize * 2)


game = Game()
