# Próxima etapa en Codex — integración de benchmarks al evaluador existente

Trabaja **en el repositorio existente** `S-Boxes-Optimization/evaluation_sboxes`, sin crear repositorios ni alterar las carpetas históricas. Inspecciona primero `git status`, `sboxes/loader.py`, `sboxes/sbox.py`, `evaluation/` y `data/literature_sboxes/`.

## Objetivo

Integrar las S-Boxes de literatura con los evaluadores que YA ESTÁN en `evaluation/`, conservando su semántica y evitando funciones duplicadas. Usa la carpeta `data/literature_sboxes/{n}x{n}/` para benchmarks externos y mantén `data/{n}x{n}_sboxes/` para las muestras propias. Por ahora solo está poblado `8x8/` (14 tablas publicadas y 22 referencias); las carpetas `4x4` a `7x7` están preparadas sin inventar datos.

## Pasos

1. Valida `python scripts/validar_sboxes_literatura.py` y utiliza `scripts/exportar_sbox_literatura.py` para comprobar la compatibilidad con el cargador actual.
2. Inspecciona las métricas existentes (`uniformity.py`, `linearity.py`, `avalanche_criterion.py`, `boomerang.py`, `fixed_points.py`, `cost_function.py`, `sbox_metrics_analysis.py`) y documenta sus definiciones exactas.
3. Implementa un adaptador mínimo que pase las 14 tablas a esas funciones sin cambiar los notebooks o resultados 4×4 a 7×7. Separa no linealidad vectorial, por coordenadas y promedio; anota normalizaciones de SAC/BIC/DDT/LAT.
4. Crea una CLI que genere en `results/literature/` CSV y JSON con métricas, `id`, `reference_id`, `source_type`, DOI/URL, hash y parámetros de cálculo, sin sobrescribir CSV históricos.
5. Añade pruebas unitarias para validación de fuentes y valores conocidos de AES (no linealidad vectorial 112, DU 4 para la definición estándar), haciendo pruebas para otras dimensiones según sus propiedades matemáticas.
6. Añade un esquema separado para resultados propios con `algorithm`, `cost_function`, `seed`, `parameters`, `evaluations`, `runtime_seconds` y `best_sbox`. Nunca inventes resultados experimentales.
7. Para Overleaf, implementa `paper_export/` para producir tablas `.tex`, gráficos y `references.bib`, pero **no sincronices todo el repositorio científico** con Overleaf por contener datos/entornos pesados.

## Restricciones

No borres, reescribas ni ejecutes todos los notebooks. No modifiques `data/clasics/`, `evaluation-env/`, `data/4x4_sboxes` a `data/8x8_sboxes`, ni CSV históricos. No atribuyas al artículo original una tabla de `source_type=secondary` sin contrastarla; integridad SHA-256 no prueba fidelidad al paper. No hagas push, merge o cambios destructivos sin autorización. Antes de editar, presenta el plan mínimo y verifica el estado de la rama actual.
