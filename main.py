import pygame
import sys
import os
import Colors
from asyncio.windows_events import NULL
from Handlers.ImageHandler import ImageHandler
from GameObjects.PassTurnButton import PassTurnButton
from GameObjects.Player import Player
from Game import Game


def drawOutlineText(game,str,x,y):
    img = game.state['font'].render(str, 1, Colors.BLACK)
    game.screen.blit(img, (x + 1, y + 1))
    game.screen.blit(img, (x - 1, y + 1))
    game.screen.blit(img, (x + 1, y - 1))
    game.screen.blit(img, (x - 1, y - 1))
    game.screen.blit(game.state['font'].render(str, 1, Colors.WHITE), (x, y))

def start(game):
    game.states[game.currentState]['background'] = ImageHandler('Images/background.jpg', pygame.Vector2(0,0), game)
    game.states[game.currentState]['passTurnButton'] = PassTurnButton(game)
    game.states[game.currentState]['turn'] = 0
    game.states[game.currentState]['turnRectangle'] = pygame.Rect(150, 0, 1150, 450)
    game.states[game.currentState]['selectedCard'] = NULL
    game.states[game.currentState]['players'] = [Player(game,0), Player(game,1)]
    game.states[game.currentState]['arrowFlies'] = 0
    game.states['menu']['selectedCard'] = NULL
    # game.passTurnButton = PassTurnButton(game)
    # game.turn = 0
    # game.turnRectangle = pygame.Rect(150, 0, 1150, 450)
    # game.selectedCard = NULL
    # game.players = [Player(game,0), Player(game,1)]
    # game.arrowFlies = 0

def update(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # game.passTurnButton.onClick(game)
                game.states[game.currentState]['passTurnButton'].onClick(game)
            if event.key == pygame.K_q:
                if game.currentState == 'play': game.currentState = 'menu'
                else: game.currentState = 'play'
                game.state = game.states[game.currentState]


def draw(game):
    if game.states[game.currentState]['selectedCard'] != NULL:
        drawOutlineText(game,'X', game.states[game.currentState]['selectedCard'].position.x + 100, game.states[game.currentState]['selectedCard'].position.y +100)
    if game.currentState == 'play':
        pygame.draw.rect(game.screen, Colors.BLACK, game.states[game.currentState]['turnRectangle'], 3)

Game(start, update, draw)


