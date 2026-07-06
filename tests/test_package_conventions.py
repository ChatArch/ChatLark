import importlib.metadata

from chatlark.bot import LarkBot
from chatlark.config import FeishuConfig, get_env_root


EXPECTED_LARKBOT_METHODS = {
    "add_tasklist_members",
    "append_doc_blocks",
    "append_doc_blocks_safe",
    "append_doc_text",
    "append_doc_texts",
    "append_doc_texts_safe",
    "batch_create_bitable_records",
    "card_action",
    "command",
    "create_bitable_app",
    "create_bitable_field",
    "create_bitable_record",
    "create_bitable_table",
    "create_calendar_event",
    "create_doc_document",
    "create_doc_permission_member",
    "create_task",
    "create_tasklist",
    "get_bot_info",
    "get_calendar_event",
    "get_chat_info",
    "get_chat_members",
    "get_doc_block_children",
    "get_doc_document",
    "get_doc_meta",
    "get_doc_public_permission",
    "get_doc_raw_content",
    "get_event_dispatcher",
    "get_message",
    "get_message_resource",
    "get_primary_calendar",
    "get_scopes",
    "get_task",
    "get_tasklist",
    "list_bitable_fields",
    "list_bitable_records",
    "list_bitable_tables",
    "list_calendar_events",
    "list_calendars",
    "list_doc_permission_members",
    "list_freebusy",
    "list_messages",
    "list_tasklist_tasks",
    "list_tasklists",
    "list_tasks",
    "on_bot_added",
    "on_message",
    "patch_calendar_event",
    "patch_doc_public_permission",
    "patch_task",
    "regex",
    "reply",
    "reply_calendar_event",
    "reply_card",
    "send_card",
    "send_file",
    "send_image",
    "send_image_file",
    "send_message",
    "send_post",
    "send_text",
    "start",
    "start_background",
    "upload_file",
    "upload_image",
}


def test_larkbot_migrated_non_model_method_surface():
    public_methods = {
        name
        for name, value in vars(LarkBot).items()
        if callable(value) and not name.startswith("_")
    }

    assert EXPECTED_LARKBOT_METHODS <= public_methods


def test_base_package_has_no_chattool_dependency():
    requirements = importlib.metadata.requires("ChatLark") or []

    assert not any(req.lower().startswith("chattool") for req in requirements)


def test_chatenv_feishu_config_is_reused():
    assert FeishuConfig.FEISHU_APP_SECRET.is_sensitive is True
    assert get_env_root().name == "envs"
