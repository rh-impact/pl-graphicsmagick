from pathlib import Path

from app import parser, main, DISPLAY_TITLE


def test_main(tmp_path: Path):
    """
    Simulated test run of the app.
    """
    inputdir = tmp_path / 'incoming'
    outputdir = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()

    options = parser.parse_args(['--name', 'bar'])

    main(options, inputdir, outputdir)

    expected_output_file = outputdir / 'bar.txt'
    assert expected_output_file.exists()
    assert expected_output_file.read_text() == 'did nothing successfully!'
