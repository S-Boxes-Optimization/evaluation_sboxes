#!/usr/bin/env python3
"""Valida catálogos literarios por tamaño, sin dependencias externas ni efectos laterales."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "literature_sboxes"


def validar_catalogo(path: Path) -> tuple[int, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    references = data.get("references", [])
    sboxes = data.get("sboxes", [])
    if not isinstance(references, list) or not isinstance(sboxes, list):
        raise ValueError(f"{path}: 'references' y 'sboxes' deben ser listas")
    ref_ids = [ref.get("id") for ref in references]
    if not all(isinstance(x, str) and x for x in ref_ids) or len(ref_ids) != len(set(ref_ids)):
        raise ValueError(f"{path}: identificadores bibliográficos vacíos o duplicados")
    box_ids = [box.get("id") for box in sboxes]
    if not all(isinstance(x, str) and x for x in box_ids) or len(box_ids) != len(set(box_ids)):
        raise ValueError(f"{path}: identificadores de S-Box vacíos o duplicados")
    for box in sboxes:
        identifier = box["id"]
        n = box.get("bit_width")
        values = box.get("sbox")
        if type(n) is not int or n < 1 or n > 8:
            raise ValueError(f"{identifier}: bit_width inválido: {n!r}")
        if path.parent.name != f"{n}x{n}":
            raise ValueError(f"{identifier}: tamaño incompatible con directorio")
        if not isinstance(values, list) or len(values) != 1 << n:
            raise ValueError(f"{identifier}: se esperaban {1 << n} entradas")
        if any(type(v) is not int or not 0 <= v < (1 << n) for v in values):
            raise ValueError(f"{identifier}: valores fuera de rango")
        if len(set(values)) != len(values):
            raise ValueError(f"{identifier}: no es una permutación")
        if box.get("reference_id") not in ref_ids:
            raise ValueError(f"{identifier}: referencia inexistente")
        if hashlib.sha256(bytes(values)).hexdigest() != box.get("sha256"):
            raise ValueError(f"{identifier}: SHA-256 inválido")
    return len(sboxes), len(references)


def main() -> None:
    paths = sorted(BASE.glob("*x*/catalogo_sboxes.json"))
    if not paths:
        raise SystemExit("No se encontraron catálogos de literatura")
    for path in paths:
        boxes, refs = validar_catalogo(path)
        print(f"OK {path.relative_to(ROOT)}: {boxes} S-Boxes, {refs} referencias")
    print("Nota: integridad y biyectividad no implican fidelidad a la publicación original.")


if __name__ == "__main__":
    main()
