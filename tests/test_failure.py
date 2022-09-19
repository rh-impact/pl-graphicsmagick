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
        assert False, "GraphicsMagick should have failed but it didn't."
    except subprocess.CalledProcessError:
        pass

def test_no_single_nor_batch_specified(tmp_path: Path):
    inputdir = tmp_path / 'incoming'
    outputdir = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()

    options = parser.parse_args([])
    try:
        main(options, inputdir, outputdir)
        assert False, "chris-gm should have failed but it didn't."
    except RuntimeError:
        pass

def test_both_single_and_batch_specified(tmp_path: Path):
    inputdir = tmp_path / 'incoming'
    outputdir = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()

    options = parser.parse_args(['-s', 'asdf', '-b', 'ghkl'])
    try:
        main(options, inputdir, outputdir)
        assert False, "chris-gm should have failed but it didn't."
    except RuntimeError:
        pass
