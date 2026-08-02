---
name: asig-tarea
description: Genera actividades y tareas nuevas para la asignatura resuelta, clasificadas en una de 11 categorías (iniciales, desarrollo, prácticas, proyectos, estudios de caso, trabajos individuales, trabajos grupales, debates, digitales, refuerzo, ampliación) y guardadas en la subcarpeta correspondiente de 07_ACTIVIDADES_TAREAS/VIGENTE/. Cada actividad queda vinculada a resultados de aprendizaje y criterios de evaluación reales. Úsalo cuando el usuario pida crear, diseñar o generar una actividad o tarea nueva de la asignatura resuelta.
---

# /asig-tarea — Actividades y tareas

## Rol

Genera actividades y tareas para el alumnado, clasificadas por tipo y
siempre vinculadas explícitamente a resultados de aprendizaje y
criterios de evaluación reales. Es al ámbito de "actividades y tareas"
lo que `/asig-tema` es al temario: reutiliza como inspiración lo que ya
existe en `07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/` (tareas de
cursos anteriores) en vez de partir siempre de cero, pero adapta el
resultado al currículo vigente de `ficha.yaml`.

## Las 11 categorías y sus carpetas

Cada actividad se guarda en exactamente una de estas subcarpetas de
`07_ACTIVIDADES_TAREAS/VIGENTE/` (cada una tiene su propio `README.md`
con la definición completa):

| # | Carpeta | Cuándo usarla |
|---|---|---|
| 1 | `1_ACTIVIDADES_INICIALES/` | Motivación/toma de contacto al empezar la unidad |
| 2 | `2_ACTIVIDADES_DESARROLLO/` | Construcción del contenido durante el desarrollo de la unidad (no es cierre ni toma de contacto) |
| 3 | `3_ACTIVIDADES_PRACTICAS/` | Práctica motriz/técnica guiada (ejecución física, estaciones, protocolos de destreza) |
| 4 | `4_PROYECTOS/` | Extendida en varias fases/sesiones a lo largo de la unidad (diseño → ejecución → evidencia) |
| 5 | `5_ESTUDIOS_CASO/` | Basada en un caso/escenario concreto que se analiza o resuelve |
| 6 | `6_TRABAJOS_INDIVIDUALES/` | Trabajo de una sola sesión/entrega, individual, que no es proyecto ni caso |
| 7 | `7_TRABAJOS_GRUPALES/` | Trabajo de una sola sesión/entrega, en grupo, que no es proyecto ni caso |
| 8 | `8_DEBATES/` | Discusión/argumentación oral en grupo sobre un tema abierto |
| 9 | `9_ACTIVIDADES_DIGITALES/` | Requiere una herramienta digital (formulario, app, vídeo) como parte central |
| 10 | `10_ACTIVIDADES_REFUERZO/` | Repaso/consolidación de un RA/criterio ya trabajado, para quien lo necesita |
| 11 | `11_ACTIVIDADES_AMPLIACION/` | Profundización más allá del mínimo, para quien ya domina el RA/criterio |

**Criterio de desambiguación** cuando una actividad podría encajar en
más de una (p. ej. un proyecto en grupo es a la vez "proyecto" y
"trabajo grupal"): si tiene varias fases/sesiones extendidas en el
tiempo con una evidencia final, es **proyecto** (4) aunque sea en grupo
o individual; si tiene un caso/escenario concreto como eje central, es
**estudio de caso** (5) aunque tenga parte práctica; solo si no encaja
en ninguna de las categorías más específicas (1-5, 8-11) se usa
**trabajo individual/grupal** (6/7) como categoría por defecto según
número de sesiones (una) y formato (individual o grupo).

## Entradas

- Unidad (`UD<NN>`) y, si se especifica, categoría (1-11) para la que se
  pide la tarea. Si no se especifica la categoría, pregúntala o
  propónla tú mismo justificando la elección según la tabla de arriba.
- `ficha.yaml → resultados_aprendizaje`, `criterios_evaluacion`,
  `contenidos`, `unidades`.
- `07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/` como banco de referencia
  de tareas de cursos anteriores.
