# ipython_magic_blockdiag
IPython Magic for Displaying blockdiag family of diagrams in Jupyter notebooks

```
%load_ext blockdiag_magic
```

By defaul, SVG is generated, but this requires inkscape. To render the original png:

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
