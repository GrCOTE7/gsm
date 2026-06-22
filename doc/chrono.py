import time
from datetime import timedelta
import importlib
import sys

# Auto‑reload du module si déjà importé
if "chrono" in sys.modules:
    importlib.reload(sys.modules["chrono"])

_start_time = None

def chrono():
    global _start_time

    # Si pas démarré → on démarre
    if _start_time is None:
        _start_time = time.perf_counter()
        return

    # Sinon → on arrête et on affiche
    end = time.perf_counter()
    seconds = end - _start_time

    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60

    print(f"Temps écoulé : {h:02d}:{m:02d}:{s:05.2f}")
