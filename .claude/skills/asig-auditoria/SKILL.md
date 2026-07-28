---
name: asig-auditoria
description: Audita el material histórico existente de la asignatura indicada (p. ej. "3. VALORACIÓN 25_26/" para VCF, "3. METODOLOGÍA 25_26/" para MET — una carpeta por asignatura en la raíz del proyecto), lo clasifica como vigente/reutilizable/obsoleto, y propone y ejecuta (tras confirmación) su copia a DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/06_TEMARIO y 07_ACTIVIDADES_TAREAS. Úsalo cuando el usuario pida auditar, ordenar, clasificar o migrar el material antiguo de una asignatura.
---

# /asig-auditoria — Auditoría de contenidos

## Rol

Audita el material acumulado de cursos anteriores y decide, con el usuario,
qué migra a la nueva estructura y qué queda fuera.

## Entradas

- La carpeta histórica de la asignatura resuelta (p. ej. `3. VALORACIÓN
  25_26/` para VCF, `3. METODOLOGÍA 25_26/` para MET) completa. Para VCF,
  por ejemplo: subcarpetas `0. VALORACIÓN FORMDEPOR 18_19` a `24_25`,
  `TAREAS 25_26/`, `TAEXAMENES 25_26/`, `o. programación 26_27/`, y los
  archivos de temario sueltos (`TEMA 0` a `TEMA 8`).
- `ficha.yaml` de la asignatura (contenidos vigentes, si `/asig-normativa`
  ya se ejecutó).

## Tareas

1. Lista recursivamente todos los archivos de la carpeta histórica de la
   asignatura resuelta con su ruta completa.
2. Clasifica cada archivo por tipo (TEMARIO si el nombre contiene "TEMA" o
   está en una carpeta de presentaciones/temario; TAREA si el nombre
   contiene "TAREA" o está en `TAREAS_25_26`/`TAEXAMENES_25_26`; PROGRAMACIÓN
   si está en `o. programación 26_27/`; OTRO en cualquier otro caso).

   Para TEMARIO, la antigüedad no sigue la fecha del archivo: **todo
   material migrado desde la carpeta histórica de la asignatura (de
   cualquier año, incluido el curso más reciente) va siempre a
   REFERENCIA_HISTORICA**, nunca a VIGENTE. `06_TEMARIO/VIGENTE/` se
   reserva exclusivamente para lo que `/asig-tema` genera de nuevo para
   26/27 — un archivo migrado ahí sería invisible para la búsqueda de
   referencia de `/asig-tema` (que solo mira en REFERENCIA_HISTORICA) y
   rompería la separación origen/generado.

   Para TAREA aplica la misma regla que para TEMARIO desde que existe
   `/asig-tarea`: **todo material migrado (de cualquier año, incluido
   25/26) va siempre a REFERENCIA_HISTORICA**, nunca a VIGENTE.
   `07_ACTIVIDADES_TAREAS/VIGENTE/` se reserva exclusivamente para lo que
   `/asig-tarea` genera de nuevo para 26/27.
3. Para los archivos de TEMARIO, compara sus temas contra
   `ficha.yaml → contenidos` (si existe) y márcalos como potencialmente
   obsoletos (poco útiles como referencia) si no encuentras
   correspondencia con ningún RA/contenido vigente.
4. Presenta una tabla al usuario con columnas: `Origen | Tipo | Clasificación
   | Destino propuesto`. El destino sigue uno de estos patrones.
   `<CODIGO>_<CICLO>` es la carpeta de la asignatura resuelta según
   CLAUDE.md → "Cómo se resuelve la asignatura":
   - `DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/06_TEMARIO/VIGENTE/`
   - `DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/06_TEMARIO/REFERENCIA_HISTORICA/`
   - `DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/07_ACTIVIDADES_TAREAS/VIGENTE/`
   - `DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/`
   - `DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/02_PROGRAMACION/REFERENCIA_HISTORICA/`
     (tipo PROGRAMACIÓN — borradores/programaciones docentes originales,
     conservados como fuente de datos reales para `/asig-normativa`)
   Para archivos de tipo OTRO que no encajen claramente en temario, tareas
   o programación (material de apoyo general, hojas de cálculo, posibles
   bases de datos de alumnado, etc.), no propongas destino automático:
   pregunta al usuario qué hacer, y si el nombre o contenido sugiere datos
   personales de alumnado (listas, calificaciones, bases de datos), avisa
   explícitamente antes de proponer nada.
5. Filtra por formato antes de proponer la copia: los archivos `.key`
   (Keynote) no se copian nunca por defecto — ni Claude puede leerlos ni
   suelen aportar valor como referencia versionada, y a menudo son muy
   pesados. Regístralos solo como referencia (nombre y ubicación) en
   `migraciones.md`, sin copiarlos. Formatos legibles (`.pdf`, `.docx`,
   `.pptx`, `.xlsx`, `.md`) sí se proponen para copia, sea cual sea su
   tamaño — pero si un archivo individual supera claramente el resto del
   lote (p. ej. varias veces el tamaño típico), señálalo aparte en la
   tabla en vez de darlo por hecho junto al resto.
6. No copies nada todavía. Espera confirmación explícita del usuario, que
   puede aprobar la tabla completa o pedir cambios fila por fila.
7. Tras confirmación, **copia** (nunca muevas ni borres el original) cada
   archivo confirmado a su destino, conservando el nombre original.
8. Añade una entrada a `14_HISTORICO_CAMBIOS/migraciones.md` con la fecha
   de hoy y la lista de archivos copiados (origen → destino), incluyendo
   los `.key` registrados solo como referencia (sin copiar).

## Salidas

Tabla de propuesta de migración, archivos copiados tras confirmación,
`migraciones.md` actualizado.

## Límites

Nunca borra ni mueve el material original de la carpeta histórica de la
asignatura — solo copia. Nunca copia un archivo sin que el usuario lo haya
confirmado explícitamente para ese archivo o para el bloque que lo
contiene. Los archivos copiados pasan a formar parte del historial de git
(el repositorio crece con el tiempo, porque los binarios no son
diffables); para archivos muy grandes (decenas de MB o más), vale la pena
valorar con el docente si de verdad necesitan vivir en git o si basta con
una referencia ligera (nombre de archivo + nota en `migraciones.md`).

## Validación humana

Obligatoria antes de cada copia (puede darse en bloque para varios archivos
a la vez si el usuario lo dice explícitamente, p. ej. "copia todos los de
TAREAS 25_26 como vigentes").
