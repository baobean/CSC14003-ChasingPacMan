import pygame

class Pacman(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        pacman_open_1 = pygame.image.load('assets/pacman/pacman_1.png').convert_alpha()
        pacman_open_1 = pygame.transform.scale2x(pacman_open_1)
        pacman_open_2 = pygame.image.load('assets/pacman/pacman_2.png').convert_alpha()
        pacman_open_2 = pygame.transform.scale2x(pacman_open_2)
        pacman_closed = pygame.image.load('assets/pacman/pacman_3.png').convert_alpha()
        pacman_closed = pygame.transform.scale2x(pacman_closed)
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
                     pygame.transform.rotate(pacman_open_2, -90),]
        }

        self.direction = "right"  # Default direction
        self.pacman_index = 0
        self.image = self.sprites[self.direction][int(self.pacman_index)]
        self.rect = self.image.get_rect(topleft=position)
        self.speed = 10
        

    def animation_state(self):
        self.pacman_index = (self.pacman_index + 0.5) % 2  # Only 2 animation frames (open & closed)
        self.image = self.sprites[self.direction][int(self.pacman_index)]  # Update sprite

    def update(self, walls, ghosts):
        keys = pygame.key.get_pressed()
        moved = False
        collide = False

        new_x, new_y = self.rect.x, self.rect.y

        if keys[pygame.K_LEFT]:
            new_x -= self.speed
            self.direction = "left"
            moved = True
        elif keys[pygame.K_RIGHT]:
            new_x += self.speed
            self.direction = "right"
            moved = True
        elif keys[pygame.K_UP]:
            new_y -= self.speed
            self.direction = "up"
            moved = True
        elif keys[pygame.K_DOWN]:
            new_y += self.speed
            self.direction = "down"
            moved = True
        
        old_x, old_y = self.rect.x, self.rect.y
        self.rect.topleft = (new_x, new_y)

        if pygame.sprite.spritecollide(self, walls,False):  # Now using `self` instead of `test_rect`
            print("Collision detected! Pac-Man cannot move.")
            self.rect.topleft = (old_x, old_y) 
            collide = True

        if moved and not collide:
             self.animation_state()

        # Check for collision with ghosts
        if pygame.sprite.spritecollide(self, ghosts, False):
            print("Pac-Man collided with a ghost!")
            self.rect.topleft = (old_x, old_y) 

        