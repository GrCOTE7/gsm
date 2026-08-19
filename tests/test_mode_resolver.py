"""Tests unitaires du résolveur de mode du launcher (scripts/app_window)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "app_window"))

from mode_resolver import resolve_mode


def test_default_gsm_app():
    action = resolve_mode("")
    assert action.apps == ["gsm"]
    assert action.mode == "app"
    assert not action.internal_child


def test_w_gsm_web():
    action = resolve_mode("w")
    assert action.apps == ["gsm"]
    assert action.mode == "web"


def test_u_upu_app():
    action = resolve_mode("u")
    assert action.apps == ["upu"]
    assert action.mode == "app"


def test_gu_both_apps():
    action = resolve_mode("gu")
    assert action.apps == ["gsm", "upu"]
    assert action.mode == "app"


def test_debug():
    action = resolve_mode("debug")
    assert action.apps == ["gsm"]
    assert action.mode == "debug"


def test_case_insensitive():
    assert resolve_mode("GU").apps == ["gsm", "upu"]


def test_internal_child():
    action = resolve_mode("_gsm_child")
    assert action.apps == ["gsm"]
    assert action.mode == "app"
    assert action.internal_child is True
    assert action.skip_cli_placement is False


def test_internal_child_web():
    assert resolve_mode("_gsm_child_web").mode == "web"


def test_internal_nocli():
    action = resolve_mode("_gsm_nocli")
    assert action.internal_child is True
    assert action.skip_cli_placement is True


def test_internal_upu_nocli_web():
    action = resolve_mode("_upu_nocli_web")
    assert action.apps == ["upu"]
    assert action.mode == "web"
    assert action.skip_cli_placement is True


def test_unknown_mode_fallback():
    action = resolve_mode("zzz")
    assert action.apps == ["gsm"]
    assert action.mode == "app"
