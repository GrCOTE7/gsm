"""Tests unitaires du résolveur de mode du launcher (scripts/app_window)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "app_window"))

import mode_resolver


def test_default_gsm_app():
    assert mode_resolver.resolve_mode("") == {"apps": ["gsm"], "mode": "app"}


def test_w_gsm_web():
    assert mode_resolver.resolve_mode("w") == {"apps": ["gsm"], "mode": "web"}


def test_u_upu_app():
    assert mode_resolver.resolve_mode("u") == {"apps": ["upu"], "mode": "app"}


def test_gu_both_apps():
    assert mode_resolver.resolve_mode("gu") == {"apps": ["gsm", "upu"], "mode": "app"}


def test_debug():
    assert mode_resolver.resolve_mode("debug")["mode"] == "debug"


def test_case_insensitive():
    assert mode_resolver.resolve_mode("GU")["apps"] == ["gsm", "upu"]


def test_internal_child():
    action = mode_resolver.resolve_mode("_gsm_child")
    assert action["apps"] == ["gsm"]
    assert action["mode"] == "app"
    assert action["internal_child"] is True
    assert action["skip_cli_placement"] is False


def test_internal_child_web():
    assert mode_resolver.resolve_mode("_gsm_child_web")["mode"] == "web"


def test_internal_nocli():
    action = mode_resolver.resolve_mode("_gsm_nocli")
    assert action["internal_child"] is True
    assert action["skip_cli_placement"] is True


def test_internal_upu_nocli_web():
    action = mode_resolver.resolve_mode("_upu_nocli_web")
    assert action["apps"] == ["upu"]
    assert action["mode"] == "web"
    assert action["skip_cli_placement"] is True


def test_unknown_mode_fallback():
    assert mode_resolver.resolve_mode("zzz")["apps"] == ["gsm"]
