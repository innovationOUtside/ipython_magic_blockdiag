
from setuptools import setup

setup(name='blockdiagMagic',
      packages=['blockdiag_magic'],
      install_requires=['blockdiag', 'seqdiag', 'nwdiag', 'actdiag']
#also support a ipython_magic_blockdiag[svg] opton that installs Wand as well
     )
