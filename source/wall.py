import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill((0, 0, 255))  # Blue walls
        self.rect = self.image.get_rect(topleft=position)
