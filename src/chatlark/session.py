"""Per-user LLM conversation session manager for Lark bots.

`ChatSession` intentionally keeps the LLM backend optional so ChatLark can be
used without depending on ChatTool. Pass `chat_factory` for a custom backend, or
install the optional `chatlark[llm]` extra to use ChatTool's `Chat` classes.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional


class ChatSession:
    """
    Per-user conversation session manager.

    Each user identified by ``user_id`` gets an independent chat object so
    conversation history is never shared between users.

    Args:
        system: System prompt shared by all users.
        max_history: Maximum number of dialogue turns to retain per user
            (one turn = one user message + one assistant reply). ``None`` means
            unlimited.
        model: Model name override for the optional ChatTool backend.
        model_type: ``"openai"`` (default) or ``"azure"`` for ChatTool backend.
        chat_factory: Callable returning a chat object with an ``ask(text)``
            method and optional ``_chat_log`` history. Overrides ``model`` and
            ``model_type`` when provided.
    """

    def __init__(
        self,
        system: str = "",
        max_history: Optional[int] = None,
        model: Optional[str] = None,
        model_type: str = "openai",
        chat_factory: Optional[Callable] = None,
    ):
        self.system = system
        self.max_history = max_history
        self.model = model
        self.model_type = model_type
        self._sessions: Dict[str, Any] = {}
        self._factory = chat_factory or self._default_factory

    def _default_factory(self):
        try:
            if self.model_type == "azure":
                from chattool.llm.chattype import AzureChat

                chat = AzureChat(model=self.model) if self.model else AzureChat()
            else:
                from chattool import Chat

                chat = Chat(model=self.model) if self.model else Chat()
        except ImportError as exc:
            raise RuntimeError(
                "ChatSession needs a chat_factory or the optional ChatTool "
                "backend. Install chatlark[llm] or pass chat_factory=."
            ) from exc

        if self.system:
            chat.system(self.system)
        return chat

    def _get_or_create(self, user_id: str):
        if user_id not in self._sessions:
            self._sessions[user_id] = self._factory()
        return self._sessions[user_id]

    def _trim_history(self, chat) -> None:
        """Trim the internal chat log to at most ``max_history`` turns."""
        if self.max_history is None or not hasattr(chat, "_chat_log"):
            return
        log = chat._chat_log
        max_msgs = 1 + self.max_history * 2
        if len(log) > max_msgs:
            chat._chat_log = log[:1] + log[-(max_msgs - 1):]

    def chat(self, user_id: str, text: str) -> str:
        """Send text to the user's conversation and return the assistant reply."""
        chat = self._get_or_create(user_id)
        self._trim_history(chat)
        return chat.ask(text)

    def clear(self, user_id: str) -> None:
        """Delete the conversation history for a user."""
        self._sessions.pop(user_id, None)

    def clear_all(self) -> None:
        """Delete conversation histories for all users."""
        self._sessions.clear()

    def user_count(self) -> int:
        """Return the number of active user sessions."""
        return len(self._sessions)

    def has_session(self, user_id: str) -> bool:
        """Return True if a user has an active session."""
        return user_id in self._sessions
