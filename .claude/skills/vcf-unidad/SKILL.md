---
name: vcf-unidad
description: Genera o actualiza una unidad didáctica completa de VCF (justificación, objetivos, RA, criterios, contenidos, metodología, actividades, recursos, diversidad, evaluación, recuperación, ampliación) y la guarda en 05_UNIDADES con la nomenclatura oficial. Úsalo cuando el usuario pida crear, redactar o revisar una unidad didáctica de VCF.
---

# /vcf-unidad — Diseño de unidades didácticas (VCF/TSEAS)

## Rol

Genera unidades didácticas completas de VCF, vinculadas a los resultados
de aprendizaje y criterios de evaluación registrados en `ficha.yaml`.

## Entradas

- `ficha.yaml`: `resultados_aprendizaje`, `criterios_evaluacion`,
  `contenidos`, `unidades`, `calendario_ref`.
- Número o nombre de unidad que pida el usuario (si no lo da, pregúntalo).
- `06_TEMARIO/REFERENCIA_HISTORICA/` como posible fuente de inspiración
  para actividades y enfoque, si ya contiene material relevante.

## Tareas

1. Si el usuario no especifica qué unidad, pregúntale número/nombre y qué
   contenidos/RA de `ficha.yaml` debe cubrir.
2. Redacta la unidad con estas secciones obligatorias:
   - Justificación (por qué esta unidad, relación con el resto del curso)
   - Duración en sesiones (usa `04_TEMPORALIZACION/calendario_26_27.md`
     si existe para ajustar el número real de sesiones disponibles)
   - Objetivos
   - Resultados de aprendizaje y criterios de evaluación vinculados
     (copiados literalmente de `ficha.yaml`, citando cuáles aplican)
   - Contenidos
   - Metodología (elige según el tipo de contenido: motriz, teórico,
     práctico — justifica la elección en una frase)
   - Actividades: inicio/motivación, desarrollo, prácticas
   - Recursos necesarios
   - Atención a la diversidad: medidas genéricas (DUA, agrupamientos
     flexibles, materiales alternativos, graduación de dificultad) — nunca
     menciones alumnos concretos ni diagnósticos
   - Evaluación e instrumentos, con evidencias esperadas
   - Actividades de recuperación y de ampliación
3. Guarda el resultado en
   `05_UNIDADES/VCF_UNIDAD_UD<NN>_2026-2027_V01_BORRADOR.md`, donde `<NN>`
   es el número de unidad con dos dígitos (p. ej. `UD03`).
4. Actualiza `ficha.yaml → unidades`: si la unidad ya existía en la lista,
   añade/actualiza el campo `archivo` con la ruta generada; si no existía,
   añade una entrada nueva `{nombre, archivo}`.

## Salidas

Archivo de unidad en `05_UNIDADES/`, `ficha.yaml` actualizado.

## Límites

La sección de diversidad usa exclusivamente medidas genéricas aplicables a
cualquier grupo — nunca datos personales ni diagnósticos de alumnado
concreto. El archivo se guarda siempre en estado `BORRADOR`.

## Validación humana

La unidad queda en `BORRADOR` hasta que el docente la revise. Si el
docente confirma que está lista, renombra el archivo cambiando
`V01_BORRADOR` por `V01_APROBADO` (o la versión que corresponda) y haz un
commit específico para esa aprobación.
