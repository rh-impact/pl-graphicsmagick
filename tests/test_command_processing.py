from pathlib import Path

from app import split_args


def test_command_args_split():
    """
    Test splitting of the --command-args parameter.
    """
    assert split_args('convert  %INDIR%/input.jpg    -resize 100x100     %OUTDIR%/output.jpg') == \
        ['convert', '%INDIR%/input.jpg', '-resize', '100x100', '%OUTDIR%/output.jpg']
