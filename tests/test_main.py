from typing import Any


def test_increment(flet_app: Any):
    tester = flet_app.tester

    tester.pump_and_settle()

    # Initial state
    assert tester.find_by_text("0").count == 1

    # Tap the increment button (found by its key) and let the UI update
    tester.tap(tester.find_by_key("increment"))
    tester.pump_and_settle()

    # New state
    assert tester.find_by_text("1").count == 1