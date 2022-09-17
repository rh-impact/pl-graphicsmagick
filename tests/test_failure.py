from pathlib import Path

from app import parser, main, DISPLAY_TITLE
from os import path
import shutil
import subprocess

INFILE = 'tests/data/tea_estate.jpg'

def test_malformed_command(tmp_path: Path):
    """
    Simulated test run of the app.
    """
    inputdir = tmp_path / 'incoming'
    outputdir = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()

    shutil.copyfile(INFILE, inputdir.joinpath('infile.jpg'))

    # fakecolor is not a color, GraphicsMagick should fail
    options = parser.parse_args(['-s', 'convert %INDIR%/infile.jpg -bordercolor boguscolor -border 5 %OUTDIR%/outfile.jpg'])
    try:
        main(options, inputdir, outputdir)
        assert false, "GraphicsMagick should have failed but it didn't."
    except subprocess.CalledProcessError:
        pass
