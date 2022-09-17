from pathlib import Path

import app


def test_command_args_split():
    """
    Test splitting of the --command-args parameter.
    """
    assert app.split_args('convert  %INDIR%/input.jpg    -resize 100x100     %OUTDIR%/output.jpg') == \
        ['convert', '%INDIR%/input.jpg', '-resize', '100x100', '%OUTDIR%/output.jpg']

def test_command_replace_vars():
    """
    Test replacement of INDIR/OUTDIR variables in the --command-args parameter.
    """
    replaced = app.replace_vars_for_values(
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
    app.run_graphicsmagick(['version'])

def test_process_command_args_single():
    """
    Test processing of single/batch command args.
    """
    processed = app.process_command_args(
        'convert %INDIR%/input.jpg -resize 100x100 %OUTDIR%/output.jpg',
        None,
        '/inputdir',
        '/outputdir',
    )
    assert processed == 'convert /inputdir/input.jpg -resize 100x100 /outputdir/output.jpg'

def test_process_command_args_batch():
    """
    Test processing of single/batch command args.
    """
    processed = app.process_command_args(
        None,
        'convert %INDIR%/%FILE% -resize 100x100 %OUTDIR%/%FILE%',
        '/inputdir',
        '/outputdir',
    )
    assert processed == 'convert /inputdir/%FILE% -resize 100x100 /outputdir/%FILE%'

def test_process_file_args():
    """
    Test processing of args per file.
    """
    assert app.process_file_args('asdf %FILE% ghjk', 'myfile.txt') == 'asdf myfile.txt ghjk'
    assert app.process_file_args('asdf %FILEBASE% ghjk', 'myfile.txt') == 'asdf myfile ghjk'
    assert app.process_file_args('asdf %FILEEXT% ghjk', 'myfile.txt') == 'asdf .txt ghjk'
    assert app.process_file_args('asdf %FILEBASE%%FILEEXT% ghjk', 'myfile.txt') == 'asdf myfile.txt ghjk'

def test_list_input_files():
    """
    Test listing the files in the input directory.
    """
    files = app.list_input_files('tests/data')
    assert files == ['tea_estate.jpg', 'tea_plantation.jpg']
