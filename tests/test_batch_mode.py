from pathlib import Path

from app import parser, main, DISPLAY_TITLE
from os import path
import shutil

TEST_FILES_DIR = 'tests/data'
FILES = ['tea_estate.jpg', 'tea_plantation.jpg']
FILES_AS_PNG = ['tea_estate.png', 'tea_plantation.png']

def test_batch_image_operation(tmp_path: Path):
    """
    Simulated test run of the app.
    """
    inputdir = tmp_path / 'incoming'
    outputdir = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()

    for f in FILES:
        shutil.copyfile(path.join(TEST_FILES_DIR, f), inputdir.joinpath(f))

    options = parser.parse_args(['-b', 'convert %INDIR%/%FILE% -blur 3 -bordercolor black -border 5 %OUTDIR%/%FILE%'])
    main(options, inputdir, outputdir)

    for f in FILES:
        assert path.exists(outputdir.joinpath(f))

def test_batch_format_conversion(tmp_path: Path):
    """
    Simulated test run of the app.
    """
    inputdir = tmp_path / 'incoming'
    outputdir = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()

    for f in FILES:
        shutil.copyfile(path.join(TEST_FILES_DIR, f), inputdir.joinpath(f))

    options = parser.parse_args(['-b', 'convert %INDIR%/%FILE% %OUTDIR%/%FILEBASE%.png'])
    main(options, inputdir, outputdir)

    for f in FILES_AS_PNG:
        assert path.exists(outputdir.joinpath(f))
