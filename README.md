# Easily consuming single-header C libraries in Python

This is a presentation I did on a technique I used for consuming 
single header C libraries from Python in a personal project, utilising
the hard work of other people so that I did not have to do any!

Given a single-header dependency with no existing binding, you can easily
create (and build, and package) one by feeding the header directly to
`cffi`, with some simple text transformations to remove problematic syntax.

Demo code & [presentation](https://nathanrw.github.io/single-header-c-libs-in-python/).

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
