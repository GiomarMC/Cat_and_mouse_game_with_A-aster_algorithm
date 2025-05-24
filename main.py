import pygame
from game_map import GameMap
from player import Player
from enemy import Enemy
import time

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 80)
small_font = pygame.font.SysFont(None, 40)


def reset_game():
    global game_map, player, enemy, cheese_pos, move_dir, \
        running, game_state, winner
    game_map = GameMap(15, 15)
    player_start = game_map.get_valid_start_position('top_left')
    enemy_start = game_map.get_valid_start_position('bottom_right')
    player = Player(
        player_start[0], player_start[1], game_map.cell_size, speed=6
    )
    enemy = Enemy(enemy_start[0], enemy_start[1], game_map.cell_size, speed=4)
    cheese_pos = game_map.get_cheese_pos()
    move_dir = [0, 0]
    running = True
    game_state = 'countdown'
    winner = None


reset_game()

countdown_start = time.time()
countdown_time = 3  # segundos


def draw_center_text(text, font, color, y_offset=0, outline=True):
    # Dibuja texto con borde negro para contraste
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 + y_offset)
    )
    if outline:
        for ox in [-2, 0, 2]:
            for oy in [-2, 0, 2]:
                if ox != 0 or oy != 0:
                    outline_surface = font.render(text, True, (0, 0, 0))
                    outline_rect = rect.copy()
                    outline_rect.x += ox
                    outline_rect.y += oy
                    screen.blit(outline_surface, outline_rect)
    screen.blit(text_surface, rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_state == 'playing':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_dir = [-1, 0]
                elif event.key == pygame.K_RIGHT:
                    move_dir = [1, 0]
                elif event.key == pygame.K_UP:
                    move_dir = [0, -1]
                elif event.key == pygame.K_DOWN:
                    move_dir = [0, 1]
            elif event.type == pygame.KEYUP:
                if event.key in [
                    pygame.K_LEFT, pygame.K_RIGHT,
                    pygame.K_UP, pygame.K_DOWN
                ]:
                    move_dir = [0, 0]
        elif game_state == 'gameover':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()
                countdown_start = time.time()

    screen.fill((0, 0, 0))
    # Siempre dibujar el mapa y personajes
    game_map.draw(screen)
    player.draw(screen, game_map.cell_size)
    enemy.draw(screen, game_map.cell_size)
    pygame.draw.circle(
        screen,
        (255, 255, 0),
        (cheese_pos[0]*game_map.cell_size + game_map.cell_size//2,
         cheese_pos[1]*game_map.cell_size + game_map.cell_size//2),
        game_map.cell_size//3
    )

    if game_state == 'countdown':
        elapsed = time.time() - countdown_start
        count = countdown_time - int(elapsed)
        if count > 0:
            draw_center_text(str(count), font, (255, 255, 0))  # Amarillo
        elif 0 <= elapsed < countdown_time + 1:
            draw_center_text('GO!', font, (0, 255, 0))  # Verde
        else:
            game_state = 'playing'
    elif game_state == 'playing':
        # Movimiento continuo del jugador
        if move_dir != [0, 0] and not player.moving:
            player.move(move_dir[0], move_dir[1], game_map)
        player.update()
        # IA: recalcular ruta y mover al gato solo si no está moviéndose
        if not enemy.moving:
            enemy.update_path((player.x, player.y), game_map)
            enemy.follow_path()
        enemy.update()
        # Condición de victoria o derrota
        if (player.x, player.y) == (enemy.x, enemy.y):
            winner = 'cat'
            game_state = 'gameover'
        if (player.x, player.y) == cheese_pos:
            winner = 'mouse'
            game_state = 'gameover'
    elif game_state == 'gameover':
        if winner == 'mouse':
            draw_center_text(
                '¡El ratón ganó!', font, (0, 255, 0), y_offset=-40
            )
        elif winner == 'cat':
            draw_center_text(
                '¡El gato atrapó al ratón!', font, (255, 0, 0), y_offset=-40
            )
        draw_center_text(
            'Presiona ESPACIO para reiniciar',
            small_font,
            (255, 255, 255),
            y_offset=40
        )

    pygame.display.flip()
    clock.tick(60)
