---
name: vcf-tarea
description: Genera actividades y tareas nuevas para VCF (iniciales, de desarrollo, prácticas, proyectos, casos, retos, debates, refuerzo, ampliación) vinculadas a RA/criterios concretos, apoyándose en las tareas de cursos anteriores como referencia. Úsalo cuando el usuario pida crear, diseñar o generar una actividad o tarea nueva de VCF.
---

# /vcf-tarea — Actividades y tareas (VCF/TSEAS)

## Rol

Genera actividades y tareas para el alumnado, vinculadas explícitamente a
resultados de aprendizaje y criterios de evaluación reales. Es al ámbito
de "actividades y tareas" lo que `/vcf-tema` es al temario: reutiliza como
inspiración lo que ya existe en `07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/`
(tareas de cursos anteriores) en vez de partir siempre de cero, pero
adapta el resultado al currículo vigente de `ficha.yaml`.

## Entradas

- Unidad o RA/criterio para el que se pide la tarea (pedirlo si no se
  especifica).
- `ficha.yaml → resultados_aprendizaje`, `criterios_evaluacion`,
  `contenidos`, `unidades`.
- `07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/` como banco de referencia
  de tareas de cursos anteriores.
- `07_ACTIVIDADES_TAREAS/VIGENTE/` para no proponer un número de tarea ya
  usado este curso.

## Tareas

1. Si no se especifica, pregunta qué unidad (`UD<NN>`) y qué tipo de
   actividad quiere el docente: inicial/motivación, de desarrollo,
   práctica, proyecto, caso, trabajo, reto, debate, refuerzo o
   ampliación.
2. Busca en `07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/` tareas
   relacionadas con la misma unidad/RA en cursos anteriores. Si
   encuentras una tarea reutilizable, indícalo explícitamente y adáptala
   (actualiza cualquier referencia a contenidos/criterios que hayan
   cambiado respecto a la normativa vigente en `ficha.yaml`) en vez de
   copiarla sin más. Si no encuentras nada, dilo explícitamente y genera
   la tarea desde `ficha.yaml → contenidos`.
3. Redacta la tarea con: enunciado para el alumnado, tipo de actividad,
   RA y criterio(s) concretos que evalúa (citados literalmente de
   `ficha.yaml`), tiempo estimado, recursos/material necesario, y
   criterios de entrega (qué se espera, en qué formato, individual o en
   grupo).
4. Numera la tarea siguiendo la secuencia ya usada en
   `07_ACTIVIDADES_TAREAS/VIGENTE/` para ese curso (revisa qué números de
   tarea ya existen antes de asignar uno nuevo, para no duplicar).
5. Guarda como
   `07_ACTIVIDADES_TAREAS/VIGENTE/VCF_TAREA_UD<NN>_<N>_2026-2027_V01_BORRADOR.md`,
   donde `<NN>` es la unidad y `<N>` el número de tarea dentro de esa
   unidad.

## Salidas

Un archivo de tarea en `07_ACTIVIDADES_TAREAS/VIGENTE/` por tarea
generada.

## Límites

No inventa un vínculo con un RA/criterio que la tarea en realidad no
evalúa. Si reutiliza una tarea histórica, lo dice explícitamente en el
propio documento (qué tarea de qué curso se usó como base) en vez de
presentarla como completamente nueva. El archivo se guarda siempre en
`BORRADOR`.

## Validación humana

La tarea queda en `BORRADOR` hasta que el docente la revise y apruebe
(vía `/vcf-revision`, igual que unidades/temario/exámenes).
