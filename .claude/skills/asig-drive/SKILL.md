---
name: asig-drive
description: Sube a Google Drive los documentos de la asignatura resuelta que ya están APROBADO, replicando la estructura de carpetas del proyecto dentro de una carpeta "<CODIGO>_<CICLO> <curso académico>". Úsalo cuando el usuario pida subir, sincronizar o compartir por Drive los documentos aprobados de una asignatura.
---

# /asig-drive — Integración con Google Drive

## Rol

Sube a Google Drive, bajo petición explícita del usuario en cada
ejecución, los documentos de la asignatura resuelta que ya tienen `APROBADO` en el nombre de
archivo (o el marcador de estado, para los 4 documentos base). Nunca
corre en segundo plano ni de forma automática.

## Entradas

- Todos los archivos con `APROBADO` en el nombre bajo
  `DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/` (unidades, temario,
  exámenes/solucionarios).
- Los 4 documentos base cuando su marcador de cabecera diga
  `**Estado: APROBADO**` (`normativa_registro.md`, `matriz_alineacion.md`,
  `programacion_26_27.md`, `calendario_26_27.md`).
- `ficha.yaml` (para saber qué hay aprobado sin tener que recorrer todos
  los archivos a mano).

## Tareas

1. Localiza en Google Drive, o crea si no existe, una carpeta de nivel
   superior llamada **`<CODIGO>_<CICLO> <curso académico>`** (p. ej. `VCF_TSEAS 2026-2027` o `MET_TSEAS 2026-2027`).
2. Dentro, replica solo las subcarpetas que realmente contienen algo
   aprobado (no crees las 15 carpetas si varias están vacías de
   aprobados): `01_NORMATIVA_CURRICULO`, `02_PROGRAMACION`,
   `03_MAPA_CURRICULAR`, `04_TEMPORALIZACION`, `05_UNIDADES`,
   `06_TEMARIO`, `08_EVALUACION`, etc., con la misma numeración y nombre
   que en el proyecto.
3. Antes de subir nada, compara con lo que ya existe en esa carpeta de
   Drive (por nombre) para no duplicar: si un documento con el mismo
   nombre ya está subido, pregunta si se debe reemplazar (una nueva
   versión aprobada más reciente) o dejarlo tal cual.
4. Presenta al usuario la lista de archivos que se van a subir, agrupada
   por carpeta, con el conteo total, y espera confirmación explícita
   antes de subir nada — igual que `/asig-auditoria` con las copias.
5. Tras confirmación, sube cada archivo como Google Doc (convertido desde
   Markdown, para que sea editable nativamente desde el móvil o la web),
   conservando el nombre de archivo original como título del documento.
6. Al terminar, informa con el enlace a la carpeta raíz de Drive y un
   resumen de cuántos archivos se subieron, cuántos se reemplazaron y
   cuántos se omitieron.

## Salidas

Carpeta `<CODIGO>_<CICLO> <curso académico>` en Google Drive con la estructura y los
documentos aprobados subidos como Google Docs; resumen en el chat con el
enlace a la carpeta.

## Límites

Solo sube documentos con `APROBADO` — nunca sube un `BORRADOR`, aunque el
usuario no se dé cuenta de que algo sigue sin aprobar (si lo pide, se le
avisa explícitamente en vez de subirlo). No borra ni modifica nada que ya
exista en Drive sin confirmación explícita para ese archivo en concreto.
No sube el material histórico de la carpeta correspondiente en la raíz del
proyecto (p. ej. `3. VALORACIÓN 25_26/` para VCF, `3. METODOLOGÍA 25_26/`
para MET — eso es contenido de referencia interno, no un documento aprobado
de la asignatura).
**Nunca sube nada de `10_DIVERSIDAD/INFORMES_ALUMNADO/`,
`10_DIVERSIDAD/PLANES_ADAPTACION/` ni
`11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/`** — son datos personales de
alumnado real (salud/discapacidad, o calificaciones), excluidos siempre
sin excepción, aunque el usuario pida "sube todo". Los informes
agregados de `11_SEGUIMIENTO_RESULTADOS/INFORMES/` sí se pueden subir
como cualquier otro documento aprobado.

## Validación humana

Obligatoria antes de cada subida (puede darse en bloque, p. ej. "sube
todo lo aprobado").
