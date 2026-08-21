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

ChatArch 的 Feishu/Lark bot helper 包，承接从 ChatTool 拆出的轻量机器人、消息发送、事件服务和消息内容构造能力。更广泛的 Feishu/Lark OpenAPI 操作仍优先使用官方 `lark-cli`。

## 快速开始

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
chatlark send "Hello"                  # 使用 FEISHU_DEFAULT_RECEIVER_ID
chatlark send -t chat_id "Hello team" # 使用 FEISHU_DEFAULT_CHAT_ID
chatlark serve echo
chatlark serve webhook
```

模型调用相关命令暂不放入 ChatLark 的默认命令面；需要模型 backend 的 bot 编排会在后续单独设计，避免重新引入 ChatTool 或其他 LLM runtime 硬依赖。

## CLI 树

`chatlark --tree` 由 ChatStyle 从真实 Click registry 渲染，并保留参数签名：

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

`chatlark --tree-brief` 保留同一组节点和说明，但省略参数签名。

| Leaf | 主要输入 | 输出 | 副作用与边界 |
|---|---|---|---|
| `chatlark info` | 可选 Feishu profile 或 `.env` | bot 名称、Open ID、状态 | 只读远程请求；不输出凭据 |
| `chatlark send` | receiver、text、ID type、可选配置 | `message_id` 或错误码 | 发送一条远程消息；不输出凭据 |
| `chatlark serve echo` | mode、host、port、log level | 长期运行日志 | 接收并回复消息；不输出凭据 |
| `chatlark serve webhook` | listener 与 webhook 参数 | 长期运行日志 | 启动监听服务；不输出 token 值 |

## Python API

```python
from chatlark import LarkBot, ChatSession

bot = LarkBot()
session = ChatSession(system="你是助手")

@bot.on_message
def chat(ctx):
    ctx.reply(session.chat(ctx.sender_id, ctx.text))

bot.start()
```

## 配置

ChatLark 复用 ChatEnv 的 Feishu 配置字段：

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_API_BASE`
- `FEISHU_DEFAULT_RECEIVER_ID`
- `FEISHU_DEFAULT_CHAT_ID`

默认从 ChatEnv active Feishu profile（`$CHATARCH_HOME/envs/Feishu/.env`）读取，并回退到进程环境变量。`info` 和 `send` 也可通过 `-e/--env` 指定 ChatEnv Feishu profile 名称或显式 `.env` 文件；命名 profile 由 ChatEnv `EnvStore` 解析，且不会被全局激活。

## 边界

- ChatLark：bot helper、消息发送、事件服务、消息上下文、消息内容构造。
- lark-cli：广泛 Feishu/Lark OpenAPI 操作和用户授权流程。
- ChatTool：迁移完成后只应保留有意设计的兼容入口或依赖连接，不再重复持有 Lark business logic。

## 开发说明

扩展前先阅读 `DEVELOP.md` 和 `AGENTS.md`。发布走 PyPI Trusted Publisher/OIDC workflow，不使用本地 token 上传正式版本。
