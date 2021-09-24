"""Blockdiag magics"""
__version__ = '0.0.2'

from .blockdiag import BlockdiagMagics

def load_ipython_extension(ipython):
    ipython.register_magics(BlockdiagMagics)
