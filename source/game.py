import pygame
import math
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
        pygame.mixer.init()    
        self.level = 1
        self.current_scene = "intro"
        self.tile_size = utils.tile_size

        self.screen_width = (utils.map_width + utils.x_offset) * self.tile_size
        self.screen_height = (utils.map_height + utils.y_offset) * self.tile_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pac-Man AI")

        self.clock = pygame.time.Clock()

        self.header_font = pygame.font.Font("assets/text/PAC-FONT.TTF", 48)
        self.text_font = pygame.font.Font("assets/text/Emulogic-zrEw.ttf", 13)

        self.bgm = pygame.mixer.Sound("assets/audio/game_start.wav")
        self.munch_sounds = [
            pygame.mixer.Sound("assets/audio/munch_1.wav"),
            pygame.mixer.Sound("assets/audio/munch_2.wav")
        ]
        self.munch_index = 0
        self.death_sound = pygame.mixer.Sound("assets/audio/pacman_death.wav")
        self.death_sound.set_volume(0.25) 

        self.text_renderer = TextRenderer()
        wall.wall_images = wall.initialize_walls()
        self.original_food = pygame.sprite.Group()  
        self.food = pygame.sprite.Group()  

        self.map_data, pacman_pos, ghost_positions = self.load_map(map_file)

        self.original_map_state = self.assign_weights(self.map_data, pacman_pos)
    
    def copy_sprites(self, original_group):
        new_group = pygame.sprite.Group()
        for sprite in original_group.sprites():
            new_sprite = sprite.copy()
            new_group.add(new_sprite)
        return new_group

    def load_map(self, file_path):
        map_data = []
        pacman_pos = None
        ghost_positions = []

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for y, row in enumerate(reader):
                int_row = [int(cell) for cell in row]  
                map_data.append(int_row)

        self.walls = pygame.sprite.Group()  

        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                if tile in wall.wall_types:
                    new_wall = wall.Wall(wall.wall_types[tile], ((x + utils.x_offset) * self.tile_size, (y + utils.y_offset) * self.tile_size), (self.tile_size, self.tile_size))
                    self.walls.add(new_wall)
                elif tile == 0:
                    self.original_food.add(Food("pellet", ((x + utils.x_offset) * self.tile_size, (y + utils.y_offset) * self.tile_size)))

        return np.array(map_data), pacman_pos, ghost_positions
    
    def generate_map_level(self, level):
        result_maps = [np.copy(self.original_map_state) for _ in range(5)]

        test_cases = [    
            {"pacman": (1, 1), "ghost": (7, 1)},
            {"pacman": (1, 1), "ghost": (10, 23)},
            {"pacman": (1, 1), "ghost": (26, 1)},
            {"pacman": (1, 1), "ghost": (1, 20)},
            {"pacman": (1, 1), "ghost": (3, 26)}
        ]

        test_cases_2 = [
            {"pacman": (1, 1), "blue_ghost": (26, 29), "pink_ghost": (3,26), "orange_ghost": (6,23), "red_ghost": (7,1)},
            {"pacman": (1, 1), "blue_ghost": (3, 26), "pink_ghost": (26, 4), "orange_ghost": (9,12), "red_ghost": (1,20)},
            {"pacman": (1, 1), "blue_ghost": (9, 8), "pink_ghost": (9, 1), "orange_ghost": (26,29), "red_ghost": (9,12)},
            {"pacman": (1, 1), "blue_ghost": (1, 20), "pink_ghost": (9, 8), "orange_ghost": (26,26), "red_ghost": (5,5)},
            {"pacman": (1, 1), "blue_ghost": (5, 5), "pink_ghost": (9, 12), "orange_ghost": (3,26), "red_ghost": (26,29)}
        ]

        if level <= 4:
            for i, positions in enumerate(test_cases, start=0):
                    pacman_pos = positions["pacman"]
                    ghost_pos = positions["ghost"]

                    result_maps[i][ghost_pos[1]][ghost_pos[0]] = level + 1
                    result_maps[i][pacman_pos[1]][pacman_pos[0]] = 6
        else:
            for i, positions in enumerate(test_cases_2, start=0):
                    pacman_pos = positions["pacman"]
                    blue_pos = positions["blue_ghost"]
                    pink_pos = positions["pink_ghost"]
                    orange_pos = positions["orange_ghost"]
                    red_pos = positions["red_ghost"]
                    
                    result_maps[i][blue_pos[1]][blue_pos[0]] = 2
                    result_maps[i][pink_pos[1]][pink_pos[0]] = 3
                    result_maps[i][orange_pos[1]][orange_pos[0]] = 4
                    result_maps[i][red_pos[1]][red_pos[0]] = 5
                    result_maps[i][pacman_pos[1]][pacman_pos[0]] = 6

        return np.array(result_maps)

    def assign_weights(self, map_data, pacman_pos):
        rows, cols = map_data.shape
        weight_map = np.zeros((rows, cols))  
        print("hello")
        for i in range(rows):
            for j in range(cols):
                cell = map_data[i][j]

                if (i, j) == pacman_pos:
                    weight_map[i][j] = 0 
                elif cell in wall.wall_types:
                    weight_map[i][j] = float('inf')
                elif cell == 0: 
                    weight = 1  

                    if (0 < i < rows - 1 and map_data[i - 1][j] == 0 and map_data[i + 1][j] == 0) or \
                       (0 < j < cols - 1 and map_data[i][j - 1] == 0 and map_data[i][j + 1] == 0):
                        weight = 0.5  

                    adjacent_walls = sum([
                        1 if i > 0 and map_data[i - 1][j] == 1 else 0,
                        1 if i < rows - 1 and map_data[i + 1][j] == 1 else 0,
                        1 if j > 0 and map_data[i][j - 1] == 1 else 0,
                        1 if j < cols - 1 and map_data[i][j + 1] == 1 else 0
                    ])

                    if adjacent_walls >= 2:
                        weight = 1.0  

                    weight_map[i][j] = weight
                elif cell == 5:  
                    weight_map[i][j] = 10 
                else:
                    weight_map[i][j] = 1  

        return weight_map

    def create_pacman(self):
        pacman_position = None

        for y, row in enumerate(self.map_state):
            for x, tile in enumerate(row):
                if tile == 6:
                    x += utils.x_offset
                    y += utils.y_offset

                    pacman_position = (x * self.tile_size, y * self.tile_size)
                    print(f"Pac-Man found at: {pacman_position}")  
                    break

        return Pacman(pacman_position if pacman_position else (1 * self.tile_size, 1 * self.tile_size))

    def create_ghosts(self):
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
        eaten_food = pygame.sprite.spritecollide(self.pacman.sprite, self.food, True)
        if eaten_food:
            self.munch_sounds[self.munch_index].play()
            self.munch_index = (self.munch_index + 1) % 2
            self.pacman.sprite.score += 100
        pacman_touched = pygame.sprite.spritecollide(self.pacman.sprite, self.ghosts, False)
        
        if pacman_touched:
            self.death_sound.play()
            self.current_scene = "ending" 
            current_screen = self.capture_screen()
            self.pacman.sprite.score = 0
            self.map_state_list = self.map_state_list[1:]
            self.pacman = None
            self.ghosts = None
            self.food = None

            self.ending_scene(current_screen)

    def game_scene(self):
        self.screen.fill((0, 0, 0))
        self.walls.draw(self.screen) 
        self.food.draw(self.screen)
        current_score = self.pacman.sprite.score
        self.text_renderer.render_text(self.screen, f"SCORE - {current_score}", 10, 10)

        self.pacman.draw(self.screen)  
        self.ghosts.draw(self.screen) 

        pacman_pos = (self.pacman.sprite.rect.x // self.tile_size - utils.x_offset, self.pacman.sprite.rect.y // self.tile_size - utils.y_offset)
        all_ghosts_positions = [(ghost.rect.x // self.tile_size - utils.x_offset, ghost.rect.y // self.tile_size - utils.y_offset) for ghost in self.ghosts]

        self.check_collisions()
        if len(self.map_state_list) == 0:
            return
        
        if self.level == 6:
            self.pacman.update(self.walls)
            self.check_collisions()
            if len(self.map_state_list) == 0:
                return
            
        for i, ghost in enumerate(self.ghosts):
            ghost_pos = (ghost.rect.x // self.tile_size - utils.x_offset, ghost.rect.y // self.tile_size - utils.y_offset)
            other_ghosts_positions = all_ghosts_positions[:i] + all_ghosts_positions[i+1:]

            positions = {
                "pacman": pacman_pos,
                "ghosts": other_ghosts_positions,  
                "ghost": ghost_pos  
            }

            ghost.update(self.map_state, positions)
            all_ghosts_positions[i] = (ghost.rect.x // self.tile_size - utils.x_offset, ghost.rect.y // self.tile_size - utils.y_offset)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()        

        pygame.display.flip()
        self.clock.tick(45)

    def capture_screen(self):
        screen_copy = pygame.display.get_surface().copy()
        return screen_copy
    
    def ending_scene(self, current_screen):
        countdown = 3
        while countdown > 0:
            self.screen.fill((0, 0, 0))
            self.screen.blit(current_screen, (0, 0))
            if len(self.map_state_list) == 0:
                self.text_renderer.render_text(self.screen, f"GO BACK TO LOBBY IN {countdown}", 100, 100, True)
            else:
                self.text_renderer.render_text(self.screen, f"MOVE TO NEW TEST CASE IN {countdown}", 100, 100, True)
            pygame.display.flip()
            pygame.time.delay(1000)
            countdown -= 1

        if len(self.map_state_list) == 0:
            self.current_scene = "intro"
        else:
            self.map_state = self.map_state_list[0]
            self.pacman = pygame.sprite.GroupSingle(self.create_pacman())
            self.ghosts = pygame.sprite.Group(*self.create_ghosts())
            
            self.food = self.copy_sprites(self.original_food)
            self.current_scene = "game"
    
    def ghost_animation(self, base_y):
        if not hasattr(self, "ghost_images"):
            self.ghost_images = [
                [pygame.image.load("assets/ghost/blue_3.1.png"), pygame.image.load("assets/ghost/blue_4.1.png")],  
                [pygame.image.load("assets/ghost/pink_3.1.png"), pygame.image.load("assets/ghost/pink_4.1.png")],  
                [pygame.image.load("assets/ghost/orange_3.1.png"), pygame.image.load("assets/ghost/orange_4.1.png")],  
                [pygame.image.load("assets/ghost/red_3.1.png"), pygame.image.load("assets/ghost/red_4.1.png")]  
            ]

            self.ghost_images = [
                [pygame.transform.scale(image, (self.tile_size * 1.75, self.tile_size * 1.75)) for image in ghost] 
                for ghost in self.ghost_images
            ]

        ghost_width = self.tile_size * 1.75
        spacing = 10
        total_width = (ghost_width * 4) + (spacing * 3)
        start_x = (self.screen_width - total_width) // 2

        max_y = base_y + 20 
        speed = 0.01  

        if not hasattr(self, "animated_ghosts"):
            self.animated_ghosts = [{"x": start_x + i * (ghost_width + spacing), "y": base_y, "direction": 1, "current_frame": 0} for i in range(4)]

        for ghost in self.animated_ghosts:
            ghost["y"] += ghost["direction"] * speed

            if ghost["y"] >= max_y or ghost["y"] <= base_y:
                ghost["direction"] *= -1  
                ghost["current_frame"] = 1 if ghost["direction"] > 0 else 0 

        for i, ghost in enumerate(self.animated_ghosts):
            frame = self.ghost_images[i][ghost["current_frame"]]
            self.screen.blit(frame, (ghost["x"], int(ghost["y"])))

    def loading_scene(self, text):
        if hasattr(self, "animated_ghosts"):
            delattr(self, "animated_ghosts")  
        running = True
        while running:
            self.screen.fill((0, 0, 0))

            self.ghost_animation(150)

            text_surface = self.text_font.render(text, True, 'white')
            text_x = (self.screen_width - text_surface.get_width()) // 2
            self.screen.blit(text_surface, (text_x, 250))

            pygame.display.flip() 

            if pygame.time.get_ticks() - self.start_loading_time > 2000:
                running = False

        self.current_scene = "game"
        self.map_state_list = self.generate_map_level(self.level)
        self.map_state = self.map_state_list[0]
        self.pacman = pygame.sprite.GroupSingle(self.create_pacman())
        self.ghosts = pygame.sprite.Group(*self.create_ghosts())
        self.food = self.copy_sprites(self.original_food)

    def intro_scene(self):
        running = True
        self.dropdown_active = False  
        selected_option = 0  
        self.level = 0  
        if hasattr(self, "animated_ghosts"):
            delattr(self, "animated_ghosts")  
        while running:
            self.screen.fill((0, 0, 0))
            self.ghost_animation(50)
            heading_text = self.header_font.render("PACMAN", True, 'yellow')
            heading_x = (self.screen_width - heading_text.get_width()) // 2
            self.screen.blit(heading_text, (heading_x, 120))
            text_surfaces = [
                self.text_font.render("Press UP/DOWN to navigate", True, 'white'),
                self.text_font.render("ENTER to select", True, 'white'),
            ]
            self.render_multi_line(text_surfaces, 200, False, False)
            if not self.dropdown_active:
                menu_surfaces = [
                    self.text_font.render("LEVEL", True, 'white'),
                    self.text_font.render("QUIT", True, 'white')
                ]
                text_positions = self.render_multi_line(menu_surfaces, 150, return_positions=True)

                indicator_surface = self.text_font.render(">", True, 'white')
                indicator_x = text_positions[0][0] - 30 
                indicator_y = text_positions[selected_option][1]  
                self.screen.blit(indicator_surface, (indicator_x, indicator_y))
            else:
                level_texts = [self.text_font.render(f"LEVEL {i}", True, 'white') for i in range(1, 7)]
                menu_surfaces = [
                    self.text_font.render("LEVEL", True, 'white')
                ] + level_texts + [
                    self.text_font.render("QUIT", True, 'white')
                ]
                text_positions = self.render_multi_line(menu_surfaces, 150, return_positions=True)

                indicator_surface = self.text_font.render(">", True, 'white')
                indicator_x = text_positions[0][0] - 30  
                indicator_y = text_positions[self.level][1]  
                self.screen.blit(indicator_surface, (indicator_x, indicator_y))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.dropdown_active:
                        if event.key == pygame.K_DOWN:
                            self.level = self.level + 1 if self.level < 6 else 0
                        elif event.key == pygame.K_UP:
                            self.level = self.level - 1 if self.level > 0 else 6
                        elif event.key == pygame.K_RETURN:
                            if self.level == 0:
                                self.dropdown_active = False
                                break
                            running = False
                    else:
                        if event.key == pygame.K_DOWN:
                            selected_option = (selected_option + 1) % 2  
                        elif event.key == pygame.K_UP:
                            selected_option = (selected_option - 1) % 2
                        elif event.key == pygame.K_RETURN:
                            if selected_option == 0:  
                                self.dropdown_active = True
                            elif selected_option == 1:  
                                pygame.quit()
                                sys.exit()
                                
        if self.level > 0:
            self.current_scene = "loading"
            self.start_loading_time = pygame.time.get_ticks()
            self.dropdown_active = False

    def render_multi_line(self, surfaces, start_y, return_positions=False, center=True):
        max_width = max(surface.get_width() for surface in surfaces)
        spacing = 10
        total_height = sum(surface.get_height() for surface in surfaces) + spacing * (len(surfaces) - 1)
        
        x_center = (self.screen_width - max_width) // 2
        if center:
            y_position = (self.screen_height - total_height) // 3 + start_y 
        else:
            y_position = start_y

        positions = []  

        for surface in surfaces:
            text_x = (self.screen_width - surface.get_width()) // 2  
            text_y = y_position
            self.screen.blit(surface, (text_x, text_y))
            positions.append((text_x, text_y))  
            y_position += surface.get_height() + spacing

        if return_positions:
            return positions

    def run(self):
        self.bgm.play(-1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.current_scene == 'intro':
                if not pygame.mixer.get_busy(): 
                    self.bgm.play(-1)
                self.intro_scene()
            if self.current_scene == 'loading':
                self.loading_scene(f"LOADING LEVEL {self.level}...")
            elif self.current_scene == 'game':
                self.bgm.stop()
                self.game_scene()
