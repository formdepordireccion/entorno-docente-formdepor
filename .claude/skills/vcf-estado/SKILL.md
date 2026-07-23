---
name: vcf-estado
description: Genera una foto de estado del proyecto VCF/TSEAS (rol de Coordinador / Centro de control) — qué falta en ficha.yaml, qué carpetas están vacías, próximos hitos del calendario e incoherencias detectadas. Úsalo cuando el usuario pida el estado, resumen, panel de control o "qué falta" de la asignatura VCF.
---

# /vcf-estado — Coordinador de la asignatura VCF/TSEAS

## Rol

Coordinador de asignatura: supervisa el proyecto VCF/TSEAS, no genera
contenido nuevo, solo informa.

## Entradas

- `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml`
- El contenido actual de las carpetas `01_NORMATIVA_CURRICULO/` a
  `14_HISTORICO_CAMBIOS/` dentro de `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/`
- `04_TEMPORALIZACION/calendario_26_27.md` si existe
- La fecha actual

## Tareas

1. Lee `ficha.yaml` y lista qué campos siguen a `null` o `[]` (p. ej.
   `normativa.rd_estatal`, `resultados_aprendizaje`, `unidades`).
2. Recorre cada carpeta numerada de `VCF_TSEAS/` (excluyendo los
   `README.md`) y, por carpeta, indica si tiene contenido generado o está
   vacía.
3. Si existe `calendario_26_27.md`, compáralo con la fecha actual y señala
   los hitos (unidades, evaluaciones, entregas) previstos en los próximos
   30 días.
4. Detecta incoherencias simples:
   - Unidades listadas en `ficha.yaml → unidades` sin archivo
     correspondiente en `05_UNIDADES/`.
   - Archivos con `BORRADOR` en el nombre que llevan más de 30 días sin
     modificarse (usa la fecha de última modificación del archivo).
5. Presenta un resumen con cuatro bloques: **Pendiente de revisión**,
   **Huecos de contenido**, **Próximos hitos**, **Incoherencias**.
6. Si el usuario pide guardar el resumen, escríbelo en
   `DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/estado_<YYYY-MM-DD>.md` con la
   fecha de hoy.

## Salidas

Resumen en el chat con los cuatro bloques anteriores. Opcionalmente, un
archivo en `00_CENTRO_CONTROL/`.

## Límites

No modifica ni crea ningún documento de las carpetas 01-14 salvo el propio
informe en `00_CENTRO_CONTROL/`. No aprueba ni rechaza nada, solo informa.

## Validación humana

Ninguna: es puramente informativo. El usuario decide qué hacer con lo que
reporta.
