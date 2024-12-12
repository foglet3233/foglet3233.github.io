import pygame
import random
import sys
from pygame.math import Vector3
import math

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
DARK_RED = (139, 0, 0)
GREEN = (0, 255, 0)


def main():
    pygame.init()

    # Load audio
    pygame.mixer.init()
    hit_sound = pygame.mixer.Sound("kill.mp3")

    # Screen setup
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Simple Duty 3D")
    clock = pygame.time.Clock()

    # Player setup
    player_pos = Vector3(0, 0, 0)  # Player's position in the 3D world
    player_angle = 0  # Horizontal angle for looking around
    player_vertical_angle = 0  # Vertical angle for looking up and down
    move_speed = 0.1
    strafe_speed = 0.05  # Reduced speed for strafing

    # Sensitivity settings
    sensitivity_scale = 2  # Default sensitivity (1-10)
    turn_speed = 0.0012 * sensitivity_scale

    # Enemy setup
    enemies = initialize_enemies()
    enemy_states = {i: {'color': RED, 'timer': 0} for i in range(len(enemies))}

    # Game variables
    score = 0
    running = True
    paused = False

    pygame.event.set_grab(True)  # Lock the mouse to the screen
    pygame.mouse.set_visible(False)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = not paused
                pygame.mouse.set_visible(paused)
                pygame.event.set_grab(not paused)

        if paused:
            render_paused(screen)
            pygame.display.flip()
            clock.tick(60)
            continue

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_mouse_click(player_pos, enemies, enemy_states, player_angle, player_vertical_angle, hit_sound)

        # Movement controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.x += math.sin(player_angle) * move_speed
            player_pos.z += math.cos(player_angle) * move_speed
        if keys[pygame.K_s]:
            player_pos.x -= math.sin(player_angle) * move_speed
            player_pos.z -= math.cos(player_angle) * move_speed
        if keys[pygame.K_a]:
            player_pos.x -= math.cos(player_angle) * strafe_speed
            player_pos.z += math.sin(player_angle) * strafe_speed
        if keys[pygame.K_d]:
            player_pos.x += math.cos(player_angle) * strafe_speed
            player_pos.z -= math.sin(player_angle) * strafe_speed

        # Mouse look
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        player_angle += mouse_dx * turn_speed
        player_vertical_angle = max(-math.pi / 4, min(math.pi / 4, player_vertical_angle - mouse_dy * turn_speed))

        # Update enemy states
        update_enemy_states(enemy_states)

        # Update screen
        screen.fill(WHITE)
        render_crosshair(screen)
        render_enemies(screen, player_pos, enemies, enemy_states, player_angle, player_vertical_angle)
        render_score(screen, score)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


def initialize_enemies():
    """Initializes the enemies with random positions in 3D space."""
    enemies = []
    for _ in range(10):
        pos = Vector3(random.uniform(-5, 5), random.uniform(-1, 1), random.uniform(5, 20))
        enemies.append(pos)
    return enemies


def handle_mouse_click(player_pos, enemies, enemy_states, player_angle, player_vertical_angle, hit_sound):
    """Handles mouse clicks to check if an enemy is under the crosshair."""
    for i, enemy_pos in enumerate(enemies):
        screen_x, screen_y, size = project_to_screen(player_pos, enemy_pos, player_angle, player_vertical_angle)
        if 390 <= screen_x <= 410 and 290 <= screen_y <= 310:  # Crosshair region
            enemy_states[i]['color'] = GREEN
            enemy_states[i]['timer'] = 180  # 3 seconds at 60 FPS
            hit_sound.play()  # Play the hit sound


def update_enemy_states(enemy_states):
    """Updates the states of the enemies to handle color change timers."""
    for state in enemy_states.values():
        if state['timer'] > 0:
            state['timer'] -= 1
            if state['timer'] == 0:
                state['color'] = RED


def render_paused(screen):
    """Renders the paused screen."""
    font = pygame.font.Font(None, 74)
    paused_text = font.render("PAUSED", True, BLACK)
    screen.blit(paused_text, (400 - paused_text.get_width() // 2, 300 - paused_text.get_height() // 2))


def render_crosshair(screen):
    """Renders a simple crosshair at the center of the screen."""
    pygame.draw.line(screen, BLACK, (400 - 10, 300), (400 + 10, 300), 2)
    pygame.draw.line(screen, BLACK, (400, 300 - 10), (400, 300 + 10), 2)


def render_enemies(screen, player_pos, enemies, enemy_states, player_angle, player_vertical_angle):
    """Renders enemies as fully 3D spheres with realistic shading on the screen."""
    light_dir = Vector3(1, -1, -1).normalize()  # Light direction for shading
    ambient_light = 0.5  # Increase ambient light to brighten spheres
    for i, enemy_pos in enumerate(enemies):
        screen_x, screen_y, size = project_to_screen(player_pos, enemy_pos, player_angle, player_vertical_angle)
        if 0 <= screen_x < 800 and 0 <= screen_y < 600:
            color = enemy_states[i]['color']
            for y in range(-size, size):
                for x in range(-size, size):
                    if x**2 + y**2 <= size**2:  # Check if the point is inside the circle
                        nx = x / size  # Normalized x-coordinate
                        ny = y / size  # Normalized y-coordinate
                        nz = math.sqrt(1 - nx**2 - ny**2) if nx**2 + ny**2 < 1 else 0  # Normalized z-coordinate
                        normal = Vector3(nx, ny, nz)
                        intensity = max(ambient_light, light_dir.dot(normal))  # Compute lighting intensity
                        shaded_color = (
                            int(color[0] * intensity),
                            int(color[1] * intensity),
                            int(color[2] * intensity),
                        )
                        screen.set_at((screen_x + x, screen_y + y), shaded_color)


def project_to_screen(player_pos, enemy_pos, player_angle, player_vertical_angle):
    """Projects 3D coordinates into 2D screen space and calculates size based on distance."""
    relative_pos = enemy_pos - player_pos

    # Rotate based on player angle
    rotated_x = relative_pos.x * math.cos(player_angle) - relative_pos.z * math.sin(player_angle)
    rotated_z = relative_pos.x * math.sin(player_angle) + relative_pos.z * math.cos(player_angle)
    rotated_y = relative_pos.y * math.cos(player_vertical_angle) - rotated_z * math.sin(player_vertical_angle)
    rotated_z = relative_pos.y * math.sin(player_vertical_angle) + rotated_z * math.cos(player_vertical_angle)

    scale = 500 / max(rotated_z, 0.1)  # Avoid division by zero
    screen_x = int(400 + rotated_x * scale)
    screen_y = int(300 - rotated_y * scale)
    size = max(5, int(50 / rotated_z))  # Enemies get larger as they get closer
    return screen_x, screen_y, size


def shoot_enemies(player_pos, enemies):
    """Checks if the player shoots an enemy in range."""
    for enemy_pos in enemies:
        if abs(player_pos.z - enemy_pos.z) < 1 and abs(player_pos.x - enemy_pos.x) < 1:
            enemies.remove(enemy_pos)
            return 1
    return 0


def render_score(screen, score):
    """Displays the player's score on the screen."""
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))


if __name__ == "__main__":
    main()
