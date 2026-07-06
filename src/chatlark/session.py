"""Per-user conversation session manager for Lark bots.

`ChatSession` intentionally requires a caller-provided backend factory. This
keeps ChatLark decoupled from ChatTool and other model runtimes while preserving
the reusable per-user session container migrated from ChatTool.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional


class ChatSession:
    """
    Per-user conversation session manager.

    Each user identified by ``user_id`` gets an independent chat object so
    conversation history is never shared between users.

    Args:
        system: System prompt metadata retained for caller-created backends.
        max_history: Maximum number of dialogue turns to retain per user
            (one turn = one user message + one assistant reply). ``None`` means
            unlimited.
        model: Model metadata retained for caller-created backends.
        model_type: Model backend metadata retained for caller-created backends.
        chat_factory: Callable returning a chat object with an ``ask(text)``
            method and optional ``_chat_log`` history.
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
        self._factory = chat_factory

    def _default_factory(self):
        raise RuntimeError(
            "ChatSession requires chat_factory in ChatLark. "
            "Model-backed ChatTool integration is intentionally skipped in this package."
        )

    def _get_or_create(self, user_id: str):
        if user_id not in self._sessions:
            factory = self._factory or self._default_factory
            self._sessions[user_id] = factory()
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
