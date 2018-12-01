#!/bin/python

import pygame
import os
import sys

def load_image(filename):
    # Add BIF support
    return pygame.image.load(filename)
    
def save_image(image, filename):
    # Add BIF support
    return pygame.image.save(image, filename)

def main():

    in_filename = "background.png"
    if len(sys.argv) > 1:
        in_filename = sys.argv[1]
    out_filename = in_filename
    if len(sys.argv) > 2:
        out_filename = sys.argv[2]
        
    screen = pygame.display.set_mode((800, 600))
    
    try:
        image = load_image(in_filename)
        xformed = pygame.transform.scale(image, screen.get_size())
        screen.blit(xformed, (0, 0))
    except:
        pass
    
    running = True
    drawing = False
    last_pos = None
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                last_pos = e.pos
                drawing = True
            elif e.type == pygame.MOUSEBUTTONUP:
                drawing = False
        if drawing:
            cur_pos = pygame.mouse.get_pos()
            pygame.draw.line(screen, (255, 0, 0), last_pos, cur_pos, 2)
            last_pos = cur_pos
        pygame.display.update()
        
    save_image(screen, out_filename)

if __name__ == '__main__':
    main()