import pygame
import csv
from pacman import Pacman
from ghost import Ghost

class Game:
    def __init__(self, map_file="map.csv"):
        pygame.init()
        self.tile_size = 40
        self.screen_width = 10 * self.tile_size
        self.screen_height = 10 * self.tile_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pac-Man AI")

        self.clock = pygame.time.Clock()

        # Load map and entities
        self.map_state = self.load_map(map_file)
        self.pacman = pygame.sprite.GroupSingle(self.create_pacman())  # Use GroupSingle for Pac-Man
        self.ghosts = pygame.sprite.Group(*self.create_ghosts())  # Use Group for multiple ghosts

    def load_map(self, file_path):
        """Load map from CSV"""
        map_data = []
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                map_data.append([int(cell) for cell in row])
        return map_data

    def create_pacman(self):
        """Find Pac-Man's position from the map and create Pac-Man"""
        for y, row in enumerate(self.map_state):
            for x, cell in enumerate(row):
                if cell == 6:
                    return Pacman((x * self.tile_size, y * self.tile_size))
        return Pacman((1 * self.tile_size, 1 * self.tile_size))  # Default position if not found

    def create_ghosts(self):
        """Find ghosts' positions from the map and create them"""
        ghost_types = {2: "Blue", 3: "Pink", 4: "Orange", 5: "Red"}
        ghosts = []
        for y, row in enumerate(self.map_state):
            for x, cell in enumerate(row):
                if cell in ghost_types:
                    ghosts.append(Ghost(ghost_types[cell], (x * self.tile_size, y * self.tile_size)))
        return ghosts

    def draw_map(self):
        """Draw the game map"""
        wall_color = (50, 50, 200)
        for y in range(len(self.map_state)):
            for x in range(len(self.map_state[y])):
                if self.map_state[y][x] == 1:
                    pygame.draw.rect(
                        self.screen, wall_color,
                        (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    )

    def run(self):
        """Main game loop"""
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.draw_map()

            # Get all positions for pathfinding
            pacman_pos = (self.pacman.sprite.rect.x // self.tile_size, self.pacman.sprite.rect.y // self.tile_size)
            # Get all ghost positions
            all_ghosts_positions = [(ghost.rect.x // self.tile_size, ghost.rect.y // self.tile_size) for ghost in self.ghosts]

            # Update each ghost
            for i, ghost in enumerate(self.ghosts):
                ghost_pos = (ghost.rect.x // self.tile_size, ghost.rect.y // self.tile_size)

                # Copy list and remove only the current ghost at index i
                other_ghosts_positions = all_ghosts_positions[:i] + all_ghosts_positions[i+1:]

                positions = {
                    "pacman": pacman_pos,
                    "ghosts": other_ghosts_positions,  # Other ghosts except the one moving
                    "ghost": ghost_pos  # The specific ghost moving
                }

                ghost.update(self.map_state, positions)

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.pacman.update()

            # Draw sprites
            self.pacman.draw(self.screen)  # Draw Pac-Man
            self.ghosts.draw(self.screen)  # Draw all ghosts

            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()
