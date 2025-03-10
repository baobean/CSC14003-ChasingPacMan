import pygame
import utils

wall_types = {7: "top", 8: "right", 9: "bottom", 10: "left", 11: "top_left", 12: "top_right", 13: "bottom_right", 14: "bottom_left"}

def initialize_walls():
    # no, rotate the images to get other directions
    wall_images = {}

    initial_types = ["top", "top_left"]

    for type in initial_types:
        image_path = f'assets/walls/{type.lower()}.png'
        image = pygame.image.load(image_path).convert_alpha()
        wall_images[type] = pygame.transform.scale(image, (utils.tile_size, utils.tile_size))

    for i, type in enumerate(["right", "bottom", "left"]):
        wall_images[type] = pygame.transform.rotate(wall_images["top"], (i + 1) * (-90))

    for i, type in enumerate(["top_right", "bottom_right", "bottom_left"]):
        wall_images[type] = pygame.transform.rotate(wall_images["top_left"], (i + 1) * (-90))

    return wall_images

wall_images = {}

class Wall(pygame.sprite.Sprite):
    def __init__(self, wall_type, position, size):
        super().__init__()

        global wall_images

        self.wall_type = wall_type
        if (wall_type == None):
            self.image = pygame.Surface(size)
            self.image.fill((0, 0, 255))  # Blue walls
        else:
            self.image = wall_images[wall_type]
        
        self.rect = self.image.get_rect(topleft=position)