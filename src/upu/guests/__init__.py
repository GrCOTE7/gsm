"""Up U! guests modules."""

import os
import importlib

REGISTRY = []

def register(subject_fn):
    REGISTRY.append(subject_fn)

# auto-import dynamique
base = os.path.dirname(__file__)

for filename in os.listdir(base):
    if filename.startswith("g") and filename.endswith(".py"):
        module_name = f"upu.guests.{filename[:-3]}"
        importlib.import_module(module_name)