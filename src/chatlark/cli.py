"""ChatLark CLI."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from chatstyle import add_tree_option

from chatlark import __version__
from chatlark.config import FeishuConfig, get_env_root, get_env_store


@click.group(name="chatlark")
@click.version_option(__version__, prog_name="chatlark")
@add_tree_option(renderer_options={"root_name": "chatlark"})
def main() -> None:
    """Opinionated ChatArch helpers for Feishu/Lark bots."""
    _load_runtime_env(None)


def _resolve_env_path(env_ref: str) -> Path:
    candidate = Path(env_ref).expanduser()
    if candidate.is_file():
        return candidate

    profile_path = get_env_store().profile_path(FeishuConfig, env_ref)
    if profile_path.exists():
        return profile_path

    raise click.ClickException(
        f"未找到配置文件: {env_ref}。可传入 .env 文件路径，或 Feishu 类型下保存的 profile 名称。"
    )


def _load_runtime_env(env_ref: str | None) -> Path | None:
    store = get_env_store()
    if env_ref:
        env_path = _resolve_env_path(env_ref)
        values = store.load_path(env_path)
        values = {
            field.env_key: values.get(
                field.env_key,
                field.default if field.default is not None else "",
            )
            for field in FeishuConfig.get_fields().values()
        }
    else:
        env_path = store.active_path(FeishuConfig)
        values = store.load_active(FeishuConfig)

    FeishuConfig.load_from_sources(env_values=values)
    return env_path if env_path.is_file() else None


def _get_bot():
    from chatlark.bot import LarkBot

    try:
        return LarkBot()
    except Exception as exc:
        click.secho(f"初始化失败: {exc}", fg="red", err=True)
        click.echo(
            "请确认已设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET，"
            f"或通过 -e/--env 指定配置文件（默认读取 {get_env_root() / FeishuConfig.get_storage_name() / '.env'}）。",
            err=True,
        )
        sys.exit(1)


def _default_target_env_name(id_type: str) -> str:
    if id_type == "chat_id":
        return "FEISHU_DEFAULT_CHAT_ID"
    return "FEISHU_DEFAULT_RECEIVER_ID"


def _default_target_value(id_type: str) -> str | None:
    if id_type == "chat_id":
        return FeishuConfig.FEISHU_DEFAULT_CHAT_ID.value or None
    return FeishuConfig.FEISHU_DEFAULT_RECEIVER_ID.value or None


def _resolve_text_target(
    receiver: str | None,
    text: str | None,
    id_type: str,
) -> tuple[str | None, str | None]:
    default_receiver = _default_target_value(id_type)

    if receiver and text:
        return receiver, text
    if receiver and not text and default_receiver:
        return default_receiver, receiver
    if not receiver and text and default_receiver:
        return default_receiver, text
    return receiver, text


@main.command()
@click.option(
    "--env",
    "-e",
    "env_ref",
    default=None,
    help="从指定 .env 文件或已保存 profile 读取配置",
)
def info(env_ref):
    """Read bot metadata and validate credentials without printing secrets."""
    _load_runtime_env(env_ref)
    bot = _get_bot()
    resp = bot.get_bot_info()

    if resp.code != 0:
        click.secho(f"请求失败: code={resp.code}", fg="red")
        return

    data = json.loads(resp.raw.content).get("bot", {})
    status_map = {1: "未激活", 2: "已激活", 3: "已停用"}
    status = status_map.get(data.get("activate_status"), "未知")
    click.echo(f"名称      : {data.get('app_name', '—')}")
    click.echo(f"Open ID   : {data.get('open_id', '—')}")
    click.echo(f"激活状态  : {status}")


@main.command()
@click.argument("receiver", required=False)
@click.argument("text", required=False, default="")
@click.option(
    "--env",
    "-e",
    "env_ref",
    default=None,
    help="从指定 .env 文件或已保存 profile 读取配置",
)
@click.option(
    "--type",
    "-t",
    "id_type",
    default="user_id",
    type=click.Choice(["open_id", "user_id", "union_id", "email", "chat_id"]),
    help="接收者 ID 类型 (默认 user_id)",
)
def send(receiver, text, env_ref, id_type):
    """Send one remote text message and print its message ID, never credentials.

    示例:
      chatlark send "你好"
      chatlark send f25gc16d "你好"
      chatlark send oc_xxx "群通知" -t chat_id
      chatlark send -t chat_id "群通知"
    """
    _load_runtime_env(env_ref)
    bot = _get_bot()
    default_target_env = _default_target_env_name(id_type)
    receiver, text = _resolve_text_target(receiver, text, id_type)

    if receiver and not text:
        click.secho(
            f"单参数形式需要先配置 {default_target_env}；否则请显式传入 receiver 和 text",
            fg="red",
        )
        return
    if not receiver:
        click.secho(
            f"请指定接收者，或先配置 {default_target_env} 作为默认发送目标", fg="red"
        )
        return
    if not text:
        click.secho("请提供文本消息内容", fg="red")
        return

    resp = bot.send_text(receiver, id_type, text)
    if resp.success():
        click.secho(
            f"文本消息发送成功  message_id={resp.data.message_id}", fg="green"
        )
        return

    click.secho(f"发送失败: code={resp.code}  msg={resp.msg}", fg="red")
    if resp.code == 99991663:
        click.echo("  -> 提示: 用户不在应用可见范围内")


from chatlark.serve import serve  # noqa: E402

main.add_command(serve)


if __name__ == "__main__":
    main()
