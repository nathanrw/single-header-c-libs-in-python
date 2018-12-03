# Demo 3

For a more realistic example of this recipe in action, let's look at using the
`nuklear` GUI library from Python. Here's the header:

```bash
cd ../nuklear-cffi
vim nuklear/nuklear.h
```

It's huge!

But it's plain C, so it's very simple and we can build and parse it just the
same as we did before.

```bash
vim build.py
```

As you can see, it's no longer than our other build script.

Here's the call site:

```bash
vim demo/overview.py
```

It's a direct port of the `overview.c` demo from the `nuklear` repo. As you
can see, it is very long!

```bash
python2 demo/demo.py
```

There you have it! Can you imagine writing and maintaining a binding for that
API by hand? Yes, it would probably produce a nicer interface, but it would
take a lot of effort! *Worse is better.*
