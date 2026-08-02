# Plantilla de la planificación semanal — artefacto HTML

Guía de diseño para el artefacto que genera `/asig-estado` en su modo
"planificación semanal" (ver `SKILL.md`). Reutiliza la marca ya fijada
para el resumen semanal; aquí solo se describe la estructura propia de
este modo.

## Marca

Misma paleta, tokens semánticos y tipografía que
`plantilla_resumen_semanal.md` (sección "Marca") — no la dupliques aquí.

## Estructura de la página

1. **Cabecera** (fondo `--azul-noche`, texto blanco): título
   "Planificación semanal · Formdepor", rango de fechas lunes-domingo de
   la semana que empieza, fecha de generación.
2. **Una sección por asignatura**, en el orden de `ASIGNATURAS/*`
   (alfabético). Cada sección es una tarjeta independiente con:
   - Nombre de la asignatura y ciclo.
   - Agenda de la semana (lista de sesiones con fecha y unidad).
   - Materiales necesarios, tareas `BORRADOR` a publicar, huecos de
     contenido y exámenes/solucionarios pendientes, cada uno como su
     propio sub-bloque con checklist (mismo formato de casilla calculada
     que ya usa el resumen semanal — ver esa plantilla, sección
     "Casillas").
   - Si ninguno de los cuatro sub-bloques tiene elementos para esa
     asignatura, una línea "Nada pendiente de preparar esta semana" en
     `--al-dia`.
3. **Prioridades de preparación**: un bloque final único (no repetido
   por asignatura), con la lista ordenada de todo el documento,
   numerada, en un contenedor visualmente distinto (fondo
   `--azul-formacion` suave o borde de acento) para que destaque como el
   resumen accionable de la página.
4. **Pie**: misma frase que ya usa el resumen semanal sobre recálculo
   desde cero y ausencia de persistencia de casillas, más la fecha/hora
   de generación.

## Responsive y overflow

Una sola columna en móvil, hasta dos columnas de tarjetas de asignatura
en pantallas anchas — mismo criterio que `plantilla_resumen_semanal.md`.

## Qué NO hacer

- No fusiones esto con el contenido del resumen semanal (viernes): son
  dos artefactos y dos borradores de Gmail distintos, aunque compartan
  fuente de datos.
- No inventes una prioridad de preparación que no se derive de uno de
  los cuatro sub-bloques (materiales, tareas, huecos, exámenes) — la
  lista final es una reordenación de lo ya calculado, no contenido
  nuevo.
- No inventes datos de alumnado ni toques
  `10_DIVERSIDAD/`/`11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/`.
- No declares capacidades `mcp` ni `downloads` en este artefacto.
