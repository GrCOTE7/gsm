import json
import os

_LOCALES_DIR = os.path.join(os.path.dirname(__file__), "..", "i18n")
_DEFAULT_LANG = "en"


class I18nService:
    _instance = None
    _strings: dict = {}
    _lang: str = _DEFAULT_LANG

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.set_language(_DEFAULT_LANG)
        return cls._instance

    def set_language(self, lang_code: str):
        path = os.path.join(_LOCALES_DIR, f"{lang_code}.json")
        if not os.path.exists(path):
            lang_code = _DEFAULT_LANG
            path = os.path.join(_LOCALES_DIR, f"{lang_code}.json")
        with open(path, encoding="utf-8") as f:
            self._strings = json.load(f)
        self._lang = lang_code

    def t(self, key: str, **kwargs) -> str:
        text = self._strings.get(key, key)
        return text.format(**kwargs) if kwargs else text

    @property
    def lang(self) -> str:
        return self._lang
