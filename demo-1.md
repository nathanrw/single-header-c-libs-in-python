# Demo 1

This is our simple image editor.

```bash
python2 ./demo-1.py
```

You click and drag to draw. The drawing is saved and then loaded on the next
run.

Let's look at the code.

```bash
vim ./demo-1.py
```

As you can see, it's a really simple program. We use the `pygame` library to
provide us with a window to draw into, and some very simple logic to implement
our image editor.

We parse command line arguments:

```Python
    in_filename = "background.png"
    if len(sys.argv) > 1:
        in_filename = sys.argv[1]
    out_filename = "background.png"
    if len(sys.argv) > 2:
        out_filename = sys.argv[2]
```

Then we open a window and draw the input image into it:

```Python
    screen = pygame.display.set_mode((800, 600))
    
    if os.path.isfile(in_filename):
        image = load_image(in_filename)
        xformed = pygame.transform.scale(image, screen.get_size())
        screen.blit(xformed, (0, 0))
```

Then we run until the window is closed, drawing a line following the mouse
cursor while any button is pressed.

```Python
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
```

Finally, we save the image out.

```Python
    save_image(screen, out_filename)
```

Our task is to change this image functions to support the `.bif` format:

```Python
def load_image(filename):
    return pygame.image.load(filename)
    
def save_image(image, filename):
    pygame.image.save(image, filename)
```

We have a C library, `bif.h`:

```bash
vim bif.h
```

Let's have a quick look in here, but we don't need to pay too much attention.
They key thing is that this is a header-only C library with the declarations
at the top and the implementation at the bottom. We need some way to build the
thing and call functions like this:

```C
enum bif_error bif_image_read(
  const char* filename, 
  enum bif_flags flags, 
  struct bif_image* image
);
```

from Python.
