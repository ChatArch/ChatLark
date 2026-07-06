import importlib


_LAZY_ATTRS = {
    "LarkBot": ("chatlark.bot", "LarkBot"),
    "MessageContext": ("chatlark.context", "MessageContext"),
    "DocxBlockType": ("chatlark.docx_blocks", "DocxBlockType"),
    "parse_markdown_blocks": ("chatlark.markdown_blocks", "parse_markdown_blocks"),
    "ChatSession": ("chatlark.session", "ChatSession"),
}


def __getattr__(name: str):
    if name == "__version__":
        return __version__
    target = _LAZY_ATTRS.get(name)
    if target is None:
        raise AttributeError(name)
    module_name, attr_name = target
    value = getattr(importlib.import_module(module_name), attr_name)
    globals()[name] = value
    return value


__version__ = "0.1.1"

__all__ = [
    "__version__",
    "LarkBot",
    "MessageContext",
    "ChatSession",
    "DocxBlockType",
    "parse_markdown_blocks",
]
