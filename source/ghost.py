import pygame
import search
import utils

class Ghost(pygame.sprite.Sprite):
    directions = ["right", "left", "up", "down"] 
    frames_cache = {}

    def __init__(self, ghost_type, position):
        super().__init__()
        self.ghost_type = ghost_type
        self.frames = self.load_frames(ghost_type)  
        self.algorithm = self.assign_algorithm(ghost_type)  
        self.animation_index = 0
        self.direction = "right"  
        self.image = self.frames["right"][0]  
        self.rect = self.image.get_rect(topleft=position)
        self.target_x = self.rect.x
        self.target_y = self.rect.y
        self.speed = 2  
        

    def load_frames(self, ghost_type):
        if ghost_type in Ghost.frames_cache:
            return Ghost.frames_cache[ghost_type] 
        
        frames = {dir: [] for dir in Ghost.directions} 
        for i, direction in enumerate(Ghost.directions, start=1):  
            for j in range(1, 3):  # Two images per direction
                image_path = f'assets/ghost/{ghost_type.lower()}_{i}.{j}.png'
                frame = pygame.image.load(image_path).convert_alpha()
                frames[direction].append(frame)

        Ghost.frames_cache[ghost_type] = frames  
        return frames  

    def assign_algorithm(self, ghost_type):
        if ghost_type == "Blue":
            return search.bfs_algorithm 
        elif ghost_type == "Pink":
            return search.ids_algorithm  
        elif ghost_type == "Orange":
            return search.ucs_algorithm  
        elif ghost_type == "Red":
            return search.astar_algorithm  
        return None  

    def determine_direction(self, next_pos):
        current_x, current_y = self.rect.x // utils.tile_size - utils.x_offset, self.rect.y // utils.tile_size - utils.y_offset

        if isinstance(next_pos, tuple) and len(next_pos) == 2:
            dx, dy = next_pos[0] - current_x, next_pos[1] - current_y
            if dx > 0:
                return "right"
            elif dx < 0:
                return "left"
            elif dy > 0:
                return "down"
            elif dy < 0:
                return "up"

        return self.direction 


    def animation_state(self):
        self.animation_index = (self.animation_index + 0.1) % len(self.frames[self.direction])
        self.image = self.frames[self.direction][int(self.animation_index)]

    def update(self, map_state, positions):
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
        if self.algorithm:
            next_pos, tmp_node, memory_usage = self.algorithm(map_state, positions)
            
            if isinstance(next_pos, tuple) and len(next_pos) == 2:  
                self.direction = self.determine_direction(next_pos)
                self.target_x = (next_pos[0] + utils.x_offset) * utils.tile_size
                self.target_y = (next_pos[1] + utils.y_offset) * utils.tile_size
    
        self.animation_state()  