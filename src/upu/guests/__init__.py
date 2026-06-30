"""Up U! guests modules."""

import pkgutil
import importlib

REGISTRY = []

def register(subject_fn):
    REGISTRY.append(subject_fn)


# Work only in desktop Windows
# import os
# # auto-import dynamique
# base = os.path.dirname(__file__)

# for filename in os.listdir(base):
#     if filename.startswith("g") and filename.endswith(".py"):
#         module_name = f"upu.guests.{filename[:-3]}"
#         importlib.import_module(module_name)

# Works on win, lx and apk
package = __package__

for _, module_name, _ in pkgutil.iter_modules(__path__):
    if module_name.startswith("g"):
        module = importlib.import_module(f"{package}.{module_name}")