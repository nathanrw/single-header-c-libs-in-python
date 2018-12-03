# Demo 2

So, we're going to do just that with `bif.h`. Or rather, in classic Blue Peter
fashion, I will now show you one I made earlier.

```bash
vim build.py
```

This is the build script that feeds our definitions and source code to the `cffi`
library so that it can build a Python module for us. Here's the entry point:

```Python
def main():
    ffibuilder = maker()
    ffibuilder.compile(verbose=True)
```

And here's the main flow of it:

```Python
def maker():
    """ Make the ffibuilder object for parsing the bif.h header. """
    
    header_filename = "bif.h"
    
    header_contents = open(header_filename, 'r').read()
    
    source = """
    #define BIF_IMPLEMENTATION
    """ + header_contents
    
    defs = build_cdef(header_contents)
    
    ffibuilder = cffi.FFI()
    ffibuilder.cdef(defs)
    ffibuilder.set_source("_bif", source, libraries=[])
    return ffibuilder
```

We do two things here: parse *definitions* from the header file, and provide
source for the ffi builder to build. *Since this is a header-only library, the
source is just the header with a special flag set!*

Note: this means that the *building* of the code is taken care of for us.
Python actually contains a simple C/C++ build system! You need a compiler for
this to work, but *you can package the resulting module*

The interesting thing here, though, is what we do inside `build_cdef()`.

```Python
def build_cdef(header_contents):
    header_only_options = """
    """
    preprocessed_text = run_c_preprocessor(header_only_options + header_contents)
    preprocessed_text = evaluate_shift(preprocessed_text)
    preprocessed_text = evaluate_or(preprocessed_text)
    write_debug_file(preprocessed_text, "cdef.h")
    return preprocessed_text
```

The header is preprocessed to strip out comments and evaluate macros.

This is *nearly* simple enough to be fed to `cffi`, except...

Note: comment out `evaluate_shift` and `evaluate_or`.

```bash
python2 setup.py build #ERROR
vim bif.h
```

(Note: setup.py defines our package, and it runs build.py)

```C
#define BIF_FLAG(N) (1 << (N))

#define BIF_CHECK_FLAG(VAR, FLAG) (!!(VAR & FLAG))

enum bif_flags {
    BIF_FLAG_NONE = 0,
    BIF_FLAG_WIBBLE = BIF_FLAG(0),
    BIF_FLAG_WOBBLE = BIF_FLAG(1),
    BIF_FLAG_WIBBLE_WOBBLE = BIF_FLAG_WIBBLE | BIF_FLAG_WOBBLE
};
```

Some joker has defined his flags in an interesting way, and `cffi` doesn't
like it!  But we still have a trick up our sleeve...

```bash
vim build.py
```

Note: comment in `evaluate_shift` and `evaluate_or`.

```Python
def evaluate_shift(preprocessed_text):
    shift_expr = "\\(1 << \\(([0-9]+)\\)\\)"
    def evaluate_shift(match):
        return str(1 << int(match.group(1)))
    return re.sub(shift_expr, evaluate_shift, preprocessed_text)
```

With a simple regex we can evaluate these compile-time constants to a point
where `cffi` can understand them.

```bash
python2 setup.py install # HURRAH
```

We've built it! Let's look at what the calling code looks like...

```bash
vim demo-2.py
```

First, we import the module (we called it `_bif` in `setup.py`.)

```Python
import _bif
```

Then, we can call the functions defined by our header.

```Python
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
```

This is noticeably unpythonic and looks a lot like C! But we got to this point
without doing any legwork. Our code is built, packaged, and we can finally
read that mystery image...

```bash
python2 demo-2.py mystery.bif
```
