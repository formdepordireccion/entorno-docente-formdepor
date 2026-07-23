---
name: vcf-auditoria
description: Audita el material existente en "3. VALORACIÓN 25_26/" (programaciones, temario y tareas de 18/19 a 25/26), lo clasifica como vigente/reutilizable/obsoleto, y propone y ejecuta (tras confirmación) su copia a DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO y 07_ACTIVIDADES_TAREAS. Úsalo cuando el usuario pida auditar, ordenar, clasificar o migrar el material antiguo de VCF.
---

# /vcf-auditoria — Auditoría de contenidos (VCF/TSEAS)

## Rol

Audita el material acumulado de cursos anteriores y decide, con el usuario,
qué migra a la nueva estructura y qué queda fuera.

## Entradas

- `3. VALORACIÓN 25_26/` completa: subcarpetas `0. VALORACIÓN FORMDEPOR
  18_19` a `24_25`, `TAREAS 25_26/`, `TAEXAMENES 25_26/`, `o. programación
  26_27/`, y los archivos de temario sueltos (`TEMA 0` a `TEMA 8`).
- `ficha.yaml` (contenidos vigentes, si `/vcf-normativa` ya se ejecutó).

## Tareas

1. Lista recursivamente todos los archivos de `3. VALORACIÓN 25_26/` con su
   ruta completa.
2. Clasifica cada archivo por tipo (TEMARIO si el nombre contiene "TEMA" o
   está en una carpeta de presentaciones/temario; TAREA si el nombre
   contiene "TAREA" o está en `TAREAS_25_26`/`TAEXAMENES_25_26`; PROGRAMACIÓN
   si está en `o. programación 26_27/`; OTRO en cualquier otro caso) y por
   antigüedad (VIGENTE si es de 25/26 o del borrador 26/27;
   REFERENCIA_HISTORICA si es de 24/25 o anterior).
3. Para los archivos de TEMARIO clasificados VIGENTE, compara sus temas
   contra `ficha.yaml → contenidos` (si existe) y márcalos como
   potencialmente obsoletos si no encuentras correspondencia.
4. Presenta una tabla al usuario con columnas: `Origen | Tipo | Clasificación
   | Destino propuesto`. El destino sigue siempre uno de estos cuatro
   patrones:
   - `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/VIGENTE/`
   - `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/REFERENCIA_HISTORICA/`
   - `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS/VIGENTE/`
   - `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/`
5. No copies nada todavía. Espera confirmación explícita del usuario, que
   puede aprobar la tabla completa o pedir cambios fila por fila.
6. Tras confirmación, **copia** (nunca muevas ni borres el original) cada
   archivo confirmado a su destino, conservando el nombre original.
7. Añade una entrada a `14_HISTORICO_CAMBIOS/migraciones.md` con la fecha
   de hoy y la lista de archivos copiados (origen → destino).

## Salidas

Tabla de propuesta de migración, archivos copiados tras confirmación,
`migraciones.md` actualizado.

## Límites

Nunca borra ni mueve el material original de `3. VALORACIÓN 25_26/` — solo
copia. Nunca copia un archivo sin que el usuario lo haya confirmado
explícitamente para ese archivo o para el bloque que lo contiene. Los
archivos copiados pasan a formar parte del historial de git (el
repositorio crece con el tiempo, porque los binarios no son diffables);
para archivos muy grandes (decenas de MB o más), vale la pena valorar con
el docente si de verdad necesitan vivir en git o si basta con una
referencia ligera (nombre de archivo + nota en `migraciones.md`).

## Validación humana

Obligatoria antes de cada copia (puede darse en bloque para varios archivos
a la vez si el usuario lo dice explícitamente, p. ej. "copia todos los de
TAREAS 25_26 como vigentes").
