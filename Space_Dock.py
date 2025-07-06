import pygame
import sys
import math
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sci-Fi Docking Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
LIGHT_GRAY = (180, 180, 180)
GREEN = (0, 255, 0)
ORANGE = (255, 150, 0)
RED = (255, 0, 0)
BLUE = (100, 255, 255)
YELLOW = (255, 255, 0)
DARK_SPACE = (10, 10, 30)
THRUSTER_ORANGE = (255, 100, 10)
PANEL = (80, 120, 150)

# Fonts
font = pygame.font.SysFont("consolas", 24)
big_font = pygame.font.SysFont("consolas", 36)

# Constants
ship_size = 25
thrust = 0.1
rotation_speed = 2
SAFE_SPEED = 0.6
WARNING_SPEED = 1.0
CRASH_SPEED = 1.8
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]

# Station parts
dock = pygame.Rect(WIDTH // 2 - 25, 70, 50, 25)  # Extended outward
station_body = pygame.Rect(WIDTH // 2 - 80, 20, 160, 60)
left_panel = pygame.Rect(WIDTH // 2 - 170, 30, 60, 40)
right_panel = pygame.Rect(WIDTH // 2 + 110, 30, 60, 40)

def reset_game():
    return {
        "pos": pygame.Vector2(random.randint(100, WIDTH - 100), random.randint(HEIGHT//2, HEIGHT - 50)),
        "velocity": pygame.Vector2(0, 0),
        "angle": 0,
        "success": False,
        "paused": False,
        "game_over": False,
        "crashed": False
    }

game = reset_game()

def draw_background():
    screen.fill(DARK_SPACE)
    for star in stars:
        pygame.draw.circle(screen, WHITE, star, 1)

def draw_button(rect, text, hover=False):
    pygame.draw.rect(screen, GRAY if not hover else (100, 100, 100), rect, border_radius=8)
    label = font.render(text, True, WHITE)
    screen.blit(label, (rect.x + 20, rect.y + 10))

def draw_flame(x, y, angle):
    shape = [(0, 0), (-5, 10), (5, 10)]
    rotated = []
    for px, py in shape:
        rx = px * math.cos(math.radians(angle)) - py * math.sin(math.radians(angle))
        ry = px * math.sin(math.radians(angle)) + py * math.cos(math.radians(angle))
        rotated.append((x + rx, y + ry))
    pygame.draw.polygon(screen, THRUSTER_ORANGE, rotated)

def draw_thrusters(pos, angle, keys):
    x, y = pos.x, pos.y
    if keys[pygame.K_UP]:
        rear_offset = pygame.Vector2(0, ship_size + 8).rotate(-angle)
        draw_flame(x + rear_offset.x, y + rear_offset.y, angle)
    if keys[pygame.K_DOWN]:
        nose_offset = pygame.Vector2(0, -ship_size - 8).rotate(-angle)
        draw_flame(x + nose_offset.x, y + nose_offset.y, angle + 180)
    if keys[pygame.K_LEFT]:
        right_offset = pygame.Vector2(ship_size + 8, 0).rotate(-angle)
        draw_flame(x + right_offset.x, y + right_offset.y, angle + 90)
    if keys[pygame.K_RIGHT]:
        left_offset = pygame.Vector2(-ship_size - 8, 0).rotate(-angle)
        draw_flame(x + left_offset.x, y + left_offset.y, angle - 90)

def draw_ship(x, y, angle):
    points = [(0, -ship_size), (ship_size // 2, ship_size), (-ship_size // 2, ship_size)]
    rotated = []
    for px, py in points:
        rx = px * math.cos(math.radians(angle)) - py * math.sin(math.radians(angle))
        ry = px * math.sin(math.radians(angle)) + py * math.cos(math.radians(angle))
        rotated.append((x + rx, y + ry))
    pygame.draw.polygon(screen, BLUE, rotated)
    pygame.draw.circle(screen, YELLOW, (int(x), int(y)), 3)

def draw_station():
    pygame.draw.rect(screen, GRAY, station_body, border_radius=12)
    for panel in [left_panel, right_panel]:
        pygame.draw.rect(screen, PANEL, panel)
        pygame.draw.rect(screen, LIGHT_GRAY, panel, 2)
        for i in range(1, 5):
            pygame.draw.line(screen, LIGHT_GRAY, (panel.left + i * 12, panel.top), (panel.left + i * 12, panel.bottom))
    pygame.draw.rect(screen, GREEN if not game["success"] else WHITE, dock, border_radius=5)
    pygame.draw.rect(screen, RED, (WIDTH//2 - 60, 30, 10, 40))
    pygame.draw.rect(screen, RED, (WIDTH//2 + 50, 30, 10, 40))
    pygame.draw.circle(screen, BLUE, (WIDTH//2, 70), 8)

def draw_radar(ship_pos, station_pos):
    radar_size = 150
    radar_rect = pygame.Rect(WIDTH - radar_size - 20, HEIGHT - radar_size - 20, radar_size, radar_size)
    center = radar_rect.center
    pygame.draw.rect(screen, (20, 20, 40), radar_rect)
    pygame.draw.rect(screen, LIGHT_GRAY, radar_rect, 2)
    pygame.draw.circle(screen, BLUE, center, 4)
    scale = 0.1
    rel = (station_pos - ship_pos) * scale
    dock_x = int(center[0] + rel.x)
    dock_y = int(center[1] + rel.y)
    pygame.draw.rect(screen, RED, pygame.Rect(dock_x - 3, dock_y - 3, 6, 6))

def angle_in_range(angle, start, end):
    angle %= 360
    start %= 360
    end %= 360
    if start < end:
        return start <= angle <= end
    else:
        return angle >= start or angle <= end

def get_speed_color(speed):
    abs_speed = abs(speed)
    if abs_speed < SAFE_SPEED:
        return GREEN
    elif abs_speed < WARNING_SPEED:
        return ORANGE
    else:
        return RED

def get_angle_color(angle):
    if angle_in_range(angle, 330, 30):
        return GREEN
    elif angle_in_range(angle, 310, 50):
        return ORANGE
    else:
        return RED

def check_crash_or_collision(pos, velocity, angle):
    ship_rect = pygame.Rect(pos.x - 15, pos.y - 15, 30, 30)
    speed = velocity.length()
    angle_ok = angle_in_range(angle, 330, 30)
    forward_vector = pygame.Vector2(0, -1).rotate(-angle)
    forward_speed = velocity.dot(forward_vector)
    speed_color = get_speed_color(forward_speed)

    touching_dock = ship_rect.colliderect(dock)
    touching_body = ship_rect.colliderect(station_body)
    touching_panels = ship_rect.colliderect(left_panel) or ship_rect.colliderect(right_panel)

    if touching_panels:
        return "crash"
    elif touching_dock:
        if speed_color == RED:
            return "crash"
        elif speed_color in [GREEN, ORANGE] and angle_ok:
            return "dock"
        else:
            return "crash"
    elif touching_body:
        return "crash"
    return None

# Main loop
running = True
while running:
    clock.tick(60)
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game["game_over"]:
            if event.key == pygame.K_p:
                game["paused"] = not game["paused"]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if game["paused"]:
                if pygame.Rect(400, 250, 200, 40).collidepoint(mx, my):
                    game["paused"] = False
                elif pygame.Rect(400, 310, 200, 40).collidepoint(mx, my):
                    game = reset_game()
            if game["game_over"]:
                if pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 40, 200, 40).collidepoint(mx, my):
                    game = reset_game()

    keys = pygame.key.get_pressed()
    if not game["paused"] and not game["game_over"]:
        if keys[pygame.K_COMMA]:
            game["angle"] += rotation_speed
        if keys[pygame.K_PERIOD]:
            game["angle"] -= rotation_speed
        if keys[pygame.K_UP]:
            game["velocity"] += pygame.Vector2(0, -thrust).rotate(-game["angle"])
        if keys[pygame.K_DOWN]:
            game["velocity"] += pygame.Vector2(0, thrust).rotate(-game["angle"])
        if keys[pygame.K_LEFT]:
            game["velocity"] += pygame.Vector2(-thrust, 0).rotate(-game["angle"])
        if keys[pygame.K_RIGHT]:
            game["velocity"] += pygame.Vector2(thrust, 0).rotate(-game["angle"])

        game["pos"] += game["velocity"]
        game["pos"].x = max(0, min(WIDTH, game["pos"].x))
        game["pos"].y = max(0, min(HEIGHT, game["pos"].y))

        status = check_crash_or_collision(game["pos"], game["velocity"], game["angle"])
        if status == "crash":
            game["game_over"] = True
            game["crashed"] = True
        elif status == "dock":
            game["game_over"] = True
            game["success"] = True

    draw_station()
    draw_thrusters(game["pos"], game["angle"], keys)
    draw_ship(game["pos"].x, game["pos"].y, game["angle"])

    forward_vector = pygame.Vector2(0, -1).rotate(-game["angle"])
    forward_speed = game["velocity"].dot(forward_vector)
    strafe_vector = pygame.Vector2(1, 0).rotate(-game["angle"])
    strafe_speed = game["velocity"].dot(strafe_vector)
    angle_mod = game["angle"] % 360

    forward_color = get_speed_color(forward_speed)
    strafe_color = get_speed_color(strafe_speed)
    angle_color = get_angle_color(angle_mod)

    screen.blit(font.render(f"Forward Speed: {forward_speed:.2f}", True, forward_color), (20, HEIGHT - 100))
    screen.blit(font.render(f"Strafe  Speed: {strafe_speed:.2f}", True, strafe_color), (20, HEIGHT - 70))
    screen.blit(font.render(f"Angle: {angle_mod:.2f}", True, angle_color), (20, HEIGHT - 40))

    if game["game_over"]:
        if game["success"]:
            screen.blit(big_font.render("\u2705 Docking Successful!", True, GREEN), (WIDTH//2 - 180, HEIGHT//2 - 50))
        elif game["crashed"]:
            screen.blit(big_font.render("\u274C Docking Failed!", True, RED), (WIDTH//2 - 150, HEIGHT//2 - 50))
        restart_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 40, 200, 40)
        draw_button(restart_btn, "RESTART", restart_btn.collidepoint(pygame.mouse.get_pos()))

    if game["paused"]:
        screen.blit(big_font.render("\u23F8\ufe0f GAME PAUSED", True, WHITE), (WIDTH//2 - 150, HEIGHT//2 - 100))
        draw_button(pygame.Rect(400, 250, 200, 40), "CONTINUE", pygame.Rect(400, 250, 200, 40).collidepoint(pygame.mouse.get_pos()))
        draw_button(pygame.Rect(400, 310, 200, 40), "RESTART", pygame.Rect(400, 310, 200, 40).collidepoint(pygame.mouse.get_pos()))

    draw_radar(game["pos"], pygame.Vector2(WIDTH//2, 70))
    pygame.display.flip()

pygame.quit()
sys.exit()
