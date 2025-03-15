import pygame
#from search import bfs_algorithm, ids_algorithm, ucs_algorithm, astar_algorithm
import search
import utils

class Ghost(pygame.sprite.Sprite):
    def __init__(self, ghost_type, position):
        super().__init__()
        self.ghost_type = ghost_type
        self.frames = self.load_frames(ghost_type)  # Load animation frames for all directions
        self.algorithm = self.assign_algorithm(ghost_type)  # Assign pathfinding algorithm

        # Initial State
        self.animation_index = 0
        self.direction = "right"  # Default direction
        self.image = self.frames["right"][0]  # Set initial frame
        self.rect = self.image.get_rect(topleft=position)
        self.target_x = self.rect.x
        self.target_y = self.rect.y
        self.speed = 2  # Adjust speed if needed
        

    def load_frames(self, ghost_type):
        """Load ghost animation frames for all directions"""
        directions = ["right", "left", "up", "down"]
        frames = {dir: [] for dir in directions}  # Dictionary to store frames by direction

        for i, direction in enumerate(directions, start=1):  
            for j in range(1, 3):  # Two images per direction
                image_path = f'assets/ghost/{ghost_type.lower()}_{i}.{j}.png'
                frame = pygame.image.load(image_path).convert_alpha()
                # frame = pygame.transform.scale2x(frame)
                frames[direction].append(frame)

        return frames  # Return dictionary of animations

    def assign_algorithm(self, ghost_type):
        """Assign the correct search algorithm to the ghost"""
        if ghost_type == "Blue":
            return search.bfs_algorithm  # Breadth-First Search
        elif ghost_type == "Pink":
            return search.ids_algorithm  # Depth-First Search 
        elif ghost_type == "Orange":
            return search.ucs_algorithm  # Uniform-Cost Search
        elif ghost_type == "Red":
            return search.astar_algorithm  # A* Search
        return None  # Default if no algorithm is assigned

    def determine_direction(self, next_pos):
        """Determines ghost movement direction based on next position."""
        current_x, current_y = self.rect.x // utils.tile_size - utils.x_offset, self.rect.y // utils.tile_size - utils.y_offset # Get grid-based position

        if isinstance(next_pos, tuple) and len(next_pos) == 2:  # Ensure next_pos is valid
            dx, dy = next_pos[0] - current_x, next_pos[1] - current_y

            if dx > 0:
                return "right"
            elif dx < 0:
                return "left"
            elif dy > 0:
                return "down"
            elif dy < 0:
                return "up"

        return self.direction  # Default to the current direction


    def animation_state(self):
        """Cycle through frames based on direction"""
        self.animation_index = (self.animation_index + 0.1) % len(self.frames[self.direction])
        self.image = self.frames[self.direction][int(self.animation_index)]

    def update(self, walls, map_state, positions):
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
            return  # Pr
        if self.algorithm:
            next_pos, tmp_node, memory_usage = self.algorithm(map_state, positions)


            
            if isinstance(next_pos, tuple) and len(next_pos) == 2:  # Ensure next_pos is a valid (x, y) tuple
                self.direction = self.determine_direction(next_pos)
                self.target_x = (next_pos[0] + utils.x_offset) * utils.tile_size
                self.target_y = (next_pos[1] + utils.y_offset) * utils.tile_size

            # if pygame.sprite.spritecollide(self, walls, False):  # Now using `self` instead of `test_rect`
            #     print("Collision detected! (Ghost)")
    
        self.animation_state()  