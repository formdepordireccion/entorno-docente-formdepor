# Plantilla del informe diario — artefacto HTML

Guía de diseño para el artefacto que genera `/asig-estado` en su modo
"informe diario" (ver `SKILL.md`). Reutiliza la marca ya fijada para el
resumen semanal; aquí solo se describe la estructura propia de este
modo.

## Marca

Misma paleta, tokens semánticos y tipografía que
`plantilla_resumen_semanal.md` (sección "Marca") — no la dupliques aquí,
reutilízala tal cual, incluido el tratamiento de tema oscuro/claro.

## Estructura de la página

1. **Cabecera** (fondo `--azul-noche`, texto blanco): título "Informe
   diario · Formdepor", fecha de hoy en formato largo (p. ej. "Martes 3
   de septiembre de 2026").
2. **Agenda del día**: una tarjeta por asignatura con clase hoy (si
   ninguna tiene clase hoy, una línea "Sin clases hoy" en `--gris-texto`
   y el resto de la página se omite salvo el pie) con unidad, sesión,
   actividades previstas (si las hay) y el material pendiente de
   revisar antes de clase.
3. **Alertas críticas**: lista con icono `--urgente` por cada hallazgo;
   si no hay ninguno, una línea "Sin alertas" en `--al-dia`. El aviso de
   día no lectivo (si aplica) va aquí también, pero con un tono neutro
   (no `--urgente`, es informativo).
4. **Próximos 7 días**: mismo formato de checklist con casilla calculada
   que ya usa el resumen semanal (ver esa plantilla, sección
   "Casillas") — un único bloque, sin distinguir "esta semana"/"la
   semana que viene".
5. **Semáforo de asignaturas**: una fila compacta por asignatura con su
   color (rojo/ámbar/verde) y una palabra de estado ("Alto", "Medio",
   "Bajo").
6. **Acción prioritaria**: bloque destacado al final, antes del pie —
   fondo `--urgente` si hay una acción concreta, `--al-dia` si la frase
   dice que no hay ninguna urgente hoy.
7. **Pie**: misma frase que ya usa el resumen semanal sobre recálculo
   desde cero y ausencia de persistencia de casillas, más la fecha/hora
   de generación.

## Responsive y overflow

Una sola columna en móvil (pensado para consultarse justo antes de
salir de casa); en pantallas anchas, las tarjetas de "Agenda del día"
pueden ir en dos columnas si hay más de una asignatura con clase hoy.

## Qué NO hacer

- No repitas el contenido del informe completo ni del resumen semanal
  (30/45 días, incoherencias detalladas) — este artefacto es solo "qué
  toca hoy y qué requiere atención".
- No inventes actividades de sesión si `actividadesPorSesion` no existe
  todavía para esa unidad — indica solo unidad y sesión.
- No inventes datos de alumnado ni toques
  `10_DIVERSIDAD/`/`11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/`.
- No declares capacidades `mcp` ni `downloads` en este artefacto — no
  hace falta ninguna.
