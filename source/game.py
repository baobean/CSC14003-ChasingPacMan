import pygame
import csv
from pacman import Pacman
from ghost import Ghost
import wall
from food import Food
from text_renderer import TextRenderer
import numpy as np
import utils
import sys

class Game:
    def __init__(self, map_file="map.csv"):
        pygame.init()
        self.level = 1
        self.ending = False
        self.current_scene = "intro"
        self.tile_size = utils.tile_size
        self.screen_width = (utils.map_width + utils.x_offset) * self.tile_size
        self.screen_height = (utils.map_height + utils.y_offset) * self.tile_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pac-Man AI")

        self.clock = pygame.time.Clock()

        self.text_renderer = TextRenderer()
        wall.wall_images = wall.initialize_walls()
        self.food = pygame.sprite.Group()  # Initialize food group
        # Load map and get Pac-Man & Ghosts' positions
        self.map_state, pacman_pos, ghost_positions = self.load_map(map_file)

        # Create Pac-Man and Ghosts with correct positions
        self.pacman = pygame.sprite.GroupSingle(self.create_pacman())
        self.ghosts = pygame.sprite.Group(*self.create_ghosts()) 
        

        # Assign correct map weights using detected positions
        self.map_state = self.assign_weights(self.map_state, pacman_pos, ghost_positions)

        print(f"Map loaded:\n{self.map_state}")

    def load_map(self, file_path):
        """Load the game map from a CSV file and extract Pac-Man & Ghost positions."""
        map_data = []
        pacman_pos = None
        ghost_positions = []

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for y, row in enumerate(reader):
                int_row = [int(cell) for cell in row]  # Convert row to integer list
                map_data.append(int_row)

        self.walls = pygame.sprite.Group()  # Initialize walls group


        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                if tile == 1:  # Wall
                    new_wall = wall.Wall(None, ((x + utils.x_offset) * self.tile_size, y * self.tile_size), (self.tile_size, self.tile_size))
                    self.walls.add(new_wall)
                elif tile in wall.wall_types: # walls
                    new_wall = wall.Wall(wall.wall_types[tile], ((x + utils.x_offset) * self.tile_size, (y + utils.y_offset) * self.tile_size), (self.tile_size, self.tile_size))
                    self.walls.add(new_wall)
                elif tile == 6:  # Pac-Man
                    pacman_pos = (x + utils.x_offset, y + utils.y_offset)  # Store grid position
                    print(f"Pac-Man found at: {pacman_pos}")
                elif tile in {2, 3, 4, 5}:  # Ghosts (different colors)
                    ghost_positions.append((x + utils.x_offset, y + utils.y_offset))
                    self.food.add(Food("pellet", ((x + utils.x_offset) * self.tile_size, (y + utils.y_offset) * self.tile_size), self.tile_size))
                elif tile == 0:
                    self.food.add(Food("pellet", ((x + utils.x_offset) * self.tile_size, (y + utils.y_offset) * self.tile_size), self.tile_size))

        return np.array(map_data), pacman_pos, ghost_positions

    def assign_weights(self, map_data, pacman_pos, ghost_positions):
        """Assign pathfinding weights to the map."""
        rows, cols = map_data.shape
        weight_map = np.zeros((rows, cols))  # Create a NumPy array for weights

        for i in range(rows):
            for j in range(cols):
                cell = map_data[i][j]

                # ✅ Ensure correct placement of Pac-Man & Ghosts
                if (i, j) == pacman_pos:
                    weight_map[i][j] = 0  # Pac-Man's target position
                elif (i, j) in ghost_positions:
                    weight_map[i][j] = 0  # Ghost starting positions

                elif cell in wall.wall_types:  # Walls
                    weight_map[i][j] = float('inf')
                elif cell == 0:  # Walkable paths
                    weight = 1  # Default cost

                    # Reduce cost for straight paths to encourage open movement
                    if (0 < i < rows - 1 and map_data[i - 1][j] == 0 and map_data[i + 1][j] == 0) or \
                       (0 < j < cols - 1 and map_data[i][j - 1] == 0 and map_data[i][j + 1] == 0):
                        weight = 0.5  # Straight paths are more attractive

                    # Slightly increase cost near walls (to prevent hugging)
                    adjacent_walls = sum([
                        1 if i > 0 and map_data[i - 1][j] == 1 else 0,
                        1 if i < rows - 1 and map_data[i + 1][j] == 1 else 0,
                        1 if j > 0 and map_data[i][j - 1] == 1 else 0,
                        1 if j < cols - 1 and map_data[i][j + 1] == 1 else 0
                    ])

                    if adjacent_walls >= 2:
                        weight = 1.0  # Small penalty for hugging corners

                    weight_map[i][j] = weight
                elif cell == 5:  # Power Pellet
                    weight_map[i][j] = 10  # Ghosts should avoid Power Pellets
                else:
                    weight_map[i][j] = 1  # Default cost

        return weight_map

    def create_pacman(self):
        pacman_position = None

        # Locate Pac-Man position from the map
        for y, row in enumerate(self.map_state):
            for x, tile in enumerate(row):
                if tile == 6:
                    x += utils.x_offset
                    y += utils.y_offset

                    pacman_position = (x * self.tile_size, y * self.tile_size)
                    print(f"Pac-Man found at: {pacman_position}")  # Debugging output
                    break

        return Pacman(pacman_position if pacman_position else (1 * self.tile_size, 1 * self.tile_size))

    def create_ghosts(self):
        """Find ghosts' positions from the map and create them"""
        ghost_types = {2: "Blue", 3: "Pink", 4: "Orange", 5: "Red"}
        ghosts = []
        for y, row in enumerate(self.map_state):
            for x, cell in enumerate(row):
                if cell in ghost_types:
                    x += utils.x_offset
                    y += utils.y_offset
                    ghosts.append(Ghost(ghost_types[cell], (x * self.tile_size, y * self.tile_size)))
                    print(f"Ghost found at: {(x - utils.x_offset) * self.tile_size, (y - utils.y_offset) * self.tile_size}") 
        return ghosts

    def check_collisions(self):
        """Check if Pacman collides with any food"""
        eaten_food = pygame.sprite.spritecollide(self.pacman.sprite, self.food, True)
        if eaten_food:
            self.pacman.sprite.score += 100
        pacman_touched = pygame.sprite.spritecollide(self.pacman.sprite, self.ghosts, False)
        if pacman_touched:
            self.current_scene = "ending"
            current_screen = self.capture_screen()
            self.pacman.sprite.score = 0
            self.ending_scene(current_screen)

    
    def game_scene(self):
        self.screen.fill((0, 0, 0))
        self.walls.draw(self.screen)
        self.food.draw(self.screen)
        current_score = self.pacman.sprite.score
        self.text_renderer.render_text(self.screen, f"SCORE - {current_score}", 10, 10)

        # Draw sprites
        self.pacman.draw(self.screen)  # Draw Pac-Man
        self.ghosts.draw(self.screen)  # Draw all ghosts

        # Get all positions for pathfinding
        pacman_pos = (self.pacman.sprite.rect.x // self.tile_size - utils.x_offset, self.pacman.sprite.rect.y // self.tile_size - utils.y_offset)
        # Get all ghost positions
        all_ghosts_positions = [(ghost.rect.x // self.tile_size - utils.x_offset, ghost.rect.y // self.tile_size - utils.y_offset) for ghost in self.ghosts]

        # Update each ghost
        for i, ghost in enumerate(self.ghosts):
            ghost_pos = (ghost.rect.x // self.tile_size - utils.x_offset, ghost.rect.y // self.tile_size - utils.y_offset)
            # print(f"Ghost at {ghost_pos}, Tile Value: {self.map_state[ghost_pos[1]][ghost_pos[0]]}")

            # Copy list and remove only the current ghost at index i
            other_ghosts_positions = all_ghosts_positions[:i] + all_ghosts_positions[i+1:]

            positions = {
                "pacman": pacman_pos,
                "ghosts": other_ghosts_positions,  # Other ghosts except the one moving
                "ghost": ghost_pos  # The specific ghost moving
            }

            ghost.update(self.walls, self.map_state, positions)
            all_ghosts_positions[i] = (ghost.rect.x // self.tile_size - utils.x_offset, ghost.rect.y // self.tile_size - utils.y_offset)

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.pacman.update(self.walls, self.ghosts)
        self.check_collisions()            

        pygame.display.flip()
        self.clock.tick(7.5)

    def capture_screen(self):
        screen_copy = pygame.display.get_surface().copy()
        return screen_copy
    
    def ending_scene(self, current_screen):
        countdown = 3

        while countdown > 0:
            self.screen.fill((0, 0, 0))
            self.screen.blit(current_screen, (0, 0))
            self.text_renderer.render_text(self.screen, f"GO BACK TO LOBBY IN {countdown}", 100, 100, True)
            pygame.display.flip()
            pygame.time.delay(1000)
            countdown -= 1

        self.current_scene = "intro"

    def intro_scene(self):
        """Intro screen with level selection"""
        self.screen.fill((0, 0, 0))
        self.text_renderer.render_text(self.screen, "CHOOSE LEVEL", 100, 100, True)

        for i in range(1, 7):
            self.text_renderer.render_text(self.screen, f"LEVEL {i}", 200, 150 + i * 25, True)

        self.text_renderer.render_text(self.screen, ">", 100, 150 + self.level * 25)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.level = self.level + 1 if self.level < 6 else 1
                elif event.key == pygame.K_UP:
                    self.level = self.level - 1 if self.level > 1 else 6
                elif event.key == pygame.K_RETURN:
                    self.current_scene = "game"      
                    return     

    def run(self):
        """Main game loop"""
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.current_scene == 'intro':
                self.intro_scene()
            elif self.current_scene == 'game':
                self.game_scene()
