from pathlib import Path

from app import replace_vars_for_values, run_graphicsmagick, split_args


def test_command_args_split():
    """
    Test splitting of the --command-args parameter.
    """
    assert split_args('convert  %INDIR%/input.jpg    -resize 100x100     %OUTDIR%/output.jpg') == \
        ['convert', '%INDIR%/input.jpg', '-resize', '100x100', '%OUTDIR%/output.jpg']

def test_command_replace_vars():
    """
    Test replacement of INDIR/OUTDIR variables in the --command-args parameter.
    """
    replaced = replace_vars_for_values(
        'convert %INDIR%/input.jpg -resize 100x100 %OUTDIR%/output.jpg',
        {
            '%INDIR%': '/inputdir',
            '%OUTDIR%': '/outputdir',
        },
    )
    assert replaced == 'convert /inputdir/input.jpg -resize 100x100 /outputdir/output.jpg'

def test_run_graphicsmagick():
    """
    Test running of GraphicsMagick command.
    """
    run_graphicsmagick(['version'])
