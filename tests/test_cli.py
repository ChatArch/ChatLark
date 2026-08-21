from pathlib import Path

from click.testing import CliRunner

from chatlark import __version__
from chatlark.cli import _load_runtime_env, main
from chatlark.config import FeishuConfig, get_env_store
from chatlark.serve import serve


def test_version_option_reports_package_version():
    result = CliRunner().invoke(main, ["--version"])

    assert result.exit_code == 0
    assert f"chatlark, version {__version__}" in result.output


def test_top_level_help_lists_tree_and_non_model_commands_only():
    result = CliRunner().invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "--tree" in result.output
    assert "--tree-brief" in result.output
    assert "info" in result.output
    assert "send" in result.output
    assert "serve" in result.output
    assert "chat" not in main.commands


def test_tree_renders_the_registered_command_surface_with_signatures():
    result = CliRunner().invoke(main, ["--tree"])

    assert result.exit_code == 0, result.output
    assert result.output.splitlines()[0] == "chatlark"
    assert "--version  # Show the version and exit." in result.output
    assert "--tree  # Print the registered CLI tree and exit." in result.output
    assert (
        "--tree-brief  # Print the registered CLI tree without parameter signatures and exit."
        in result.output
    )
    assert "info" in result.output
    assert "[--env ENV-REF]" in result.output
    assert "send" in result.output
    assert "[RECEIVER]" in result.output
    assert "[TEXT]" in result.output
    assert "[--type ID-TYPE]" in result.output
    assert "serve" in result.output
    assert "echo" in result.output
    assert "[--mode MODE]" in result.output
    assert "webhook" in result.output
    assert "[--verification-token VERIFICATION-TOKEN]" in result.output


def test_tree_brief_keeps_nodes_and_descriptions_but_omits_signatures():
    full = CliRunner().invoke(main, ["--tree"])
    brief = CliRunner().invoke(main, ["--tree-brief"])

    assert full.exit_code == 0, full.output
    assert brief.exit_code == 0, brief.output
    assert brief.output.splitlines()[0] == "chatlark"
    for description in (
        "Read bot metadata and validate credentials without printing secrets.",
        "Send one remote text message and print its message ID, never credentials.",
        "Run long-lived Lark bot network services.",
        "Run an echo bot that receives and replies to remote messages.",
        "Run a webhook verifier without printing token values.",
    ):
        assert description in full.output
        assert description in brief.output
    assert "[RECEIVER]" in full.output
    assert "[--env ENV-REF]" in full.output
    assert "[RECEIVER]" not in brief.output
    assert "[--env ENV-REF]" not in brief.output
    assert "[--mode MODE]" not in brief.output


def test_tree_root_uses_public_console_command_in_module_mode():
    result = CliRunner().invoke(main, ["--tree"], prog_name="python -m chatlark.cli")

    assert result.exit_code == 0, result.output
    assert result.output.splitlines()[0] == "chatlark"
    assert "python -m chatlark.cli" not in result.output


def test_bilingual_readmes_embed_the_registered_full_tree():
    result = CliRunner().invoke(main, ["--tree"])

    assert result.exit_code == 0, result.output
    documented_tree = f"```text\n{result.output.rstrip()}\n```"
    for readme in (Path("README.md"), Path("README.en.md")):
        assert documented_tree in readme.read_text(encoding="utf-8")


def test_serve_help_lists_non_model_commands_only():
    result = CliRunner().invoke(main, ["serve", "--help"])

    assert result.exit_code == 0
    assert "echo" in result.output
    assert "webhook" in result.output
    assert "ai" not in serve.commands


def test_named_chatenv_profile_is_typed_and_isolated(
    monkeypatch,
    tmp_path,
):
    fields = FeishuConfig.get_fields()
    original_values = {name: field.value for name, field in fields.items()}
    monkeypatch.setenv("CHATARCH_HOME", str(tmp_path))
    monkeypatch.setenv("FEISHU_APP_ID", "process-app")
    monkeypatch.setenv("FEISHU_APP_SECRET", "process-secret")
    monkeypatch.setenv("FEISHU_VERIFY_TOKEN", "process-token")
    store = get_env_store()
    profile_path = store.save_profile(
        FeishuConfig,
        "work",
        {
            "FEISHU_APP_ID": "profile-app",
            "FEISHU_APP_SECRET": "profile-secret",
        },
    )

    try:
        loaded_path = _load_runtime_env("work")

        assert loaded_path == profile_path
        assert FeishuConfig.FEISHU_APP_ID.value == "profile-app"
        assert FeishuConfig.FEISHU_APP_SECRET.value == "profile-secret"
        assert FeishuConfig.FEISHU_VERIFY_TOKEN.value == ""
    finally:
        for name, value in original_values.items():
            fields[name].value = value
