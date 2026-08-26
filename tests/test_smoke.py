import importlib.util
import sys
import pytest
from pathlib import Path


def _load_module(module_name: str, relative_path: str):
    app_window_dir = Path(__file__).resolve().parents[1] / "scripts" / "app_window"
    if str(app_window_dir) not in sys.path:
        sys.path.insert(0, str(app_window_dir))

    spec = importlib.util.spec_from_file_location(module_name, app_window_dir / relative_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _load_cli_spawner_module():
    return _load_module("cli_spawner_test_mod", "cli_spawner.py")


def _load_app_launcher_module():
    return _load_module("app_launcher_test_mod", "app_launcher.py")

@pytest.mark.skipif(sys.platform != "linux", reason="Test spécifique à Linux")
def test_linux_cli_spawner_skips_non_executable_candidates(tmp_path, monkeypatch) -> None:
    cli_spawner = _load_cli_spawner_module()

    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    gnome_terminal = fake_bin / "gnome-terminal"
    gnome_terminal.write_text("#!/bin/sh\n")
    gnome_terminal.chmod(0o644)
    xterm = fake_bin / "xterm"
    xterm.write_text("#!/bin/sh\n")
    xterm.chmod(0o755)

    monkeypatch.setenv("PATH", str(fake_bin))

    seen = []

    def fake_popen(args, *_, **__):
        seen.append(args)
        if args[0] == str(xterm):
            return object()
        raise PermissionError(13, "Permission denied", args[0])

    monkeypatch.setattr(cli_spawner.subprocess, "Popen", fake_popen)

    assert cli_spawner._spawn_cli_linux("gsm") is True
    assert seen == [[str(xterm)]]


def test_launch_cli_parent_falls_back_to_plain_launch(monkeypatch) -> None:
    app_launcher = _load_app_launcher_module()

    launched = {}

    monkeypatch.setattr(app_launcher, "spawn_cli_if_needed", lambda *args, **kwargs: False)
    monkeypatch.setattr(
        app_launcher,
        "_launch_plain",
        lambda app, action, env: launched.setdefault("plain", (app, action, env)),
    )

    action = type("Action", (), {"mode": "app", "apps": ["gsm"], "internal_child": False})()
    env = {"GSM_WINDOW_CLI": 1}

    app_launcher._launch_cli_parent("gsm", action, env)

    assert launched["plain"] == ("gsm", action, env)


def test_smoke() -> None:
    assert True
