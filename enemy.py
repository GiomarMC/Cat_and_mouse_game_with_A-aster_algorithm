from a_star import a_star
import pygame


class Enemy:
    def __init__(self, x, y, cell_size=40, speed=4):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.speed = speed  # píxeles por frame
        self.pixel_x = x * cell_size
        self.pixel_y = y * cell_size
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.moving = False
        self.path = []

        # Para animación
        self.direction = 'down'
        self.anim_frame = 0
        self.anim_timer = 0
        self.anim_interval = 5  # cada 5 frames cambia el sprite

        size = int(cell_size * 1.2)
        self.sprites = {
            'up': [pygame.transform.scale(pygame.image.load(f'assets/cat/up{i}.png'), (size, size)) for i in range(4)],
            'down': [pygame.transform.scale(pygame.image.load(f'assets/cat/down{i}.png'), (cell_size, cell_size)) for i in range(4)],
            'left': [pygame.transform.scale(pygame.image.load(f'assets/cat/left{i}.png'), (size, size)) for i in range(4)],
            'right': [pygame.transform.scale(pygame.image.load(f'assets/cat/right{i}.png'), (size, size)) for i in range(4)],
        }

    def update_path(self, target_pos, game_map):
        self.path = a_star((self.x, self.y), target_pos, game_map.grid)

    def follow_path(self):
        if self.moving:
            return
        if self.path and len(self.path) > 1:
            nx, ny = self.path[1]
            dx, dy = nx - self.x, ny - self.y
            if dx == 1: self.direction = 'right'
            elif dx == -1: self.direction = 'left'
            elif dy == 1: self.direction = 'down'
            elif dy == -1: self.direction = 'up'

            self.x, self.y = nx, ny
            self.target_x = nx * self.cell_size
            self.target_y = ny * self.cell_size
            self.moving = True

    def update(self):
        if self.moving:
            dx = self.target_x - self.pixel_x
            dy = self.target_y - self.pixel_y
            step_x = self.speed if dx > 0 else -self.speed
            step_y = self.speed if dy > 0 else -self.speed
            if abs(dx) > 0:
                if abs(dx) < self.speed:
                    self.pixel_x = self.target_x
                else:
                    self.pixel_x += step_x
            if abs(dy) > 0:
                if abs(dy) < self.speed:
                    self.pixel_y = self.target_y
                else:
                    self.pixel_y += step_y
            if self.pixel_x == self.target_x and self.pixel_y == self.target_y:
                self.moving = False

        # Control de animación
        self.anim_timer += 1
        if self.anim_timer >= self.anim_interval:
            self.anim_frame = (self.anim_frame + 1) % 4
            self.anim_timer = 0

    def draw(self, screen, cell_size):
        sprite = self.sprites[self.direction][self.anim_frame]
        screen.blit(sprite, (self.pixel_x, self.pixel_y))
