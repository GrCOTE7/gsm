from ..helpers.env import is_dev_env


class AppWindow:
    """Construit le titre de l'onglet selon l'environnement et la page active."""

    app_name = "GSM App"
    dev_prefix = "L_"

    @classmethod
    def build_title(cls, page_label: str | None = None) -> str:
        prefix = cls.dev_prefix if is_dev_env() else ""
        base_title = f"{prefix}{cls.app_name}"
        return f"{base_title} | {page_label}" if page_label else base_title
        
