import pygame
from search import bfs_algorithm, dfs_algorithm, ucs_algorithm, astar_algorithm

class Ghost(pygame.sprite.Sprite):
    def __init__(self, ghost_type, position):
        super().__init__()
        self.ghost_type = ghost_type  # Store ghost type (Blue, Pink, Orange, Red)
        self.frames = self.load_frames(ghost_type)  # Load animation frames
        self.algorithm = self.assign_algorithm(ghost_type)  # Assign pathfinding algorithm

        # Set initial state
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=position)
        self.direction = 'right'
        self.speed = 3  # Adjust speed if needed

    def load_frames(self, ghost_type):
        """Load ghost animation frames based on type"""
        colors = ["blue", "pink", "orange", "red"]
        if ghost_type not in ["Blue", "Pink", "Orange", "Red"]:
            ghost_type = "Red"  

        base_path = f'assets/ghost/{ghost_type.lower()}_'  # Example: 'assets/ghost/blue_'
        return [pygame.image.load(base_path + str(i) + ".png").convert_alpha() for i in range(1, 5)]

    def assign_algorithm(self, ghost_type):
        if ghost_type == "Blue":
            return dfs_algorithm  # Depth-First Search
        elif ghost_type == "Pink":
            return bfs_algorithm  # Breadth-First Search
        elif ghost_type == "Orange":
            return ucs_algorithm  # Uniform-Cost Search
        elif ghost_type == "Red":
            return astar_algorithm  # A* Search
        return None  # Default if no algorithm is assigned

    def animation_state(self):
        self.animation_index = (self.animation_index + 0.1) % len(self.frames)
        self.image = self.frames[int(self.animation_index)]

    def update(self, map_state, positions):
        if self.algorithm:
            next_pos = self.algorithm(map_state, positions)
            if next_pos != (-1, -1):  
                self.rect.x, self.rect.y = next_pos[0] * 40, next_pos[1] * 40

        self.animation_state()
