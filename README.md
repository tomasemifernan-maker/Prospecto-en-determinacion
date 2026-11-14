# Prospecto de colegios (promos de egresados)

Herramienta para buscar y contactar colegios de Córdoba que compran ropa de egresados.

- App publicada: https://claude.ai/artifact/8fe78zXs7Uyj9nrC5vgVaw
- Los datos que cargás (colegios, estados, notas, ajustes) se guardan en la nube del artifact.

## Qué hay en cada carpeta

- `prospectos-colegios.html`: la app terminada (es lo que se publica).
- `app/plantilla.html`: la app sin los datos del padrón. Acá se hacen los cambios.
- `datos/padron-cordoba.json`: las 1.103 escuelas de Córdoba con secundario, sacadas del padrón oficial.
- `scripts/extraer_padron.py`: saca las escuelas de Córdoba del Excel nacional del padrón.
- `scripts/armar_app.py`: junta la plantilla con los datos y arma `prospectos-colegios.html`.

## Actualizar el padrón

1. Bajar el Excel más nuevo de https://datos.gob.ar/dataset/educacion-padron-oficial-establecimientos-educativos
2. `python3 scripts/extraer_padron.py padron.xlsx` (necesita `pip install openpyxl`)
3. `python3 scripts/armar_app.py`
4. Volver a publicar `prospectos-colegios.html` en el mismo link.

## Fuentes

- Padrón Oficial de Establecimientos Educativos, actualizado al 16/06/2026.
- Anuario de estadísticas educativas 2023 de Córdoba (egresados por departamento, ciclo 2022).
- Competencia: Google Maps al 13/11/2026.
