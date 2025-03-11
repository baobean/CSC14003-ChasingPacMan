import pygame

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
        self.speed = 3  
        self.grid_size = 16  # Adjust based on map tile size
        self.score = 0

    def animation_state(self):
        self.pacman_index = (self.pacman_index + 0.5) % 2  
        self.image = self.sprites[self.direction][int(self.pacman_index)]  

    def can_move(self, direction, walls):
        """Check if Pac-Man can move in the given direction."""
        test_sprite = pygame.sprite.Sprite()  # Create a temporary sprite
        test_sprite.rect = self.rect.copy()  # Copy Pac-Man's current position

        if direction == "left":
            test_sprite.rect.x -= self.speed
        elif direction == "right":
            test_sprite.rect.x += self.speed
        elif direction == "up":
            test_sprite.rect.y -= self.speed
        elif direction == "down":
            test_sprite.rect.y += self.speed

        # Check if test_sprite collides with any wall
        collision = pygame.sprite.spritecollideany(test_sprite, walls)
        
        print(f"Trying to move {direction}: {'Blocked' if collision else 'Clear'} at {test_sprite.rect.topleft}")
        
        return collision is None

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

    def update(self, walls, ghosts):
        self.handle_input()

        # If the intended direction is possible, switch to it
        if self.can_move(self.intended_direction, walls):
            self.direction = self.intended_direction  

        # Try to move in the current direction
        if self.can_move(self.direction, walls):
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
