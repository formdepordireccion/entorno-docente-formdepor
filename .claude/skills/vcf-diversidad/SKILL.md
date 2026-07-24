---
name: vcf-diversidad
description: Elabora planes de adaptación curricular (PAC) reales a partir de los informes de alumnado con necesidades especiales guardados en 10_DIVERSIDAD/INFORMES_ALUMNADO/. Trabaja con datos personales de salud/discapacidad reales — nunca sube nada a git ni a Drive/Calendar. Úsalo cuando el usuario pida elaborar, actualizar o consultar un plan de adaptación curricular para un alumno o alumna concretos.
---

# /vcf-diversidad — Atención a la diversidad individual (VCF/TSEAS)

## Rol

A diferencia de las medidas genéricas de diversidad que ya incluye cada
unidad (`/vcf-unidad`), este comando trabaja con casos reales: lee los
informes de alumnado con necesidades especiales y elabora un plan de
adaptación curricular (PAC) concreto, cruzado con las unidades y
criterios reales de la asignatura.

**Maneja datos personales de salud/discapacidad reales.** Esto es una
excepción explícita y deliberada a la regla general del proyecto de "no
inventar ni usar datos personales" — aquí no se inventan, se usan los que
el docente ha aportado legítimamente, con el máximo cuidado.

## Entradas

- `10_DIVERSIDAD/INFORMES_ALUMNADO/` — informes reales (PDF/DOCX/imágenes)
  aportados por el docente.
- `ficha.yaml` (unidades, RA, criterios) y `05_UNIDADES/*APROBADO*.md`
  (unidades ya aprobadas, para adaptar sobre una base real).

## Tareas

1. Lee el informe o informes indicados por el docente (o todos los de
   `INFORMES_ALUMNADO/` si no se especifica ninguno).
2. Extrae **solo las implicaciones funcionales para la docencia**: qué
   necesita el alumno o alumna en el aula/instalación deportiva (más
   tiempo, apoyo visual, adaptación de esfuerzo físico, pausas,
   alternativas a una prueba concreta, etc.) — no reproduzcas el
   diagnóstico médico/psicopedagógico completo ni datos clínicos que no
   sean necesarios para decidir la adaptación docente.
3. Cruza esas necesidades contra las unidades reales (`ficha.yaml →
   unidades`, `05_UNIDADES/`): para cada unidad donde la necesidad tenga
   impacto real, propone una adaptación concreta (de actividad, de
   instrumento de evaluación, de tiempos, de instalación/equipamiento).
4. Genera el plan de adaptación curricular en
   `10_DIVERSIDAD/PLANES_ADAPTACION/PAC_<identificador-corto>_2026-2027.md`,
   usando un identificador corto que el propio docente indique (nunca el
   nombre completo del alumno o alumna en el nombre de archivo).
5. El PAC incluye: necesidades funcionales (resumidas, no el informe
   completo), adaptaciones por unidad afectada, instrumentos de
   evaluación adaptados si aplica, y una referencia a dónde está el
   informe original (`INFORMES_ALUMNADO/`) para quien necesite consultar
   el detalle clínico completo.
6. Nunca modifica las unidades de `05_UNIDADES/` ni el temario — las
   medidas genéricas siguen ahí; el PAC es un documento aparte.

## Salidas

Un archivo PAC por alumno/a en `10_DIVERSIDAD/PLANES_ADAPTACION/`.

## Límites

- **Nunca** sube nada de `INFORMES_ALUMNADO/` ni de `PLANES_ADAPTACION/`
  a git, Google Drive o Google Calendar — están excluidos explícitamente
  de `/vcf-drive`, `/vcf-calendar-sync`, `/vcf-revision` y `/vcf-estado`.
  `.gitignore` ya los excluye a nivel de archivo; esto es una capa
  adicional a nivel de comando.
- Nunca copia texto clínico/diagnóstico literal más allá de lo
  estrictamente necesario para justificar una adaptación docente
  concreta — minimización de datos.
- Nunca menciona datos de un alumno o alumna al generar contenido
  *genérico* (`/vcf-unidad`, `/vcf-tema`, `/vcf-examen`) — si el docente
  pide mezclar ambas cosas, se le recuerda esta separación en vez de
  hacerlo.
- No inventa necesidades ni adapta nada sin un informe real de respaldo
  en `INFORMES_ALUMNADO/`.
- No decide por su cuenta si una adaptación es válida a efectos
  normativos/oficiales — el PAC es una propuesta de trabajo del docente,
  no un documento oficial del centro salvo que el propio centro lo
  adopte como tal.

## Validación humana

Obligatoria: el docente revisa cada PAC antes de aplicarlo. El propio
carácter confidencial de estos documentos hace que no tengan un estado
`BORRADOR`/`APROBADO` en el nombre de archivo como el resto — se
consideran siempre documentos de trabajo vivos, revisables en cualquier
momento.
