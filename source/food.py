import pygame
import utils

class Food(pygame.sprite.Sprite):
    food_images = {}

    def __init__(self, food_type, position, size):
        super().__init__()

        if food_type not in Food.food_images:
            Food.food_images[food_type] = pygame.image.load(f"assets/food/{food_type}.png").convert_alpha()

        self.food_type = food_type
        self.image = Food.food_images[food_type]
        self.rect = self.image.get_rect(topleft=position)