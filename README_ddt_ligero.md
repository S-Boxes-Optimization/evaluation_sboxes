# DDT ligera portable

Esta versión calcula la tabla diferencial (DDT) de una S-box y no depende de módulos internos del repositorio.

## Archivo principal

- `ddt_ligero.py`

## Qué copiar a otro repositorio

1. `ddt_ligero.py`
2. (Opcional) `README_ddt_ligero.md`

No necesitas copiar carpetas `evaluation/` ni `sboxes/`.

## Uso

### 1) Desde archivo JSON (como en este repo)

```bash
python ddt_ligero.py --file sboxes/data/ascon.json
```

Admite:
- JSON objeto con `table`, `input_size`, `output_size` (y opcional `name`)
- JSON lista con la tabla directamente

### 2) Desde lista directa

```bash
python ddt_ligero.py --sbox "[0xC,0x5,0x6,0xB,0x9,0x0,0xA,0xD,0x3,0xE,0xF,0x8,0x4,0x7,0x1,0x2]"
```

También sirve formato coma-separado:

```bash
python ddt_ligero.py --sbox "12,5,6,11,9,0,10,13,3,14,15,8,4,7,1,2"
```

### 3) Guardar en CSV

```bash
python ddt_ligero.py --file sboxes/data/ascon.json --out ddt.csv
```

