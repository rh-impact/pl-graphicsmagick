from pathlib import Path

from app import parser, main, DISPLAY_TITLE
from os import path
import shutil

INFILE = 'tests/data/tea_estate.jpg'

def test_main(tmp_path: Path):
    """
    Simulated test run of the app.
    """
    inputdir = tmp_path / 'incoming'
    outputdir = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()

    shutil.copyfile(INFILE, inputdir.joinpath('infile.jpg'))

    options = parser.parse_args(['-c', 'convert %INDIR%/infile.jpg -blur 3 -bordercolor black -border 5 %OUTDIR%/outfile.jpg'])
    main(options, inputdir, outputdir)

    assert path.exists(outputdir.joinpath('outfile.jpg'))
