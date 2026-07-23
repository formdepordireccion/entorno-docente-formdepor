---
name: vcf-examen
description: Genera instrumentos de evaluación de VCF (exámenes, rúbricas, banco de preguntas) vinculados a resultados de aprendizaje y criterios de evaluación, con su solucionario en archivo separado. Úsalo cuando el usuario pida un examen, rúbrica, banco de preguntas o solucionario de VCF.
---

# /vcf-examen — Evaluación (VCF/TSEAS)

## Rol

Genera pruebas de evaluación y sus solucionarios, controlando cobertura de
RA/criterios y dificultad.

## Entradas

- Unidad o bloque de contenidos a evaluar (pedirlo si no se especifica).
- `ficha.yaml`: `resultados_aprendizaje`, `criterios_evaluacion`.
- `07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/` y `08_EVALUACION/` como
  banco de referencia de exámenes/preguntas anteriores.

## Tareas

1. Si no se especifica, pregunta qué tipo de instrumento quiere el usuario:
   examen tipo test, de desarrollo, práctico, rúbrica, o banco de
   preguntas.
2. Identifica en `ficha.yaml` los RA y criterios del bloque a evaluar.
3. Redacta cada pregunta/ítem vinculado explícitamente a un RA y un
   criterio concreto (indícalo entre paréntesis junto a la pregunta).
   Verifica cobertura: todos los RA del bloque deben estar representados
   por al menos una pregunta.
4. Varía la dificultad (al menos un tercio de nivel básico, un tercio
   intermedio, un tercio de aplicación/análisis).
5. Si es examen: genera también una segunda versión alternativa (mismas
   preguntas reordenadas o con variantes equivalentes) pensada para
   recuperación.
6. Si es rúbrica: genera una escala de niveles de desempeño (p. ej.
   Insuficiente/Suficiente/Notable/Excelente) por cada criterio.
7. Guarda el instrumento visible en
   `08_EVALUACION/VCF_EXAMEN_UD<NN>_2026-2027_V01_BORRADOR.md` y el
   solucionario en un archivo **separado**:
   `08_EVALUACION/VCF_EXAMEN_UD<NN>_2026-2027_V01_BORRADOR_SOLUCIONARIO.md`.

## Salidas

Instrumento(s) + solucionario en `08_EVALUACION/`.

## Límites

El solucionario nunca va en el mismo archivo que el examen visible para el
alumnado. Este comando no pondera notas ni decide calificaciones — eso es
exclusivamente manual del docente.

## Validación humana

Aprobación docente obligatoria (cambio explícito de `BORRADOR` a
`APROBADO` en el nombre de archivo) antes de aplicar el examen al
alumnado.
