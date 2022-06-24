import pygame

class Clicker():
    def __init__(self, rect, onClick, args) -> None:
        self.lastClick = 0
        self.rect = rect
        self.onClick = onClick
        self.args = args
    
    def update(self):
        if pygame.mouse.get_pressed()[0] and self.lastClick == 0 and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.onClick(self.args)
        self.lastClick = pygame.mouse.get_pressed()[0]
