# Centro de Control Docente — registro vivo de documentos

Fecha: 2026-07-31
Estado: Aprobado por el usuario, pendiente de implementación

## Contexto y alcance

El docente trajo una propuesta externa (documento "arquitectura
automatizada.pdf", generado por otra herramienta/IA fuera de este proyecto)
que recomienda evolucionar el entorno docente hacia un "sistema operativo
docente real": un registro central por documento, un "Centro de Control
Docente" (hoja maestra de 5 pestañas), rutinas de información diarias/
semanales/mensuales/trimestrales, una lista de qué automatizar primero, y
una taxonomía de 8 estados documentales que sustituiría el ciclo
`BORRADOR`/`APROBADO` actual.

Ese documento describe **cuatro cambios independientes**, y él mismo
recomienda no construirlo todo a la vez:

- **A. Modelo de registro por documento** (qué campos, de dónde salen).
- **B. Centro de Control Docente** como hoja maestra en Drive.
- **C. Rutinas de información** (diario, semanal, mensual, trimestral).
- **D. Taxonomía de 8 estados documentales**, sustituyendo `BORRADOR`/
  `APROBADO`.

Este spec cubre **solo A+B**, y dentro de B, solo dos de las cinco pestañas
originales (**Documentos** y **Panel general** como resumen calculado sobre
esa). Quedan fuera explícitamente de este documento:

- **C (rutinas de información)**: el patrón "informe diario automático a
  las 07:15" tal como lo describe la propuesta no es viable en esta
  plataforma — no existe cron durable indefinido (`CronCreate` es de sesión,
  máximo 7 días). El patrón ya validado en este proyecto es un recordatorio
  de Google Calendar que el propio docente dispara abriendo Claude Code
  (así funcionan ya `/asig-mantenimiento` y el modo resumen semanal de
  `/asig-estado`). Encajar las cinco rutinas de la propuesta en ese patrón,
  decidiendo cuáles merecen de verdad su propio recordatorio, es su propio
  diseño posterior.
- **D (8 estados documentales)**: cambio de gran alcance — tocaría la
  nomenclatura de cada archivo ya `APROBADO` en VCF y MET, cada skill de
  "la fábrica" y `/asig-revision` entero. Se deja como decisión aparte,
  a tomar cuando ya se sepa qué campos necesita de verdad el registro real
  (este mismo spec, una vez implementado y usado, informará esa decisión).
- **Pestañas "Plan docente" y "Evaluación"** de la propuesta original:
  - "Plan docente" (sesiones previstas vs. impartidas) necesita empezar a
    registrar si una sesión concreta se dio de verdad o no — un dato que
    hoy no existe en ningún sitio del proyecto.
  - "Evaluación" tal como está planteada en la propuesta ("calificaciones
    pendientes de registrar") choca directamente con la regla 3 de
    `CLAUDE.md`: `11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/` contiene datos
    reales de alumnado y **nunca sale de este disco local**, sin excepción.
    Una hoja en Drive no puede mostrar nada derivado de esa carpeta.

## Decisiones de diseño (resumen de la conversación de brainstorming)

1. **"Vivo" significa recalculado bajo demanda, no una hoja que se
   actualiza sola en tiempo real.** Cada vez que se ejecuta, el sistema
   relee el repositorio desde cero y regenera el registro entero — mismo
   patrón que ya usan `/asig-estado` y `/asig-mantenimiento`. Construir algo
   "verdaderamente en vivo" dentro de Google Sheets exigiría Apps Script u
   otro conector nuevo, infraestructura ajena a este entorno y descartada.
2. **Cubre las dos asignaturas desde el principio** (VCF y MET), no una
   asignatura piloto — mismo patrón multi-asignatura que ya usa
   `/asig-estado`.
3. **Alcance de documentos: el mismo universo que `/asig-revision`.** Los 4
   documentos base (normativa, matriz, programación, calendario) + unidades
   didácticas + temario + actividades/tareas + evaluación + recursos
   digitales — es decir, todo lo que pasa por el ciclo `BORRADOR`/
   `APROBADO`. Queda fuera el material migrado de `REFERENCIA_HISTORICA`
   (no tiene ciclo de estado) y, como siempre, las tres carpetas de datos
   personales.
4. **Limitación de herramienta confirmada: no hay forma de sobrescribir una
   hoja de Drive existente ni de borrar archivos.** El conector de Drive
   disponible solo puede crear archivos nuevos. Por tanto, la fuente real
   del registro vive en el repositorio (Markdown, versionado en git, mismo
   patrón que `estado_<fecha>.md`), y la publicación a Drive —si se pide—
   es siempre un archivo nuevo con fecha, nunca una única hoja fija que se
   actualiza sola.
5. **Vive como un tercer modo de `/asig-estado`**, no como una skill nueva.
   `/asig-estado` ya es "coordinador de asignaturas, no genera contenido,
   solo informa" y ya tiene dos modos (informe completo, resumen semanal);
   este es un tercero ("registro"). Evita duplicar la lógica de lectura de
   `ficha.yaml`/carpetas que la skill ya tiene, y evita sumar una
   decimosexta skill con responsabilidades solapadas.
6. **"Fecha de próxima revisión" solo cuando hay una regla real detrás**,
   nunca inventada ni tecleada a mano (no sobreviviría al recálculo desde
   cero). Reutiliza dos reglas que el proyecto ya aplica en otro sitio: el
   umbral de 15 días de `BORRADOR` estancado de `/asig-mantenimiento`, y la
   fecha de inicio de la próxima unidad desde `ficha.yaml` que ya usa
   `/asig-estado`. Fuera de esos dos casos, el campo queda vacío.
7. **RA/criterios: cita literal cuando el documento la tiene, si no el RA
   completo de la unidad.** Tareas y exámenes ya citan el criterio exacto
   dentro de su propio texto (ej. "RA1.b") — se extrae esa cita. Unidades,
   temario, recursos digitales y documentos base no citan con esa
   granularidad — se usa el RA completo de `ficha.yaml → unidades[].ra`
   para esa unidad.
8. **Enlace al archivo: Drive si existe, aviso explícito si no.** Pensado
   para poder revisar el registro fuera de Claude Code (incluso desde
   el móvil). Si el documento todavía no se subió (`BORRADOR`, o
   `APROBADO` pendiente de subida manual como los `.pptx`), el campo dice
   "no subido a Drive" en vez de un enlace roto o inconsistente.

## Arquitectura

### Modelo de datos — tabla "Documentos"

Una fila por documento, doce campos:

| Campo | Origen |
|---|---|
| Asignatura | ruta del archivo / `ficha.yaml → asignatura.codigo` |
| Unidad | ruta del archivo (token `UD<NN>` del nombre) o "—" para los 4 documentos base |
| Tipo de documento | carpeta contenedora (unidad, temario, tarea, examen, recurso digital, documento base) |
| Curso académico | `ficha.yaml → asignatura.curso_academico` |
| Estado | `BORRADOR`/`APROBADO` extraído del nombre de archivo (o del marcador de cabecera, para los 4 documentos base) |
| Versión | token `V0X` del nombre de archivo |
| Fecha de última revisión | fecha de última modificación del archivo (git) |
| Fecha de próxima revisión | ver decisión 6 — puede quedar vacío |
| RA / Criterios relacionados | ver decisión 7 |
| Enlace al archivo | ver decisión 8 |
| Observaciones | avisos ya detectables en el propio documento: `[NUEVO]`, "pendiente de verificación manual", "sin respaldo histórico", discrepancias — misma extracción que ya hace `/asig-revision` al presentar sus tablas |
| Acción pendiente | derivada de Estado + Observaciones (p. ej. "revisar y aprobar en `/asig-revision`", "actualizar tras drift de normativa detectado por `/asig-mantenimiento`", "subir a Drive") |

### Vista "Panel general"

Una fila por asignatura, calculada agregando las filas de "Documentos" de
esa asignatura — no una fuente de datos independiente:

| Campo | Cálculo |
|---|---|
| Asignatura | — |
| % Preparación | documentos `APROBADO` ÷ total de documentos esperados (mismo criterio de "huecos de contenido" que ya usa `/asig-estado`) |
| Unidad actual | unidad cuyo rango de fechas (`ficha.yaml → unidades[].fechas`) contiene la fecha de hoy |
| Próxima evaluación | próximo examen en `08_EVALUACION/` según el calendario de la asignatura |
| Pendientes | recuento de filas de "Documentos" con "Acción pendiente" no vacía |
| Riesgo | heurística simple: Alto si hay algún `BORRADOR` estancado (>15 días) próximo a usarse, o incoherencias sin resolver de `/asig-mantenimiento`; Medio si hay pendientes pero sin urgencia; Verde/Bajo si no hay ninguno |

### Mecánica de generación

1. **Disparo:** a demanda ("actualiza el centro de control", "genera el
   registro de documentos"). Opcionalmente se puede encadenar a la misma
   ejecución que el resumen semanal ya disparado por Calendar, si el
   docente lo pide explícitamente en ese momento — no se añade un
   recordatorio de Calendar nuevo en este spec (eso es parte de C, fuera de
   alcance).
2. **Recorrido:** repite, para cada asignatura bajo `ASIGNATURAS/*/`, un
   barrido de los mismos documentos que ya recorre `/asig-revision`,
   extrayendo los doce campos de la tabla de arriba.
3. **Artefacto local (fuente real):**
   `DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/centro_control_<YYYY-MM-DD>.md`
   — un único archivo Markdown con dos secciones: "Panel general" primero
   (tabla corta, una fila por asignatura), "Documentos" después (tabla
   larga, agrupada por asignatura). Mismo patrón que `estado_<fecha>.md`
   que ya genera el informe completo de `/asig-estado`.
4. **Snapshot opcional a Drive:** si el docente lo pide en el momento, se
   genera además una versión CSV de cada tabla y se sube con
   `create_file` (conversión automática CSV → Google Sheet, mismo
   mecanismo ya usado para convertir Markdown → Google Doc). Cada snapshot
   es un archivo nuevo con fecha en el nombre — no existe una única hoja
   fija que se sobrescribe, por la limitación de herramienta de la
   decisión 4. El docente puede acumular o borrar snapshots antiguos desde
   la propia interfaz de Drive.

## Riesgos y mitigación

- **Riesgo: la tabla "Documentos" crece mucho** (VCF + MET ya suman más de
  250 archivos entre unidades, temario, tareas, exámenes y recursos).
  Mitigación: se agrupa por asignatura y por tipo de documento dentro del
  Markdown (igual que ya hace `/asig-revision`), y el "Panel general" da
  una vista resumida de una fila por asignatura para quien no necesite el
  detalle completo.
- **Riesgo: expectativa de "hoja fija que se actualiza sola"** que la
  propuesta original transmite pero que esta plataforma no puede ofrecer.
  Mitigación: este mismo spec (decisión 4) fija la fuente real en el
  repositorio y el snapshot de Drive como copia fechada, no como sustituto;
  hay que comunicarlo así también en la salida del propio comando (una
  línea explícita, mismo estilo que ya usa el resumen semanal para avisar
  de que "no hay persistencia de casillas").
- **Riesgo: "Acción pendiente" y "Riesgo" (Panel general) son heurísticas
  nuevas, no verificadas contra un caso real todavía.** Mitigación: probar
  primero contra VCF y MET tal como están hoy, y ajustar los umbrales si el
  resultado no coincide con lo que el docente esperaría ver.

## Fuera de alcance (siguiente paso, no parte de este plan)

- Las rutinas de información C (diario/semanal/mensual/trimestral) —
  requieren decidir, una por una, si merecen su propio recordatorio de
  Calendar y qué contenido mínimo justifica cada una.
- La taxonomía de 8 estados documentales D — decisión de gran alcance,
  aparte, a tomar después de usar este registro un tiempo.
- Las pestañas "Plan docente" (necesita registrar sesiones impartidas de
  verdad) y "Evaluación" (chocaría con la protección de datos de
  calificaciones tal como está planteada en la propuesta original).
- Añadir un recordatorio de Calendar nuevo para disparar este modo — se
  invoca a demanda por ahora; si el uso real lo justifica, se decide más
  adelante como parte de C.

## Siguiente paso

Invocar la skill `writing-plans` para convertir este diseño en un plan de
implementación paso a paso (que incluirá la actualización de
`.claude/skills/asig-estado/SKILL.md` con el tercer modo).
