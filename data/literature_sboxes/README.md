# S-Boxes de la literatura por tamaño

Esta carpeta reúne S-Boxes **publicadas** que sirven como referencias para comparar los algoritmos de optimización del proyecto. No sustituye a `data/4x4_sboxes` ... `data/8x8_sboxes`, donde se conservan los datos del proyecto, ni a `data/clasics` (nombre existente en este repositorio).

| Subcarpeta | Estado | Número de tablas importadas |
| --- | --- | ---: |
| `4x4/` | Preparada para investigaciones verificadas | 0 |
| `5x5/` | Preparada para investigaciones verificadas | 0 |
| `6x6/` | Preparada para investigaciones verificadas | 0 |
| `7x7/` | Preparada para investigaciones verificadas | 0 |
| `8x8/` | Catálogo inicial con vectores, referencias y procedencia | 14 |

El catálogo `8x8/catalogo_sboxes.json` contiene 14 permutaciones de 256 valores y 22 entradas bibliográficas. La fuente de cada S-Box se identifica mediante `reference_id`; `source_type=secondary` indica que fue reproducida por una fuente secundaria y **no** comprobada directamente contra el artículo original.

## Validación y exportación

Desde la raíz del repositorio, con Python 3:

```bash
python scripts/validar_sboxes_literatura.py
python scripts/exportar_sbox_literatura.py --list
python scripts/exportar_sbox_literatura.py zhu2020_adaptive_ga --output /tmp/zhu2020.json
```

En Windows puedes usar `--output zhu2020.json`. El archivo exportado es compatible con `sboxes/loader.py`: `name`, `input_size`, `output_size` y `table` en hexadecimal. El JSON maestro mantiene **números enteros** para procesar en Python sin conversiones innecesarias.

Los verificadores comprueban longitud, rango, unicidad, referencias y SHA-256; esto **no acredita** que la transcripción de cada tabla coincida con el artículo original. Antes de publicar comparaciones, cotejar las tablas de origen secundario con las fuentes primarias y recalcular métricas con definiciones homogéneas. No reemplazar resultados históricos ni las implementaciones existentes de `evaluation/`.

Para añadir nuevas tablas 4×4 a 7×7, usar el mismo esquema por carpeta con `bit_width`, `sbox` (longitud `2**bit_width`) y referencia trazable. Las S-Boxes no biyectivas requieren ampliar deliberadamente la validación en lugar de saltarse los controles.
