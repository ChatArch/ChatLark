from click.testing import CliRunner

from chatlark import __version__
from chatlark.cli import main
from chatlark.serve import serve


def test_version_option_reports_package_version():
    result = CliRunner().invoke(main, ["--version"])

    assert result.exit_code == 0
    assert f"chatlark, version {__version__}" in result.output


def test_top_level_help_lists_non_model_commands_only():
    result = CliRunner().invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "info" in result.output
    assert "send" in result.output
    assert "serve" in result.output
    assert "chat" not in main.commands


def test_serve_help_lists_non_model_commands_only():
    result = CliRunner().invoke(main, ["serve", "--help"])

    assert result.exit_code == 0
    assert "echo" in result.output
    assert "webhook" in result.output
    assert "ai" not in serve.commands
