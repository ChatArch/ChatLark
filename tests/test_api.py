from chatlark.bot import LarkBot
from chatlark.context import MessageContext
from chatlark.docx_blocks import DocxBlockType
from chatlark.elements import TextMessage
from chatlark.markdown_blocks import parse_markdown_blocks
from chatlark.session import ChatSession


def test_public_api_modules_expose_migrated_lark_helpers():
    assert LarkBot.__name__ == "LarkBot"
    assert MessageContext.__name__ == "MessageContext"
    assert ChatSession.__name__ == "ChatSession"
    assert DocxBlockType.TEXT.value == 2
    assert callable(parse_markdown_blocks)


def test_text_message_serializes_to_lark_payload():
    assert TextMessage("hello").to_json() == '{"text": "hello"}'


def test_chat_session_accepts_custom_factory():
    class FakeChat:
        def __init__(self):
            self._chat_log = ["system"]

        def ask(self, text):
            self._chat_log.extend([text, "ok"])
            return f"reply:{text}"

    session = ChatSession(chat_factory=FakeChat, max_history=1)

    assert session.chat("u1", "hello") == "reply:hello"
    assert session.has_session("u1")
    assert session.user_count() == 1
    session.clear("u1")
    assert not session.has_session("u1")
