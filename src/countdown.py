import asyncio
from collections.abc import Awaitable, Callable


def countdown_values(start: int) -> range:
    return range(start, -1, -1)


async def run_countdown(
    start: int,
    on_tick: Callable[[int], None],
    on_step: Callable[[int], Awaitable[None]] | None = None,
) -> None:
    for sec in countdown_values(start):
        on_tick(sec)
        if sec > 0:
            if on_step is not None:
                await on_step(sec)
            await asyncio.sleep(1)
