# src/gsm/core/app_env.py
import os
from dataclasses import dataclass

from ..helpers.env import get_env


@dataclass(frozen=True)
class AppEnv:
    """Détection de l'environnement d'exécution de l'app."""

    name: str = str(get_env("ENV_LOCAL", "0"))

    def is_local(self) -> bool:
        return self.name == "1"
    
    def plateform(self) -> str:
        return os.name

app_env = AppEnv()