- Todas las subcarpetas de `07_ACTIVIDADES_TAREAS/VIGENTE/` (para no
  proponer un número de tarea ya usado dentro de la misma unidad,
  independientemente de en qué subcarpeta esté).

## Tareas

1. Si no se especifica, pregunta qué unidad (`UD<NN>`) y qué categoría
   (1-11) quiere el docente. Si el docente describe la actividad sin
   nombrar la categoría, clasifícala tú mismo con el criterio de
   desambiguación de arriba y dilo explícitamente ("la clasifico como
   proyecto porque...").
2. Busca en `07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/` tareas
   relacionadas con la misma unidad/RA en cursos anteriores. Si
   encuentras una tarea reutilizable, indícalo explícitamente y adáptala
   (actualiza cualquier referencia a contenidos/criterios que hayan
   cambiado respecto a la normativa vigente en `ficha.yaml`, y adapta
   también el horario/sesiones al calendario real 26/27) en vez de
   copiarla sin más. Si no encuentras nada, dilo explícitamente y genera
   la tarea desde `ficha.yaml → contenidos`.
3. Redacta la tarea con: enunciado para el alumnado, categoría (1-11) y
   justificación breve de por qué encaja ahí, RA y criterio(s) concretos
   que evalúa (citados literalmente de `ficha.yaml`), tiempo estimado,
   recursos/material necesario, y criterios de entrega (qué se espera,
   en qué formato, individual o en grupo).
4. Incluye siempre, como línea propia justo después del párrafo de
   `**Estado: ...**` de la cabecera (antes de "Origen del material" o de
   cualquier otro contenido), el campo estructurado:
   `**Sesión(es) sugerida(s):** <N>` o `<N>-<M>` para un rango — usando
   el mismo número de sesión que ya manejas para redactar el resto de la
   tarea (fecha/sesión dentro de la unidad). Si la actividad es de
   repaso o ampliación **sin una sesión fija** (se aplica cuando el
   docente lo considere, no ligada a un día concreto), usa en su lugar:
   `**Sesión(es) sugerida(s):** flexible (repaso/ampliación sin sesión
   fija — a criterio del docente, no ligada a un día concreto del
   calendario)`. Este campo es el que `/asig-programacion` lee
   literalmente para volcar la propuesta de actividades al calendario
   visual — mantén el formato exacto (negrita, dos puntos, sin variarlo)
   para que siga siendo extraíble automáticamente.
5. Numera la tarea siguiendo la secuencia ya usada para esa unidad en
   **cualquier** subcarpeta de `07_ACTIVIDADES_TAREAS/VIGENTE/` (revisa
   las 11 antes de asignar un número, para no duplicar entre
   categorías).
6. Guarda como
   `07_ACTIVIDADES_TAREAS/VIGENTE/<N_CARPETA>/<CODIGO>_TAREA_UD<NN>_<N>_2026-2027_V01_BORRADOR.md`,
   donde `<CODIGO>` es el código de la asignatura (resuelto según CLAUDE.md → "Cómo se resuelve la asignatura"), `<N_CARPETA>` es la subcarpeta de la categoría elegida,
   `<NN>` es la unidad y `<N>` el número de tarea dentro de esa unidad
   (independiente de la categoría).

## Salidas

Un archivo de tarea en la subcarpeta de `07_ACTIVIDADES_TAREAS/VIGENTE/`
que corresponda a su categoría, por tarea generada.

## Límites

No inventa un vínculo con un RA/criterio que la tarea en realidad no
evalúa. Si reutiliza una tarea histórica, lo dice explícitamente (qué
tarea de qué curso se usó como base) en vez de presentarla como
completamente nueva. El archivo se guarda siempre en `BORRADOR`. Nunca
crea una categoría nueva sobre la marcha — si una actividad no encaja
bien en ninguna de las 11, se lo dice al docente en vez de forzarla o
inventar una carpeta 12.

## Validación humana

La tarea queda en `BORRADOR` hasta que el docente la revise y apruebe
(vía `/asig-revision`, igual que unidades/temario/exámenes).
