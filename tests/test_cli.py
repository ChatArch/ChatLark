from click.testing import CliRunner

from chatlark import __version__
from chatlark.cli import main


def test_version_option_reports_package_version():
    result = CliRunner().invoke(main, ["--version"])

    assert result.exit_code == 0
    assert f"chatlark, version {__version__}" in result.output


def test_top_level_help_lists_migrated_commands():
    result = CliRunner().invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "info" in result.output
    assert "send" in result.output
    assert "chat" in result.output
    assert "serve" in result.output


def test_serve_help_lists_migrated_commands():
    result = CliRunner().invoke(main, ["serve", "--help"])

    assert result.exit_code == 0
    assert "echo" in result.output
    assert "ai" in result.output
    assert "webhook" in result.output
