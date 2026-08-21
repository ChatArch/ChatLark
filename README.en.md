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
chatlark --tree
chatlark --tree-brief
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

Model-calling commands are intentionally outside ChatLark's default command surface for now. Model-backed bot orchestration will be designed separately so ChatLark does not regain a hard dependency on ChatTool or another LLM runtime.

## CLI tree

`chatlark --tree` is rendered by ChatStyle from the real Click registry and keeps parameter signatures:

```text
chatlark
├── --help  # Show this message and exit.
├── --version  # Show the version and exit.
├── --tree  # Print the registered CLI tree and exit.
├── --tree-brief  # Print the registered CLI tree without parameter signatures and exit.
├── info [--env ENV-REF]  # Read bot metadata and validate credentials without printing secrets.
├── send [RECEIVER] [TEXT] [--env ENV-REF] [--type ID-TYPE]  # Send one remote text message and print its message ID, never credentials.
└── serve  # Run long-lived Lark bot network services.
    ├── echo [--mode MODE] [--host HOST] [--port PORT] [--log-level LOG-LEVEL]  # Run an echo bot that receives and replies to remote messages.
    └── webhook [--host HOST] [--port PORT] [--path PATH] [--log-level LOG-LEVEL] [--encrypt-key ENCRYPT-KEY] [--verification-token VERIFICATION-TOKEN]  # Run a webhook verifier without printing token values.
```

`chatlark --tree-brief` keeps the same nodes and descriptions while omitting parameter signatures.

| Leaf | Main inputs | Output | Side effects and boundary |
|---|---|---|---|
| `chatlark info` | optional Feishu profile or `.env` | bot name, Open ID, status | read-only remote request; never prints credentials |
| `chatlark send` | receiver, text, ID type, optional config | `message_id` or error code | sends one remote message; never prints credentials |
| `chatlark serve echo` | mode, host, port, log level | long-running logs | receives and replies to messages; never prints credentials |
| `chatlark serve webhook` | listener and webhook parameters | long-running logs | starts a listener; never prints token values |

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

By default ChatLark reads the active ChatEnv Feishu profile (`$CHATARCH_HOME/envs/Feishu/.env`) and falls back to process environment variables. `info` and `send` also accept `-e/--env` with a named ChatEnv Feishu profile or an explicit `.env` file; named profiles are resolved through ChatEnv `EnvStore` without global activation.

## Boundary

- ChatLark: bot helpers, message sending, event services, message contexts, and message payload builders.
- lark-cli: broad Feishu/Lark OpenAPI operations and user authorization flows.
- ChatTool: after migration, should keep only deliberate compatibility entry points or dependency wiring, not duplicate Lark business logic.

## Development

Read `DEVELOP.md` and `AGENTS.md` before extending the package. Releases use PyPI Trusted Publisher/OIDC workflow, not local token uploads for real versions.
