import pygame
import utils

class Pacman(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        pacman_open_1 = pygame.image.load('assets/pacman/pacman_1.png').convert_alpha()
        pacman_open_2 = pygame.image.load('assets/pacman/pacman_2.png').convert_alpha()
        pacman_closed = pygame.image.load('assets/pacman/pacman_3.png').convert_alpha()

        self.pacman_open = [pacman_open_1, pacman_open_2]
        self.pacman_closed = pacman_closed
        self.sprites = {
            "right": [self.pacman_closed, self.pacman_open[0], self.pacman_open[1]],
            "left": [pygame.transform.flip(pacman_closed, True, False),
                     pygame.transform.flip(pacman_open_1, True, False), 
                     pygame.transform.flip(pacman_open_2, True, False)],
            "up": [pygame.transform.rotate(pacman_closed, 90),
                   pygame.transform.rotate(pacman_open_1, 90), 
                   pygame.transform.rotate(pacman_open_2, 90)],
            "down": [pygame.transform.rotate(pacman_closed, -90),
                     pygame.transform.rotate(pacman_open_1, -90), 
                     pygame.transform.rotate(pacman_open_2, -90)]
        }

        self.direction = "right"  
        self.intended_direction = "right"  
        self.pacman_index = 0
        self.image = self.sprites[self.direction][int(self.pacman_index)]
        self.rect = self.image.get_rect(topleft=position)
        self.target_x = self.rect.x
        self.target_y = self.rect.y
        self.speed = 2
        self.grid_size = 16  
        self.score = 0

    def animation_state(self):
        self.pacman_index = (self.pacman_index + 0.1) % 2
        self.image = self.sprites[self.direction][int(self.pacman_index)]  

    def can_move(self, direction, walls):
        test_sprite = pygame.sprite.Sprite()  
        test_sprite.rect = self.rect.copy()  

        if direction == "left":
            test_sprite.rect.x -= utils.tile_size
        elif direction == "right":
            test_sprite.rect.x += utils.tile_size
        elif direction == "up":
            test_sprite.rect.y -= utils.tile_size
        elif direction == "down":
            test_sprite.rect.y += utils.tile_size

        collision = pygame.sprite.spritecollideany(test_sprite, walls)
        
        return collision is None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.intended_direction = "left"
            print("Left key pressed")
        elif keys[pygame.K_RIGHT]:
            self.intended_direction = "right"
            print("Right key pressed")
        elif keys[pygame.K_UP]:
            self.intended_direction = "up"
            print("Up key pressed")
        elif keys[pygame.K_DOWN]:
            self.intended_direction = "down"
            print("Down key pressed")

    def update(self, walls):
        self.handle_input()  
        
        if self.intended_direction and self.intended_direction != self.direction:
            if self.can_move(self.intended_direction, walls):
                self.direction = self.intended_direction
                self.intended_direction = None 

                self.rect.x = (self.rect.x // utils.tile_size) * utils.tile_size
                self.rect.y = (self.rect.y // utils.tile_size) * utils.tile_size

                if self.direction == "left":
                    self.target_x = max(0, self.rect.x - utils.tile_size)
                elif self.direction == "right":
                    self.target_x = (self.rect.x + utils.tile_size) // utils.tile_size * utils.tile_size
                elif self.direction == "up":
                    self.target_y = max(0, self.rect.y - utils.tile_size)
                elif self.direction == "down":
                    self.target_y = (self.rect.y + utils.tile_size) // utils.tile_size * utils.tile_size

        if self.rect.x != self.target_x or self.rect.y != self.target_y:
            if self.rect.x < self.target_x:
                self.rect.x += min(self.speed, self.target_x - self.rect.x)
            elif self.rect.x > self.target_x:
                self.rect.x -= min(self.speed, self.rect.x - self.target_x)

            if self.rect.y < self.target_y:
                self.rect.y += min(self.speed, self.target_y - self.rect.y)
            elif self.rect.y > self.target_y:
                self.rect.y -= min(self.speed, self.rect.y - self.target_y)

            self.animation_state()

            return 

        self.handle_input()

        if self.can_move(self.direction, walls):
            if self.direction == "left":
                self.target_x = max(0, self.rect.x - utils.tile_size)
            elif self.direction == "right":
                self.target_x = (self.rect.x + utils.tile_size) // utils.tile_size * utils.tile_size
            elif self.direction == "up":
                self.target_y = max(0, self.rect.y - utils.tile_size)
            elif self.direction == "down":
                self.target_y = (self.rect.y + utils.tile_size) // utils.tile_size * utils.tile_size

        self.animation_state()
