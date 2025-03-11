import pygame
import utils

class TextRenderer:
    def __init__(self):
        sprite_sheet_path = "assets/text/text.png"
        image = pygame.image.load(sprite_sheet_path).convert_alpha()

        scale_factor = utils.char_width / 8

        new_width = int(image.get_width() * scale_factor)
        new_height = int(image.get_height() * scale_factor)

        self.sprite_sheet = pygame.transform.scale(image, (new_width, new_height))
        
        self.chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ*-\"0123456789.>c&,"
        self.char_width = utils.char_width
        self.char_height = utils.char_height
        self.char_map = self.generate_char_map()
    
    def generate_char_map(self):
        char_map = {}
        columns = self.sprite_sheet.get_width() // self.char_width

        for index, char in enumerate(self.chars):
            x = (index % columns) * self.char_width
            y = (index // columns) * self.char_height
            char_map[char] = self.sprite_sheet.subsurface(x, y, self.char_width, self.char_height)

        return char_map
    
    def render_text(self, surface, text, pos_x, pos_y, spacing = 1):
        x_offset = pos_x

        for char in text:
            if char in self.char_map:
                char_image = self.char_map[char]
                surface.blit(char_image, (x_offset, pos_y))
                x_offset += self.char_width + spacing
            elif char == ' ':
                x_offset += self.char_width + spacing

