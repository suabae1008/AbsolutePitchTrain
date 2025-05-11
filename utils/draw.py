# draw.py

import pygame

def draw_piano(screen, font, white_notes, black_notes, active_whites=None, active_blacks=None, label=""):
    screen.fill('white')
    active_whites = active_whites or []
    active_blacks = active_blacks or []

    for i, note in enumerate(white_notes):
        c = 'lightblue' if i in active_whites else 'white'
        pygame.draw.rect(screen, c, [i * 40, 100, 40, 300])
        pygame.draw.rect(screen, 'black', [i * 40, 100, 40, 300], 2)

    black_idx = 0
    for i in range(len(white_notes) - 1):
        if white_notes[i][0] in ['E', 'B']: continue
        c = 'lightblue' if black_idx in active_blacks else 'black'
        pygame.draw.rect(screen, c, [i * 40 + 28, 100, 24, 180])
        black_idx += 1

    if label:
        label_surface = font.render(label, True, (0, 0, 0))
        screen.blit(label_surface, (20, 20))
