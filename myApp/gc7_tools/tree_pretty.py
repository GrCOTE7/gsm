from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

DEFAULT_EXCLUDES = {".git", ".venv", ".vscode", "build", "__pycache__"}


def iter_children(path: Path, excluded_names: set[str]) -> list[Path]:
    children = [child for child in path.iterdir() if child.name not in excluded_names]
    # Dossiers d'abord, puis fichiers, tri alphabetique insensible a la casse.
    children.sort(key=lambda p: (not p.is_dir(), p.name.lower()))
    return children


def build_tree_lines(
    root: Path, excluded_names: set[str], include_files: bool
) -> list[str]:
    lines: list[str] = [str(root.resolve())]

    def walk(current: Path, prefix: str = "") -> None:
        children = iter_children(current, excluded_names)
        if not include_files:
            children = [child for child in children if child.is_dir()]

        for index, child in enumerate(children):
            is_last = index == len(children) - 1
            branch = "└── " if is_last else "├── "
            lines.append(f"{prefix}{branch}{child.name}")

            if child.is_dir():
                child_prefix = f"{prefix}{'    ' if is_last else '│   '}"
                walk(child, child_prefix)

    walk(root)
    return lines


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Genere une arborescence texte avec symboles Unicode "
            "(├──, └──, │) en excluant .git et .venv par defaut."
        )
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Dossier racine a afficher (defaut: dossier courant).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="tree.txt",
        help="Fichier de sortie UTF-8 (defaut: txt_pretty.txt).",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Nom de dossier/fichier a exclure (peut etre repete).",
    )
    parser.add_argument(
        "--dirs-only",
        action="store_true",
        help="N'afficher que les dossiers.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root).resolve()

    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Chemin invalide: {root}")

    excluded_names = DEFAULT_EXCLUDES.union(set(args.exclude))
    lines = build_tree_lines(root, excluded_names, include_files=not args.dirs_only)

    output_path = Path(args.output)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Arborescence ecrite dans: {output_path.resolve()}")
    print(f"Exclusions: {', '.join(sorted(excluded_names))}")


if __name__ == "__main__":
    main()
