import math
from turtle import pos
import pygame
from GameObject import GameObject
from Handlers.ImageHandler import ImageHandler

class Arrow(GameObject):
    def __init__(self, game, position, destination) -> None:
        super().__init__(game)
        self.imageHandler = ImageHandler('Images/arrow.png',pygame.Vector2(), game)
        self.position = position - self.imageHandler.getCenter()
        self.imageHandler.position = self.position
        self.destination = destination - self.imageHandler.getCenter()
        self.direction = (destination - self.position).normalize()
        self.speed = 30
        self.imageHandler.setAngle(math.degrees(math.atan2(self.direction.x, self.direction.y)) + 180)
        
    def update(self):
        self.position += self.direction * self.speed
