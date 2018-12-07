# Easily consuming single-header C libraries in Python

This is a presentation I did on a technique I used for consuming 
single header C libraries from Python in a personal project, utilising
the hard work of other people so that I did not have to do any!

Given a single-header dependency with no existing binding, you can easily
create (and build, and package) one by feeding the header directly to
`cffi`, with some simple text transformations to remove problematic syntax.

Demo code & [presentation](https://nathanrw.github.io/single-header-c-libs-in-python/).

[nuklear-cffi](https://github.com/nathanrw/nuklear-cffi)

## Presenting

```bash
xrandr --output <projector> --auto
xrandr --output <projector> --scale-from <desktop-resolution>
reveal-md presentation.md # or navigate to static site.
```

## Publishing

```bash
reveal-md presentation.md --static docs --static-dirs=images
```

## Links

This presentation is a recipe for using the hard work of other people 
without going to much trouble. Here is that hard work:

- [nuklear](https://github.com/vurtun/nuklear), a ridiculously impressive
  GUI library with *no dependencies* in a single ANSI C header.
- [cffi](https://cffi.readthedocs.io/en/latest/), a foreign function
  interface library for Python which takes a reduced C syntax as its
  interface definition language and which can build and package C source
  code for you.
- [pcpp](https://github.com/ned14/pcpp), A C preprocessor written in
  Python.
