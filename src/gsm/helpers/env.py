import os, re, inspect
from dotenv import load_dotenv
from datetime import datetime as dt

# Charger les variables d'environnement du fichier .env
load_dotenv(override=True)

_CHECK_TIME_FORMAT = "%Y-%m-%d %H:%M"
APP_NAME = "Up You!"

#################################################
DEFAULT_ROUTE = "/archives"  # 2ar unused
DEFAULT_ROUTE = "/react"
DEFAULT_ROUTE = "/home"
DEFAULT_ROUTE = "/tests2"
DEFAULT_ROUTE = "/tests"
DEFAULT_ROUTE = "/icons"
DEFAULT_ROUTE = "/calculator"
DEFAULT_ROUTE = "/about"
DEFAULT_ROUTE = "/counter"
#################################################


def get_env(key: str, default=None):
    return os.getenv(key, default)


def is_dev_env() -> bool:
    return get_env("DEV", "0") == "1"


def _env_int(name: str, default: int = 0) -> int:
    raw = str(os.getenv(name, str(default)) or "").strip()

    if not raw:
        return default

    # Tolère les valeurs de type "1526 # commentaire" dans .env.
    raw = raw.split("#", 1)[0].strip()
    match = re.search(r"[-+]?\d+", raw)
    if not match:
        return default

    try:
        return int(match.group(0))
    except TypeError, ValueError:
        return default


def curr_time():
    now = dt.now()
    return f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"


def nf(f, dec=2):
    "Number Format 123456789 → 123 456,79"
    try:
        f = float(f)
        # Keep formatting deterministic on all platforms (desktop/mobile/web)
        # by avoiding OS locale dependencies.
        s = f"{f:,.{dec}f}"
        # U+00A0 is better supported on Android fonts than U+202F.
        return s.replace(",", "\u00a0").replace(".", ",")
    except TypeError, ValueError:
        print(f"nf(): unsupported value type ({type(f).__name__}) -> {f}")
        return str(f)


def dv(var) -> str:
    """Debug Var → name = <type> value"""
    frame = inspect.currentframe()

    if frame is None:
        print(f"<unknown> = <{type(var).__name__}> {var!r}")
        return ""

    caller = frame.f_back
    if caller is None:
        print(f"<unknown> = <{type(var).__name__}> {var!r}")
        return ""

    name = None
    for var_name, var_val in caller.f_locals.items():
        if var_val is var:
            name = var_name
            break

    if name is None:
        name = "<unknown>"

    return f"{name} = <{type(var).__name__}> {var!r}"


def dvd(var):
    """Debug Var → name = <type> value"""
    frame = inspect.currentframe()

    if frame is None:
        print(f"<unknown> = <{type(var).__name__}> {var!r}")
        return

    caller = frame.f_back
    if caller is None:
        print(f"<unknown> = <{type(var).__name__}> {var!r}")
        return

    name = None
    for var_name, var_val in caller.f_locals.items():
        if var_val is var:
            name = var_name
            break

    if name is None:
        name = "<unknown>"

    print(f"{name} = <{type(var).__name__}> {var!r}")


if __name__ == "__main__":

    w = int(str(get_env("gsm_WINDOW_LEFT", 1912)))
    # print(w)
    print(repr(w))
    # from dotenv import find_dotenv, dotenv_values
    # print(find_dotenv())
    # print(os.environ.get("gsm_WINDOW_LEFT"))
    # print(dotenv_values(".env"))
