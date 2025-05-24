import pygame

class Player:
    def __init__(self, x, y, cell_size=40, speed=6):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.speed = speed  # píxeles por frame
        self.pixel_x = x * cell_size
        self.pixel_y = y * cell_size
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.moving = False
        self.move_dir = (0, 0)

        # Animación
        self.direction = 'down'
        self.anim_frame = 0
        self.anim_timer = 0
        self.anim_interval = 2  # velocidad de cambio de sprite

        size = int(cell_size * 0.8)
        self.sprites = {
            'up': [pygame.transform.scale(pygame.image.load(f'assets/mouse/up{i}.png'), (size, size)) for i in range(4)],
            'down': [pygame.transform.scale(pygame.image.load(f'assets/mouse/down{i}.png'), (size, size)) for i in range(4)],
            'left': [pygame.transform.scale(pygame.image.load(f'assets/mouse/left{i}.png'), (size, size)) for i in range(4)],
            'right': [pygame.transform.scale(pygame.image.load(f'assets/mouse/right{i}.png'), (size, size)) for i in range(4)],
        }

    def move(self, dx, dy, game_map):
        if self.moving:
            return
        nx, ny = self.x + dx, self.y + dy
        if (0 <= nx < game_map.cols and
            0 <= ny < game_map.rows and
                not game_map.is_wall(nx, ny)):
            self.x, self.y = nx, ny
            self.target_x = nx * self.cell_size
            self.target_y = ny * self.cell_size
            self.move_dir = (dx, dy)
            self.moving = True

            # Cambiar dirección para sprite
            if dx == -1: self.direction = 'left'
            elif dx == 1: self.direction = 'right'
            elif dy == -1: self.direction = 'up'
            elif dy == 1: self.direction = 'down'

            # Reiniciar animación
            self.anim_frame = 0
            self.anim_timer = 0

    def update(self):
        if self.moving:
            dx = self.target_x - self.pixel_x
            dy = self.target_y - self.pixel_y
            step_x = self.speed if dx > 0 else -self.speed
            step_y = self.speed if dy > 0 else -self.speed
            if abs(dx) > 0:
                self.pixel_x += step_x if abs(dx) >= self.speed else dx
            if abs(dy) > 0:
                self.pixel_y += step_y if abs(dy) >= self.speed else dy
            if self.pixel_x == self.target_x and self.pixel_y == self.target_y:
                self.moving = False

        # Actualizar animación si se está moviendo
        if self.moving:
            self.anim_timer += 1
            if self.anim_timer >= self.anim_interval:
                self.anim_frame = (self.anim_frame + 1) % 4
                self.anim_timer = 0

    def draw(self, screen, cell_size):
        size = int(cell_size * 0.5)
        offset = (cell_size - size) // 2
        sprite = self.sprites[self.direction][self.anim_frame]
        screen.blit(sprite, (self.pixel_x + offset, self.pixel_y + offset))
