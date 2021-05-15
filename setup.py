
from setuptools import setup

setup(name='blockdiagMagic',
      author="Tony Hirst",
     author_email="tony.hirst@gmail.com",
     description="IPython magics for rendering blockdiag family diagrams.",
     long_description='''
    A collection of IPython cell magics for creating blockdiag, nwdiag and actdiag diagrams inline in Jupyter notebooks.
    ''',
     long_description_content_type="text/markdown",
     packages=['blockdiag_magic'],
     install_requires=['blockdiag', 'seqdiag', 'nwdiag', 'actdiag'],
     version='0.0.3'
      
     )
