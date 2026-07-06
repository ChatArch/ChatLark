<div align="center">
    <a href="https://pypi.python.org/pypi/ChatLark">
        <img src="https://img.shields.io/pypi/v/ChatLark.svg" alt="PyPI version" />
    </a>
    <a href="https://github.com/ChatArch/ChatLark/actions/workflows/ci.yml">
        <img src="https://github.com/ChatArch/ChatLark/actions/workflows/ci.yml/badge.svg" alt="Tests" />
    </a>
</div>

<div align="center">

[English](README.en.md) | [简体中文](README.md)
</div>

# ChatLark

ChatArch Feishu/Lark bot helpers extracted from ChatTool. ChatLark owns lightweight bot helpers, message sending, event services, and message payload builders. Broad Feishu/Lark OpenAPI operations should still use the official `lark-cli`.

## Quick Start

```bash
pip install -e ".[dev]"
chatlark --help
chatlark --version
chatlark send --help
chatlark serve --help
python -m pytest -q
python -m build
```

## CLI

```bash
chatlark info
chatlark send USER_ID "Hello"
chatlark send "Hello"                  # Uses FEISHU_DEFAULT_RECEIVER_ID
chatlark send -t chat_id "Hello team" # Uses FEISHU_DEFAULT_CHAT_ID
chatlark serve echo
chatlark serve webhook
```

AI chat remains optional to avoid making the base ChatLark package depend on ChatTool:

```bash
pip install "chatlark[llm]"
chatlark chat
chatlark serve ai --system "You are a concise work assistant"
```

## Python API

```python
from chatlark import LarkBot, ChatSession

bot = LarkBot()
session = ChatSession(system="You are an assistant")

@bot.on_message
def chat(ctx):
    ctx.reply(session.chat(ctx.sender_id, ctx.text))

bot.start()
```

## Configuration

ChatLark reuses ChatEnv's Feishu configuration fields:

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_API_BASE`
- `FEISHU_DEFAULT_RECEIVER_ID`
- `FEISHU_DEFAULT_CHAT_ID`

Provide them as environment variables, or pass `-e/--env` with a ChatEnv Feishu profile name or `.env` file.

## Boundary

- ChatLark: bot helpers, message sending, event services, message contexts, and message payload builders.
- lark-cli: broad Feishu/Lark OpenAPI operations and user authorization flows.
- ChatTool: after migration, should keep only deliberate compatibility entry points or dependency wiring, not duplicate Lark business logic.

## Development

Read `DEVELOP.md` and `AGENTS.md` before extending the package. Releases use PyPI Trusted Publisher/OIDC workflow, not local token uploads for real versions.
