# Easily re-use single header c libraries in Python using `cffi`

### Nathan Woodward

---

# What is this?

- A technique for easily re-using single-header C libraries from Python.

- A C preprocessor is utilised alongside simple text transformations 
  such that input for the `cffi` interop library can be generated 
  automatically from the header itself.

---

# Why are we here?

- This will likely have little to no *direct* applicability to the day-to-day 
  lives of many of the people in this room.

- I present it nevertheless for your extra-curricular enrichment!

---

# The problem

- Suppose I am writing a Python program, and I need to do something 
  complicated. There is a good library for it, but it is written 
  in C.
- What do I do?
  - Use an existing *binding* for it.
  - Roll my own.

---

# Writing a binding

- Turns out, there's not a binding for our library (or perhaps 
  there is one but it's incomplete or unmaintained...)

- But, it's been written following the *single-header* idiom, for ease 
  of integration.

---

# Single-header C libraries

- A (horrible bodge | cunning workaround) to the problem of 
  integrating C/C++ libraries.

- Instead of worrying about build systems, artifacts and so 
  on, just write the whole thing in one header.

- Clients then `#include` it and build it however they want.

---

# Single-header C libraries

```C
/* pfx.h */
int pfx_do_it();

#ifdef PFX_IMPLEMENTATION
int pfx_do_it()
{
    return 0;
}
#endif
```

---

# Image editor

- We're developing an image editor.

- I want to edit my favourite picture, `mystery.bif`, so we need
  to add support for it.
  
- This is an obscure format read and written by the single-header
  C library `bif.h`.

---

# DEMO: Image editor

---

# What are our options?

1. Write a C++ Python module that wraps the library and
   exposes what we want to Python.
     
2. Build a dll and poke it via `ctypes`.
  
3. Use some sort of binding generator e.g. `SWIG` to
   automate the process.

---

# Write a C++ Python module

Nope.

Note: Completely manual. How to build and package? Got to maintain it. Urgh!

---

# Build a DLL and poke it

Nope.

Note: Same problem of building and packaging. Got to duplicate header info in Python.

---

# Use a binding generator

- Sounds groovy! However, there is a slight issue. 

- e.g. `SWIG` interface definition. Duplicates information 
  that is present in the library.

  ```SWIG
  // wibble.i
  enum my_flag {wblWIBBLE = 3, wblWOBBLE = 5};
  ```

- Would be nice to automate this if possible.

---

# The `cffi` library

- A library for producing Python bindings for C libraries
  without learning a special language (e.g. `SWIG`).
  
- Generates a Python module from snippets of the C declarations
  that you want to expose.

- *Semi-automatic* - you can't just pass it a whole header (d'oh!)

---

# Can we do better?

- So, we're stuck pasting in snippets from the header and maintaining
  the thing by hand?

---

# Can we do better?

- Yes!

- Preprocess the header to remove problematic syntax, then 
  feed the whole thing to `cffi`.

- We only care about one header, not every possible header!

- Virtually no maintanance, and easy to build and package!

---

# DEMO

Note: build.py
      show changes to demo.py
      note the use of `pcpp` library. Pure python preprocessor.
      shift and or evaluation
      `python setup.py install; python demo.py`

---

<img src="./images/a-pair-of-pigs.jpg" alt="A pair of pigs" width="500"/>

Unknown, *A Pair of Pigs*, circa 1850, oil on canvas, Compton Verney, Warwickshire
    
---

# A real example: `nuklear-cffi`.

- Benefits of the technique become apparent with ginormous libraries.

- This allowed me to use this GUI library from Python without 
  going insane: https://github.com/vurtun/nuklear

---

# DEMO: `nuklear-cffi`

Note: Show nuklear.h
      Show build.py
      Run demo.py

---

# Conclusion

- The use of `cffi` is not novel. But I've not seen *this
  degree of automation* elsewhere.

- Reduced maintanance and build complexity for simple dependencies.

- Allows you to get a complete solution going very quickly.

- At the cost of being a very low-level interface.

---

# Questions