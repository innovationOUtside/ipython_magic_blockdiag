#via https://gist.github.com/sherdim/f0293bc7b022b852185b
"""magics for using blockdiag.com modules with IPython Notebook

The module provides magics:  %%actdiag, %%blockdiag, %%nwdiag, %%seqdiag

Sample usage (in IPython cell):

    %%blockdiag
    {
       A -> B -> C;
            B -> D;
    }

TH: <s>Some browsers do not properly render SVG, therefore PNG image is used by default.</s> Render using SVG by default for higher quality images. Require an appropriate browser.

Use magics %setdiagsvg and %setdiagpng to set SVG or PNG mode

PNG rendered on windows with default libraries does not support antialiasing,
resulting in a poor image quality


TH: Inkscape not required if rendering direct in browser in Jupyter notebook. 
TO DO: Simplify to remove inskcape; update display methods.

If inkscape is installed on the machine and can be found in system path,
the diagram is created as SVG and then rendered to PNG using inkscape.

Inkscape for windows can be downloaded from (http://inkscape.org/)

"""

import imp
import io
import os
import sys
import pipes
import subprocess
import tempfile
from shutil import copyfile

try:
    import hashlib
except ImportError:
    import md5 as hashlib

from IPython.core.magic import Magics, magics_class, cell_magic, line_cell_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.core.displaypub import publish_display_data
from IPython.display import SVG, display

@magics_class
class BlockdiagMagics(Magics):
    """Magics for blockdiag and others"""
    
    def __init__(self, shell):
        super(BlockdiagMagics, self).__init__(shell)
        self._publish_mode='SVG'
        self._publish_mode = self._publish_mode.lower()
    
    #def _import_all(self, module):
    #    for k, v in module.__dict__.items():
    #        if not k.startswith('__'):
    #            self.shell.push({k:v})

    def run_command(self, args, silent_except=False):
        try:
            startupinfo = None
            if os.name == 'nt':
                # Avoid a console window in Microsoft Windows.
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.call(args, stderr=subprocess.STDOUT,
                                  startupinfo=startupinfo)
            return True
        except subprocess.CalledProcessError as e:
            print(e.output, file=sys.stderr)
            print("ERROR: command `%s` failed\n%s" %
                      ' '.join(map(pipes.quote, e.cmd)),
                      file=sys.stderr)
        except OSError as e:
            if not silent_except:
                print ('Exception %s' % str(e), file=sys.stderr)
        return False

    def diag(self, line, cell, command, outfile):
        """Create sequence diagram using supplied diag methods."""
        code = cell + u'\n'
        try:
            tmpdir = tempfile.mkdtemp()
            fd, diag_name = tempfile.mkstemp(dir=tmpdir)
            f = os.fdopen(fd, "wb")
            f.write(code.encode('utf-8'))
            f.close()
            draw_name = diag_name + '.' + self._publish_mode
            args = ['-T', self._publish_mode, '-o', draw_name, diag_name]
            # if os.path.exists(fontpath):
            #    sys.argv += ['-f', fontpath]

            # do not use PIL library when rendering to SVG
            # this allows avoid problem with handling unicode in diagram
            #~ if _draw_mode == 'SVG':
                #~ args += ['--ignore-pil']

            command.main(args=args)

            #file_name = diag_name + '.' + self._publish_mode
            with io.open(draw_name, 'rb') as f:
                data = f.read()
                f.close()

        finally:
            if outfile:
                copyfile(draw_name, outfile)
            for file in os.listdir(tmpdir):
                os.unlink(tmpdir + "/" + file)
            os.rmdir(tmpdir)

        if self._publish_mode == 'svg':
            display(SVG(data))
            #publish_display_data(
                #~ u'IPython.core.displaypub.publish_svg',
            #    {'image/svg+xml':data}
            #)
        else:
            publish_display_data(
                #~ u'IPython.core.displaypub.publish_png',
                {'image/png':data}
            )

    @cell_magic
    @magic_arguments()
    @argument('--outfile', '-o', default='', help='Output file.')
    def actdiag(self, line, cell):
        import actdiag.command
        args = parse_argstring(self.actdiag, line)
        self.diag(line, f'actdiag {{ {cell} }}', actdiag.command, args.outfile)

    @cell_magic
    @magic_arguments()
    @argument('--outfile', '-o', default='', help='Output file.')
    def blockdiag(self, line, cell):
        import blockdiag.command
        args = parse_argstring(self.blockdiag, line)
        self.diag(line, f'blockdiag {{ {cell} }}', blockdiag.command, args.outfile)

    @cell_magic
    @magic_arguments()
    @argument('--outfile', '-o', default='', help='Output file.')
    def nwdiag(self, line, cell):
        import nwdiag.command
        args = parse_argstring(self.nwdiag, line)
        self.diag(line, f'nwdiag {{ {cell} }}', nwdiag.command,  args.outfile)

    @cell_magic
    @magic_arguments()
    @argument('--outfile', '-o', default='', help='Output file.')
    def seqdiag(self, line, cell):
        import seqdiag.command
        args = parse_argstring(self.seqdiag, line)
        self.diag(line, f'seqdiag {{ {cell} }}', seqdiag.command,  args.outfile)

    @cell_magic
    @magic_arguments()
    @argument('--outfile', '-o', default='', help='Output file.')
    def packetdiag(self, line, cell):
        """Depends on nwdiag."""
        import packetdiag.command
        args = parse_argstring(self.seqdiag, line)
        self.diag(line, f'packetdiag {{ {cell} }}', packetdiag.command, args.outfile)

    @cell_magic
    @magic_arguments()
    @argument('--outfile', '-o', default='', help='Output file.')
    def rackdiag(self, line, cell):
        """Depends on nwdiag."""
        import rackdiag.command
        args = parse_argstring(self.rackdiag, line)
        self.diag(line, f'rackdiag {{ {cell} }}', rackdiag.command, args.outfile)
        
    @line_cell_magic
    def setdiagsvg(self, line, cell=None):
        self._publish_mode = 'SVG'.lower()

    @line_cell_magic
    def setdiagpng(self, line, cell=None):
        self._publish_mode = 'PNG'.lower()


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ipython.register_magics(BlockdiagMagics)
    
ip = get_ipython()
ip.register_magics(BlockdiagMagics)
