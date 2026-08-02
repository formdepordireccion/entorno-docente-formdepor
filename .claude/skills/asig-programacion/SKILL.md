---
name: asig-programacion
description: Cierra la programación didáctica 26/27 de la asignatura resuelta a partir de su borrador existente y de su ficha.yaml, y genera el calendario de temporalización (unidades, evaluaciones, entregas, recuperación) descontando festivos y no lectivos de Extremadura. Úsalo cuando el usuario pida programación, temporalización o calendario del curso 26/27.
---

# /asig-programacion — Planificación y temporalización

## Rol

Genera los planes anual/trimestral y el calendario de unidades y
evaluaciones del curso 2026-2027, descontando festivos, vacaciones y días
no lectivos de Extremadura.

## Entradas

- `ficha.yaml`: `resultados_aprendizaje`, `criterios_evaluacion`,
  `contenidos`, `asignatura.horas_totales`, `asignatura.horas_semanales`.
  Si estos campos están vacíos, avisa al usuario de que conviene ejecutar
  `/asig-normativa` antes, pero puedes continuar con lo que el usuario te
  dé directamente si insiste.
- El borrador de programación 26/27 de la asignatura resuelta, en su
  carpeta histórica del proyecto (p. ej. `3. VALORACIÓN 25_26/o.
  programación 26_27/1.Modulo Profesional Valoracion de la CF_Mario_Curso
  2026-2027.md` para VCF; `3. METODOLOGÍA 25_26/1.Modulo_Profesional_
  Metodologia_Mario_Curso_2026-2027_programación.md` para MET), si
  existe.
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
7. Genera también, siempre, `04_TEMPORALIZACION/calendario_visual_<curso>.html`
   — un calendario interactivo (navegación mes a mes, franja resumen del
   curso completo, panel de detalle por unidad con sus RA y materiales
   generados, leyenda filtrable) igual al ya usado en VCF y MET. No es
   opcional ni se pregunta si se quiere: es una salida más de este comando,
   igual que `calendario_26_27.md`.

   Usa siempre la plantilla y el script compartidos por el departamento
   (mismo motor CSS+JS para todas las asignaturas, no lo reescribas a
   mano):
   - Plantilla: `.claude/skills/asig-programacion/templates/calendario_visual_template.html`
   - Generador: `.claude/skills/asig-programacion/scripts/generar_calendario_visual.py`

   Pasos:
   a. Construye un JSON de configuración (puedes escribirlo en el
      scratchpad de la sesión, no hace falta guardarlo en el repositorio)
      con esta forma exacta:
      ```json
      {
        "titulo_pagina": "<CODIGO> · Calendario visual <curso>",
        "eyebrow": "<CODIGO>/<CICLO> · Formdepor",
        "curso_academico": "2026-2027",
        "subtitulo": "Temporalización, reparto de contenidos y evaluaciones · <nombre completo de la asignatura> (<CODIGO>)",
        "estado_badge": "BORRADOR",
        "rango_curso_largo": "<inicio corto> – <fin corto>",
        "dias_lectivos_texto": "<días de la semana con clase, en texto>",
        "fecha_fin_lectivo_larga": "<fecha larga de fin del periodo lectivo regular>",
        "fuente_calendario_oficial": "<cita de la resolución de calendario escolar>",
        "fuente_evaluacion_final": "<cita de la resolución para las fechas de evaluación final>",
        "footer_html": "<párrafo HTML explicando cómo leer el calendario, fuentes, estado y limitaciones conocidas>",
        "unit_color": {"UD00": "#hex", "UD01": "#hex", "...": "..."},
        "data": {
          "generado": "<fecha de hoy>",
          "cursoInicio": "YYYY-MM-DD",
          "cursoFin": "YYYY-MM-DD",
          "totalSesiones": 0,
          "unidades": [
            {"id": "UD00", "nombre": "...", "ra": ["RA1"], "inicio": "YYYY-MM-DD", "fin": "YYYY-MM-DD", "trimestre": 1, "tipo": "unidad", "archivo_base": "UD00", "sesiones": 0, "nota": "(opcional)", "raDetalle": [{"id": "RA1", "texto": "...", "bloque": "..."}], "materiales": {"unidad": true, "temario": 6, "tareas": 9, "examen": true, "recursos": false}, "actividadesPorSesion": {"1": [{"titulo": "...", "categoria": "Actividades iniciales", "archivo": "../../07_ACTIVIDADES_TAREAS/VIGENTE/1_ACTIVIDADES_INICIALES/<CODIGO>_TAREA_UD00_1_<curso>_V01_APROBADO.md"}]}, "actividadesFlexibles": [{"titulo": "...", "categoria": "Actividades de refuerzo", "archivo": "../../07_ACTIVIDADES_TAREAS/VIGENTE/10_ACTIVIDADES_REFUERZO/<CODIGO>_TAREA_UD00_8_<curso>_V01_APROBADO.md"}]},
            {"id": "EVAL-T1", "nombre": "Evaluación y repaso — 1ª evaluación", "ra": [], "inicio": "YYYY-MM-DD", "fin": "YYYY-MM-DD", "trimestre": 1, "tipo": "evaluacion", "sesiones": 0}
          ],
          "finales": [{"id": "FINAL-ORD", "nombre": "Evaluación final ordinaria", "fecha": "YYYY-MM-DD", "tipo": "final"}, {"id": "FINAL-EXT", "nombre": "Evaluación final extraordinaria", "fecha": "YYYY-MM-DD", "tipo": "final"}],
          "dias": [{"fecha": "YYYY-MM-DD", "weekday": 0, "tipo": "unidad|evaluacion|recuperacion|festivo|final|no_lectivo_semanal|sin_asignar", "bloqueId": "UD00", "etiqueta": "...", "numSesionBloque": 1}]
        }
      }
      ```
      El array `dias` debe cubrir **cada día natural** entre `cursoInicio`
      y `cursoFin` (no solo los lectivos): usa `tipo: "no_lectivo_semanal"`
      para los días de la semana sin clase de esta asignatura y fines de
      semana, `tipo: "festivo"` con `etiqueta` para los no lectivos del
      calendario oficial, y `tipo: "sin_asignar"` para huecos sin unidad
      asignada. Reutiliza exactamente los mismos datos día a día, unidades,
      RA y sesiones que ya calculaste para `calendario_26_27.md` — nunca
      inventes un segundo cálculo independiente que pueda desincronizarse
      del documento `.md`. El campo `materiales` de cada unidad se
      construye comprobando (con `find`/`ls`, no de memoria) qué existe ya
      en `05_UNIDADES/`, `06_TEMARIO/VIGENTE/`, `07_ACTIVIDADES_TAREAS/VIGENTE/`,
      `08_EVALUACION/` y `09_RECURSOS_DIGITALES/` para esa unidad — no lo
      des por hecho.

      Los campos `actividadesPorSesion` y `actividadesFlexibles` de cada
      unidad se construyen leyendo, para cada tarea ya generada de esa
      unidad en cualquier subcarpeta de `07_ACTIVIDADES_TAREAS/VIGENTE/`
      (`BORRADOR` o `APROBADO`, ambos cuentan), la línea `**Sesión(es)
      sugerida(s):** ...` que define `/asig-tarea` justo tras la cabecera
      de estado — no la infieras del contenido de la tarea, usa
      literalmente ese campo. Si el valor es un número (`N`) o un rango
      (`N-M`), la tarea va en `actividadesPorSesion`, bajo la clave de
      cada número de sesión que cubra (un rango `2-3` aparece tanto en
      `"2"` como en `"3"`); si el valor es `flexible (...)`, la tarea va
      en `actividadesFlexibles` en su lugar. Cada entrada lleva `titulo`
      (el título de la tarea, sin el prefijo "TAREA UDxx-n —"),
      `categoria` (el nombre legible de su subcarpeta, p. ej.
      "Actividades iniciales" para `1_ACTIVIDADES_INICIALES/`) y
      `archivo` con la ruta relativa desde
      `04_TEMPORALIZACION/calendario_visual_<curso>.html` hasta el
      archivo de la tarea (típicamente
      `../../07_ACTIVIDADES_TAREAS/VIGENTE/<N_CARPETA>/<archivo>.md`). Si
      una unidad todavía no tiene tareas generadas, omite ambos campos o
      déjalos vacíos — no inventes actividades de relleno.
   b. Ejecuta:
      ```
      python3 .claude/skills/asig-programacion/scripts/generar_calendario_visual.py \
        RUTA_AL_JSON_CONFIG.json \
        "DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/04_TEMPORALIZACION/calendario_visual_<curso>.html"
      ```
   c. Comprueba que el script no avisa de marcadores sin sustituir y que
      `totalSesiones`/el número de unidades del HTML generado coinciden
      con `calendario_26_27.md` antes de darlo por bueno.

   Si en el futuro se necesita ajustar el aspecto visual (colores,
   layout, textos fijos de la interfaz) para **todas** las asignaturas a
   la vez, edita la plantilla compartida, no el HTML ya generado de una
   asignatura concreta.
8. Actualiza `ficha.yaml → unidades` con la lista de unidades y sus
   fechas de inicio/fin previstas. `estado` permanece en `borrador`.

## Salidas

`programacion_26_27.md`, `calendario_26_27.md`,
`calendario_visual_<curso>.html`, `ficha.yaml` actualizado.

## Límites

No inventa fechas de festivos sin fuente verificada — si no puede
confirmarlas, las marca como "pendiente de verificar por el docente" en
vez de asumir un calendario genérico. No fija ponderaciones de
calificación sin que el docente las confirme.

## Validación humana

El docente debe aprobar la programación y el calendario (pasar
`estado` a `aprobado` explícitamente) antes de subirlos a Drive/Calendar.
