#!/usr/bin/env python3
"""Exporta una S-Box publicada al formato admitido por sboxes.loader.load."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "literature_sboxes"


def cargar_catalogos() -> list[dict]:
    resultado = []
    for path in sorted(BASE.glob("*x*/catalogo_sboxes.json")):
        obj = json.loads(path.read_text(encoding="utf-8"))
        for box in obj.get("sboxes", []):
            resultado.append(box)
    return resultado


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("id", nargs="?", help="Identificador de la S-Box")
    p.add_argument("--list", action="store_true", help="Listar identificadores")
    p.add_argument("--output", type=Path, help="Archivo destino JSON")
    a = p.parse_args()
    boxes = cargar_catalogos()
    if a.list:
        for b in boxes:
            print(f"{b['id']} ({b['bit_width']}x{b['bit_width']}) | {b['reference_id']}")
        return
    if not a.id or a.output is None:
        p.error("Se requiere ID y --output, o bien --list")
    matches = [b for b in boxes if b['id'] == a.id]
    if len(matches) != 1:
        p.error("Identificador desconocido o duplicado: " + a.id)
    box = matches[0]
    n = box['bit_width']
    converted = {
        "name": box['id'],
        "input_size": n,
        "output_size": n,
        "table": [hex(x) for x in box['sbox']],
    }
    if a.output.exists():
        p.error(f"Archivo destino ya existe: {a.output}")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(converted, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Exportada {box['id']} a {a.output}")


if __name__ == '__main__':
    main()
