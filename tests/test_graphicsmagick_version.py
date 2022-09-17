from pathlib import Path

from app import parser, main, DISPLAY_TITLE


def test_graphicsmagick_version(tmp_path: Path):
    """
    Simulated test run of the app.
    """
    inputdir = tmp_path / 'incoming'
    outputdir = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()

    options = parser.parse_args(['-s', 'version'])

    main(options, inputdir, outputdir)

    # TODO: Test that this prints output of calling `gm version`.
