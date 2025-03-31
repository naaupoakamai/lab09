import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Paint")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

color = BLACK
radius = 5
mode = 'free'
drawing = False
start_pos = None

screen.fill(WHITE)
pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            if mode == 'free':
                pygame.draw.circle(screen, color, event.pos, radius)

        elif event.type == pygame.MOUSEBUTTONUP:
            end_pos = event.pos
            drawing = False

            if mode == 'rect':
                rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                pygame.draw.rect(screen, color, rect, width=2)

            elif mode == 'circle':
                center = start_pos
                radius_c = int(math.hypot(end_pos[0]-center[0], end_pos[1]-center[1]))
                pygame.draw.circle(screen, color, center, radius_c, width=2)

            elif mode == 'square':
                side = max(abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1]))
                rect = pygame.Rect(start_pos[0], start_pos[1], side, side)
                pygame.draw.rect(screen, color, rect, width=2)

            elif mode == 'right_triangle':
                x1, y1 = start_pos
                x2, y2 = end_pos
                points = [start_pos, (x2, y1), end_pos]
                pygame.draw.polygon(screen, color, points, width=2)

            elif mode == 'equilateral_triangle':
                x1, y1 = start_pos
                x2, y2 = end_pos
                side = abs(x2 - x1)
                height = int((3 ** 0.5 / 2) * side)
                points = [start_pos, (x1 + side, y1), (x1 + side // 2, y1 - height)]
                pygame.draw.polygon(screen, color, points, width=2)

            elif mode == 'rhombus':
                x1, y1 = start_pos
                x2, y2 = end_pos
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                dx = abs(x2 - x1) // 2
                dy = abs(y2 - y1) // 2
                points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
                pygame.draw.polygon(screen, color, points, width=2)

        elif event.type == pygame.MOUSEMOTION:
            if drawing and mode == 'free':
                pygame.draw.circle(screen, color, event.pos, radius)
            elif drawing and mode == 'eraser':
                pygame.draw.circle(screen, WHITE, event.pos, radius)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                mode = 'rect'
            elif event.key == pygame.K_c:
                mode = 'circle'
            elif event.key == pygame.K_f:
                mode = 'free'
            elif event.key == pygame.K_e:
                mode = 'eraser'
            elif event.key == pygame.K_s:
                mode = 'square'
            elif event.key == pygame.K_t:
                mode = 'right_triangle'
            elif event.key == pygame.K_q:
                mode = 'equilateral_triangle'
            elif event.key == pygame.K_h:
                mode = 'rhombus'

            elif event.key == pygame.K_1:
                color = RED
            elif event.key == pygame.K_2:
                color = GREEN
            elif event.key == pygame.K_3:
                color = BLUE
            elif event.key == pygame.K_4:
                color = BLACK
            elif event.key == pygame.K_5:
                color = WHITE

    pygame.display.flip()

pygame.quit()
