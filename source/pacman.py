import pygame

class Pacman(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.pacman_open = pygame.image.load('assets/pacman_open.png').convert_alpha()
        self.pacman_closed = pygame.image.load('assets/pacman_closed.png').convert_alpha()

        self.sprites = {
            "right": [self.pacman_open, self.pacman_closed],
            "left": [pygame.transform.flip(self.pacman_open, True, False), 
                     pygame.transform.flip(self.pacman_closed, True, False)],
            "up": [pygame.transform.rotate(self.pacman_open, 90), 
                   pygame.transform.rotate(self.pacman_closed, 90)],
            "down": [pygame.transform.rotate(self.pacman_open, -90), 
                     pygame.transform.rotate(self.pacman_closed, -90)]
        }

        self.direction = "right"  # Default direction
        self.pacman_index = 0
        self.image = self.sprites[self.direction][self.pacman_index]
        self.rect = self.image.get_rect(midbottom=position)
        self.speed = 5

    def animation_state(self):
        self.pacman_index = (self.pacman_index + 0.1) % 2  # Only 2 animation frames (open & closed)
        self.image = self.sprites[self.direction][int(self.pacman_index)]  # Update sprite

    def update(self):
        keys = pygame.key.get_pressed()
        moved = False 

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = "left"
            moved = True
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = "right"
            moved = True
        elif keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.direction = "up"
            moved = True
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.direction = "down"
            moved = True

        if moved:
            self.animation_state()  