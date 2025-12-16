import gettext

_current_lang = None
_ = lambda s: s  # 預設直接回傳原字串

def set_language(lang: str):
    global _, _current_lang  # ⚠️ 一定要加 global
    if lang == _current_lang:
        return

    t = gettext.translation(
        "messages",
        localedir="locales",
        languages=[lang],
        fallback=True
    )
    _ = t.gettext
    _current_lang = lang

def tr(key: str) -> str:
    return _(key)
