### Easily re-use single header c libraries in Python using `cffi`

Nathan Woodward

---

### What is this?

- A technique for easily re-using single-header C libraries from Python.

- A C preprocessor is utilised alongside simple text transformations 
  such that input for the `cffi` interop library can be generated 
  automatically from the header itself.

---

### Why are we here?

- This will likely have little to no *direct* applicability to the day-to-day 
  lives of many of the people in this room.

- I present it nevertheless for your extra-curricular enrichment!

---

### Image editor

- We're developing an image editor.

- I want to edit my favourite picture, `mystery.bif`, so we need
  to add support for it.
  
  - This is an obscure format read and written by the *single-header
    C library* `bif.h`. 
    
  - No *binding* for it yet exists.
  
Note: binding - wrapper through which we can re-use code written
      in a different language.

---

### Single-header C libraries

- A (horrible bodge | cunning workaround) to the problem of 
  integrating C and C++ libraries.

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
  
- Just write the whole thing in one header and build how you like.

<!-- Note: Instead of worrying about build systems, artifacts and so on, just write the whole thing in one header.
  
Note: Clients then `#include` it and build it however they want. -->

---

### DEMO: Image editor

Note: See `demo-1.md`.

---

### Writing a binding

1. Write a C++ Python module that wraps the library and
   exposes what we want to Python.
     
2. Build a dll and poke it via `ctypes`.
  
3. Use some sort of binding generator e.g. `SWIG` to
   automate the process.

---

### Write a C++ Python module

Nope.

Note: Completely manual. How to build and package? Got to maintain it. Urgh!

---

### Build a DLL and poke it

Nope.

Note: Same problem of building and packaging. Got to duplicate header info in Python.

---

### Use a binding generator

- Sounds groovy! However, there is a slight issue. 

- e.g. `SWIG` interface definition. Duplicates information 
  that is present in the library.

  ```SWIG
  // wibble.i
  enum my_flag {wblWIBBLE = 3, wblWOBBLE = 5};
  ```

Note: Would be nice to automate this if possible.

---

### The `cffi` library

- A [library](https://cffi.readthedocs.io/en/latest/) for producing 
  Python bindings for C libraries without learning a special 
  language (e.g. `SWIG`).
  
- Part of the [pypy](https://pypy.org/features.html) project, a
  faster Python written in Python.
  
- Generates a Python module from snippets of the C declarations
  that you want to expose.

- *Semi-automatic* - you can't just pass it a whole header (d'oh!)

Note: 'cffi' - c foreign function interface.

---

### The `cffi` library

- So, we're stuck pasting in snippets from the header and maintaining
  the thing by hand?

---

### The `cffi` library

- ~~So, we're stuck pasting in snippets from the header and maintaining
  the thing by hand?~~ No!

- Preprocess the header to remove problematic syntax, then 
  feed the whole thing to `cffi`.

- Virtually no maintanance, and easy to build and package!

Note: We only care about one header, not every possible header!

---

### DEMO: `mystery.bif`

Note: see `demo-2.py`.

---

<img src="./images/a-pair-of-pigs.jpg" alt="A pair of pigs" width="500"/>

Unknown, *A Pair of Pigs*, circa 1850, oil on canvas, Compton Verney, Warwickshire
    
---

### A real example: `nuklear-cffi`.

- Benefits of the technique become apparent with ginormous libraries.

- This allowed me to use this GUI library from Python without 
  going insane: https://github.com/vurtun/nuklear

- `nuklear` is an impressive bit of work, it's a platform and render backend
  agnostic immediate-mode GUI library in a single C header.

---

### DEMO: `nuklear-cffi`

Note: See `demo-3.md`.

---

### Conclusion

- The use of `cffi` is not novel. But I've not seen *this
  degree of automation* elsewhere. (Although I didn't look
  that hard and it wouldn't surprise me!)

- Reduced maintanance and build complexity for simple dependencies.

- Allows you to get a complete solution going very quickly.

- At the cost of being a very low-level interface.

---

### Questions
