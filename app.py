#!/usr/bin/env python

from chris_plugin import chris_plugin

from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from importlib.metadata import Distribution
from os import listdir
from os import path
from pathlib import Path
import re
import subprocess

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
parser.add_argument('-s', '--single',
                    type=str,
                    default='',
                    help=("Arguments to be passed to 'gm' command, single execution. "
                          "Mutually exclusive with -b."))
parser.add_argument('-b', '--batch',
                    type=str,
                    default='',
                    help=("Arguments to be passed to 'gm' command, executed once per each file in input directory. "
                          "Mutually exclusive with -s."))

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

    processed_args = process_command_args(options.single, options.batch, inputdir, outputdir)

    if options.single:
        run_graphicsmagick(split_args(processed_args))
    else:  # options.batch is truthy
        input_files = list_input_files(inputdir)
        for input_file in input_files:
            file_args = process_file_args(processed_args, input_file)
            run_graphicsmagick(split_args(file_args))

def list_input_files(inputdir):
    return sorted([f for f in listdir(inputdir) if path.isfile(path.join(inputdir, f))])

def process_command_args(single_args, batch_args, inputdir, outputdir):
    if not single_args and not batch_args:
        raise RuntimeError("Either --single or --batch argument must be specified.")
    if single_args and batch_args:
        raise RuntimeError("Arguments --single and --batch are mutually exclusive.")

    vars_values = {
        '%INDIR%': str(inputdir),
        '%OUTDIR%': str(outputdir),
    }
    return replace_vars_for_values(single_args or batch_args, vars_values)

def process_file_args(args, input_file):
    base, ext = path.splitext(input_file)
    vars_values = {
        '%FILE%': input_file,
        '%FILEBASE%': base,
        '%FILEEXT%': ext,
    }
    return replace_vars_for_values(args, vars_values)

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
