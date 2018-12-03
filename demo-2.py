#!/bin/python

import pygame
import os
import sys
import _bif

def load_image(filename):
    # Create struct to fill out. This is managed by a python object which deletes
    # the memory when it is garbage collected.
    bif_image = _bif.ffi.new("struct bif_image*")
    
    # Attempt to read the file as BIF.
    result = _bif.lib.bif_image_read(filename, _bif.lib.BIF_FLAG_WIBBLE, bif_image)
    if result == _bif.lib.BIF_OK:
    
        # Get the data as a python string.
        num_bytes = bif_image.width * bif_image.height * 4
        buffer = _bif.ffi.unpack(_bif.ffi.cast("char*", bif_image.buffer), num_bytes)
        
        # Turn that into a pygame surface. This copies the data.
        ret = pygame.image.fromstring(buffer, (bif_image.width, bif_image.height), "RGBA")
        
        # Make sure to clean up the memory allocated by bif_image_read()!
        _bif.lib.bif_image_free(bif_image)
        return ret
        
    else:
        # It's not a BIF image so use pygame's image loading.
        return pygame.image.load(filename)
    
def save_image(image, filename):
    data = pygame.image.tostring(image, "RGBA")
    bif_image = _bif.ffi.new("struct bif_image*")
    bif_image.width = image.get_width()
    bif_image.height = image.get_height()
    bif_image.buffer = _bif.ffi.cast("uint32_t*", _bif.ffi.from_buffer(data))
    error = _bif.lib.bif_image_write(filename, _bif.lib.BIF_FLAG_WOBBLE, bif_image)
    if error != _bif.lib.BIF_OK:
        raise Exception("Failed to write BIF image. Error code: %s" % error)

def main():

    in_filename = "background.bif"
    if len(sys.argv) > 1:
        in_filename = sys.argv[1]
    out_filename = "background.bif"
    if len(sys.argv) > 2:
        out_filename = sys.argv[2]
        
    screen = pygame.display.set_mode((800, 600))
    
    if os.path.isfile(in_filename):
        image = load_image(in_filename)
        xformed = pygame.transform.scale(image, screen.get_size())
        screen.blit(xformed, (0, 0))
    
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