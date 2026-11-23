# src/gsm/core/app_env.py
from dataclasses import dataclass
from platform import system as system_name

from ..helpers.env import get_env


@dataclass(frozen=True)
class AppEnv:
    """Détection de l'environnement d'exécution de l'app."""

    name: str = str(get_env("ENV_LOCAL", "0"))

    def is_local(self) -> bool:
        return self.name == "1"

    def platform(self) -> str:
        """Nom lisible du système : 'Windows', 'Linux', 'Darwin'.

        On importe `system` depuis le module stdlib `platform` (plutôt que
        `import platform`) car cette méthode porte le même nom : cela évite
        toute ambiguïté à la lecture du fichier.

        On n'utilise pas `os.name`, qui renvoie un identifiant de noyau peu
        parlant ('nt' sous Windows), incohérent avec le `OS: Windows 11` affiché
        par ailleurs dans le diagnostic.
        """
        return system_name()


app_env = AppEnv()
