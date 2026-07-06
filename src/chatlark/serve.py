"""ChatLark bot service commands."""

from __future__ import annotations

import sys

import click

from chatlark.bot import LarkBot

LOG_LEVELS = click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False)


def _get_bot():
    try:
        return LarkBot()
    except Exception as exc:
        click.echo(f"初始化失败: {exc}", err=True)
        click.echo("请确认已设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET 环境变量", err=True)
        sys.exit(1)


@click.group()
def serve():
    """Run Lark bot services."""


@serve.command()
@click.option(
    "--mode",
    "-m",
    default="ws",
    type=click.Choice(["ws", "flask"]),
    help="运行模式: ws (WebSocket) 或 flask (Webhook)",
)
@click.option("--host", default="0.0.0.0", help="Flask 监听地址 (仅 flask 模式)")
@click.option("--port", "-p", default=7777, type=int, help="Flask 监听端口 (仅 flask 模式)")
@click.option("--log-level", "-l", default="INFO", type=LOG_LEVELS, help="日志级别 (默认 INFO)")
def echo(mode, host, port, log_level):
    """Start an echo bot that replies with the received text."""
    bot = _get_bot()

    @bot.on_message
    def handle(ctx):
        ctx.reply(f"Echo: {ctx.text}")

    click.secho(f"回显机器人启动  mode={mode}  log_level={log_level}", fg="green")
    _start(bot, mode, host, port, log_level)


@serve.command()
@click.option("--host", default="0.0.0.0", help="监听地址")
@click.option("--port", "-p", default=7777, type=int, help="监听端口")
@click.option("--path", default="/webhook/event", help="Webhook 路径")
@click.option("--log-level", "-l", default="INFO", type=LOG_LEVELS, help="日志级别 (默认 INFO)")
@click.option("--encrypt-key", default="", help="事件加密 Key")
@click.option("--verification-token", default="", help="验证 Token")
def webhook(host, port, path, log_level, encrypt_key, verification_token):
    """Start an empty webhook server for platform URL verification."""
    bot = _get_bot()
    click.secho(f"Webhook 服务启动  http://{host}:{port}{path}  log_level={log_level}", fg="green")
    bot.start(
        mode="flask",
        encrypt_key=encrypt_key,
        verification_token=verification_token,
        host=host,
        port=port,
        path=path,
        log_level=log_level,
    )


def _start(bot, mode, host, port, log_level="INFO"):
    try:
        if mode == "ws":
            bot.start(mode="ws", log_level=log_level)
        else:
            bot.start(mode="flask", host=host, port=port, log_level=log_level)
    except KeyboardInterrupt:
        click.echo("\n已停止")
