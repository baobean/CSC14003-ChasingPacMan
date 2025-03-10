import pygame
import math

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
        self.speed = 5
        self.grid_size = 16  # Adjust based on map tile size

        print(type(self.image))
        print(type(self.rect))

    def animation_state(self):
        self.pacman_index = (self.pacman_index + 0.5) % 2  
        self.image = self.sprites[self.direction][int(self.pacman_index)]  

    def can_move(self, direction, walls, map_state):
        collision = False
        """Check if Pac-Man can move in the given direction."""
        temp_sprite = self.rect.copy()
        temp_sprite.center = self.rect.center  # Copy Pac-Man's current position

        temp_sprite_x = round(temp_sprite.centerx // self.grid_size)
        temp_sprite_y = round(temp_sprite.centery // self.grid_size)

        next_x, next_y = temp_sprite_x, temp_sprite_y

        if direction == "left":
            next_x -= 1
        elif direction == "right":
            next_x += 1
        elif direction == "up":
            next_y -= 1
        elif direction == "down":
            next_y += 1

        if map_state[next_y][next_x] == float('inf'):
            collision = True
        
        print(f"Trying to move {direction}: {'Blocked' if collision else 'Clear'} at {next_x}, {next_y}")
        
        return not collision

    def handle_input(self):
        """Check user input and update intended direction."""
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

    def update(self, walls, ghosts, map_state):
        self.handle_input()

        # If the intended direction is possible, switch to it
        if self.can_move(self.intended_direction, walls, map_state):
            self.direction = self.intended_direction  

        # Try to move in the current direction
        if self.can_move(self.direction, walls, map_state):
            if self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "right":
                self.rect.x += self.speed
            elif self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "down":
                self.rect.y += self.speed
            self.animation_state()  
        else:
            print("Pac-Man is stuck but will continue moving in an open direction.")

        # Check for collision with ghosts
        if pygame.sprite.spritecollide(self, ghosts, False):
            print("Pac-Man collided with a ghost!")
