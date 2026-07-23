---
name: vcf-programacion
description: Cierra la programación didáctica 26/27 de VCF a partir del borrador existente y de ficha.yaml, y genera el calendario de temporalización (unidades, evaluaciones, entregas, recuperación) descontando festivos y no lectivos de Extremadura. Úsalo cuando el usuario pida programación, temporalización o calendario del curso 26/27.
---

# /vcf-programacion — Planificación y temporalización (VCF/TSEAS)

## Rol

Genera los planes anual/trimestral y el calendario de unidades y
evaluaciones del curso 2026-2027, descontando festivos, vacaciones y días
no lectivos de Extremadura.

## Entradas

- `ficha.yaml`: `resultados_aprendizaje`, `criterios_evaluacion`,
  `contenidos`, `asignatura.horas_totales`, `asignatura.horas_semanales`.
  Si estos campos están vacíos, avisa al usuario de que conviene ejecutar
  `/vcf-normativa` antes, pero puedes continuar con lo que el usuario te
  dé directamente si insiste.
- `3. VALORACIÓN 25_26/o. programación 26_27/1.Modulo Profesional
  Valoracion de la CF_Mario_Curso 2026-2027.md` (borrador ya existente,
  nombre real del archivo sin tildes; hay también un `.docx` homólogo con
  tildes en la misma carpeta).
- Calendario escolar oficial de Extremadura 2026-2027 (festivos, no
  lectivos), buscado con WebSearch en la web de la Consejería de Educación
  de Extremadura si no lo aporta el usuario.

## Tareas

1. Lee el borrador de programación 26/27 y fusiónalo con los datos
   disponibles en `ficha.yaml` (RA, criterios, contenidos, horas).
2. Busca con WebSearch el calendario escolar oficial de Extremadura
   2026-2027. Si no lo encuentras con certeza, dilo explícitamente y pide
   al usuario que lo aporte o confirme.
3. Calcula las sesiones lectivas disponibles por trimestre, descontando
   festivos y no lectivos, según las horas semanales de `ficha.yaml`.
4. Distribuye las unidades sobre esas sesiones. Si `ficha.yaml → unidades`
   está vacío, propón una distribución basada en los contenidos y pide
   confirmación antes de fijarla. Deja huecos explícitos para
   evaluaciones y recuperación.
5. Genera `02_PROGRAMACION/programacion_26_27.md` con: introducción,
   contextualización, RA/criterios/contenidos (de `ficha.yaml`),
   metodología general, distribución temporal por trimestre, criterios de
   calificación (a rellenar/confirmar por el docente), atención a la
   diversidad general, y bibliografía/recursos.
6. Genera `04_TEMPORALIZACION/calendario_26_27.md`: tabla semana a semana
   con unidad/tema, sesión de evaluación o entrega si aplica.
7. Actualiza `ficha.yaml → unidades` con la lista de unidades y sus
   fechas de inicio/fin previstas. `estado` permanece en `borrador`.

## Salidas

`programacion_26_27.md`, `calendario_26_27.md`, `ficha.yaml` actualizado.

## Límites

No inventa fechas de festivos sin fuente verificada — si no puede
confirmarlas, las marca como "pendiente de verificar por el docente" en
vez de asumir un calendario genérico. No fija ponderaciones de
calificación sin que el docente las confirme.

## Validación humana

El docente debe aprobar la programación y el calendario (pasar
`estado` a `aprobado` explícitamente) antes de subirlos a Drive/Calendar.
