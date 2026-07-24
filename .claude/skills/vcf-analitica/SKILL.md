---
name: vcf-analitica
description: Analiza calificaciones reales del alumnado de VCF por RA/criterio para detectar patrones de error y generar informes agregados. NO EJECUTABLE TODAVÍA — no hay calificaciones reales cargadas (el curso 2026-2027 no ha empezado). Úsalo cuando el usuario pida analizar resultados, calificaciones o rendimiento de VCF; si no hay datos, informa de ello en vez de generar nada.
---

# /vcf-analitica — Analítica y mejora (VCF/TSEAS)

## Estado: esqueleto, sin ejecutar

Este comando define el formato y el proceso, pero **no tiene datos reales
que analizar todavía** — el curso 2026-2027 aún no ha empezado y no
existen calificaciones. Está aquí para no tener que diseñarlo desde cero
cuando lleguen las primeras notas.

## Rol

Analiza calificaciones reales por criterio de evaluación para detectar
qué se falla más, cómo evoluciona el rendimiento por evaluación, y qué
RA necesitan refuerzo — sin identificar nunca a un alumno o alumna
concretos en el resultado.

## Entradas

- `11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/` — calificaciones reales,
  una vez existan. Formato propuesto (un archivo YAML por instrumento de
  evaluación aplicado):

  ```yaml
  unidad: UD02
  instrumento: 08_EVALUACION/VCF_EXAMEN_UD02_2026-2027_V01_APROBADO.md
  fecha_aplicacion: "2026-12-10"
  calificaciones:
    - alumno_id: "A01"          # identificador/pseudónimo, nunca el nombre completo
      respuestas:
        - criterio: "RA1.a"
          resultado: correcta   # correcta | incorrecta | parcial
        - criterio: "RA1.b"
          resultado: incorrecta
      nota_final: 7.2
  ```

  El mapeo `alumno_id` → nombre real, si existe, vive fuera de este
  proyecto (p. ej. en la aplicación de gestión académica del centro) —
  este comando nunca lo necesita ni lo guarda.

- `ficha.yaml → criterios_evaluacion` (para saber qué cubre cada
  criterio).

## Tareas

1. **Primero, comprueba si hay datos.** Si
   `11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/` está vacía (salvo el
   README), dilo explícitamente: "No hay calificaciones cargadas
   todavía — nada que analizar." No generes ningún informe ni inventes
   cifras de ejemplo.
2. Si hay datos, agrégalos por criterio: % de aciertos/fallos por
   criterio, por RA, por unidad, y su evolución en el tiempo si hay más
   de una evaluación cargada.
3. Identifica los criterios con peor resultado agregado (candidatos a
   refuerzo) y los RA mejor cubiertos.
4. Genera un informe en
   `11_SEGUIMIENTO_RESULTADOS/INFORMES/informe_<fecha>.md` con las
   cifras agregadas y una propuesta de qué reforzar — nunca con datos
   por alumno individual identificable.
5. Si el usuario pide explícitamente un análisis a nivel de un alumno o
   alumna concretos, indícale que eso corresponde a `/vcf-diversidad`
   (si hay necesidades especiales de por medio) o a una conversación
   directa con el docente — este comando no genera análisis
   individualizados.

## Salidas

Informes agregados en `11_SEGUIMIENTO_RESULTADOS/INFORMES/`.

## Límites

**No ejecutable de forma útil hasta que existan calificaciones reales** —
no rellena con datos de ejemplo ni simula resultados para "mostrar cómo
quedaría". Nunca identifica a un alumno o alumna en el informe de salida,
aunque `alumno_id` esté presente en los datos de origen. No decide notas
ni pondera calificaciones — eso es exclusivamente manual del docente
(regla general del proyecto).

## Validación humana

El docente revisa el informe antes de usarlo para decisiones docentes
(refuerzo, repaso, ajuste de programación).
