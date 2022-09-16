#!/usr/bin/env python

from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from importlib.metadata import Distribution
from pathlib import Path
import re
import subprocess

from chris_plugin import chris_plugin

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version


DISPLAY_TITLE = r"""
GraphicsMagick ChRIS plugin
"""


parser = ArgumentParser(description='cli description',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')

# Originally i wanted simple pass-through args at the end of the
# command line, but the @chris_plugin decorator automatically adds
# inputdir and outputdir arguments at the end. So the way to make
# pass-through arguments work with ChRIS is probably to have them all
# as a single argument, and then split them by whitespace when passing
# them to the 'gm' command.
parser.add_argument('-c', '--command-args',
                    type=str,
                    required=True,
                    help="arguments to be passed to the 'gm' command")

# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser=parser,
    title='GraphicsMagick ChRIS plugin',
    category='Image Processing', # ref. https://chrisstore.co/plugins
    min_memory_limit='100Mi',    # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE)

    raw_args = options.command_args
    vars_values = {
        '%INDIR%': str(inputdir),
        '%OUTDIR%': str(outputdir),
    }
    processed_args = split_args(replace_vars_for_values(raw_args, vars_values))
    run_graphicsmagick(processed_args)

def replace_vars_for_values(args_str, vars_values):
    replaced = args_str
    for var, value in vars_values.items():
        replaced = replaced.replace(var, value)
    return replaced

def split_args(args_str):
    args_singlespace = re.sub(' +', ' ', args_str)
    return args_singlespace.split(' ')

def run_graphicsmagick(args):
    cmd = ['/usr/bin/gm']
    cmd.extend(args)
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == '__main__':
    main()
