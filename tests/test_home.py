from typing import Any
import pytest


@pytest.mark.parametrize("flet_app", ["/home"], indirect=True)
def test_text(flet_app: Any):
    tester = flet_app.tester

    tester.pump_and_settle()

    assert tester.find_by_text_containing("justo").count == 1
