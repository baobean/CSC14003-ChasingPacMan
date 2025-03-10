import pygame
# import csv
import utils

# class Map:
#     def __init__(self, file_path="map.csv"):
#         self.tile_size = utils.tile_size  # Kích thước mỗi ô
#         self.map_state = self.load_map(file_path)
#         self.width = len(self.map_state[0])
#         self.height = len(self.map_state)

#         # Màu sắc hiển thị
#         self.colors = {
#             0: (0, 0, 0),   # Đường đi (đen)
#             1: (50, 50, 200) # Tường (xanh dương)
#         }

    # def load_map(self, file_path):
    #     """Load bản đồ từ file CSV"""
    #     map_data = []
    #     with open(file_path, newline='') as csvfile:
    #         reader = csv.reader(csvfile)
    #         for row in reader:
    #             int_row = [int(cell) for cell in row]
    #             map_data.append(int_row)
        
    #     # Debugging: Print the loaded map to check correctness
    #     print("Loaded Map:")
    #     for row in map_data:
    #         print(row)  # Should match map.csv format

    #     return map_data


    # def draw(self, screen):
    #     """Vẽ bản đồ lên màn hình."""
    #     for y in range(self.height):
    #         for x in range(self.width):
    #             tile_value = self.map_state[y][x]
    #             color = self.colors.get(tile_value, (255, 255, 255))  # Mặc định là trắng
    #             rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
    #             pygame.draw.rect(screen, color, rect)

    # def is_walkable(self, x, y):
    #     """Kiểm tra xem vị trí có đi được không."""
    #     tile_x, tile_y = x // self.tile_size, y // self.tile_size
    #     if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
    #         return self.map_state[tile_y][tile_x] == 0  # 0 là đường đi
    #     return False
