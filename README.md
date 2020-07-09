# ipython_magic_blockdiag
IPython Magic for Displaying blockdiag family of diagrams in Jupyter notebooks

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/innovationOUtside/ipython_magic_blockdiag/master)

```
%load_ext blockdiag_magic
```

By defaul, PNG is generated.

Higher quality SVG is available, but in this magic, this requires inkscape. (The original `blockdiag` package was updated to use imagemagick for SVG rendering so this magic meeds updating to make use of that.)

```
%setdiagsvg
#Reset to png output with: %setdiagpng
```

```
#For inline png - lower quality image if inkscape not available
#%setdiagpng magic
```

```python
%%blockdiag
    {
       A -> B -> C;
            B -> D;
    }
```
