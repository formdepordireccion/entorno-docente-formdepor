---
name: asig-estado
description: Genera una foto de estado de las asignaturas del departamento (rol de Coordinador / Centro de control) — qué falta en cada ficha.yaml, qué carpetas están vacías, próximos hitos del calendario, incoherencias detectadas, y qué unidades próximas necesitan material todavía. Incluye un modo de resumen semanal que publica un artefacto HTML visual por asignatura y deja un borrador en Gmail con el enlace. Úsalo cuando el usuario pida el estado, resumen, panel de control, "qué falta", qué preparar la semana que viene, o cuando toque el recordatorio semanal de Google Calendar (VCF · Resumen semanal).
---

# /asig-estado — Coordinador de las asignaturas del departamento

## Rol

Coordinador de asignaturas: supervisa todas las asignaturas que existan
bajo `DEPARTAMENTO_DOCENTE/ASIGNATURAS/` (hoy VCF y MET, pensado para
seguir creciendo), no genera contenido nuevo, solo informa. Tiene dos
modos: el informe completo bajo demanda (tareas 1-7 más abajo) y el
resumen semanal condensado y multi-asignatura (ver "Modo resumen
semanal").

El informe completo es uno de los comandos de solo lectura/informe que
forman la excepción de CLAUDE.md → "Cómo se resuelve la asignatura"
(punto 4): si el usuario pide "el estado" **sin mencionar ninguna
asignatura**, no pregunta cuál — recorre automáticamente **todas** las
que existan bajo `ASIGNATURAS/*/ficha.yaml`, generando un informe
completo e independiente de cinco bloques (ver tarea 6) por cada una. Si
el usuario sí menciona una asignatura concreta ("el estado de MET"), se
resuelve según esa misma sección de CLAUDE.md y el informe completo
cubre solo esa asignatura — sus cinco bloques, nada más. El resumen
semanal (ver "Modo resumen semanal") no sigue esta distinción: siempre
recorre todas las asignaturas existentes, se mencione una o no, porque
está pensado como una foto de arranque de semana de todo el
departamento a la vez.

## Entradas

- `DEPARTAMENTO_DOCENTE/ASIGNATURAS/*/00_FICHA/ficha.yaml` — una por
  asignatura existente.
- El contenido actual de las carpetas `01_NORMATIVA_CURRICULO/` a
  `14_HISTORICO_CAMBIOS/` dentro de cada `DEPARTAMENTO_DOCENTE/ASIGNATURAS/<ASIGNATURA>/`
- `04_TEMPORALIZACION/calendario_*.md` de cada asignatura, si existe
- La fecha actual

## Tareas

Repite los pasos 1-6 para cada asignatura cubierta en esta ejecución (ver
"Rol": todas las que existan bajo `ASIGNATURAS/*/ficha.yaml` si el
usuario no especificó ninguna, o solo la resuelta si especificó una). El
paso 7 es aparte, no se repite por asignatura.

1. Lee su `ficha.yaml` y lista qué campos siguen a `null` o `[]` (p. ej.
   `normativa.rd_estatal`, `resultados_aprendizaje`, `unidades`).
2. Recorre cada carpeta numerada de esa asignatura (excluyendo los
   `README.md`) y, por carpeta, indica si tiene contenido generado o está
   vacía. **Excepción:** `10_DIVERSIDAD/INFORMES_ALUMNADO/`,
   `10_DIVERSIDAD/PLANES_ADAPTACION/` y
   `11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/` contienen datos
   personales de alumnado — indica solo si tienen contenido o no
   (vacía/con documentos), nunca nombres de archivo ni ningún detalle de
   su contenido.
3. Si existe `04_TEMPORALIZACION/calendario_*.md` para esa asignatura,
   compáralo con la fecha actual y señala los hitos (unidades,
   evaluaciones, entregas) previstos en los próximos 30 días.
4. Detecta incoherencias simples:
   - Unidades listadas en `ficha.yaml → unidades` sin archivo
     correspondiente en `05_UNIDADES/`.
   - Archivos con `BORRADOR` en el nombre que llevan más de 30 días sin
     modificarse (usa la fecha de última modificación del archivo).
5. **Próxima preparación (propuesta semanal):** ordena
   `ficha.yaml → unidades` por `fechas.inicio` y localiza las 2-3
   unidades reales (con `archivo`, no bloques de evaluación) cuyo inicio
   caiga dentro de los próximos 45 días. Para cada una, comprueba qué
   material ya existe y cuál falta:
   - Unidad (`05_UNIDADES/`) → si falta, sugiere `/asig-unidad`.
   - Temario (`06_TEMARIO/VIGENTE/`, 6 archivos por unidad) → si falta o
     está incompleto, sugiere `/asig-tema`.
   - Actividades/tareas propias de esa unidad
     (`07_ACTIVIDADES_TAREAS/VIGENTE/`) → si no hay ninguna, sugiere
     `/asig-tarea` (aviso, no obligatorio).
   - Examen (`08_EVALUACION/`) → si falta, sugiere `/asig-examen`.
   - Recursos digitales (`09_RECURSOS_DIGITALES/`, cualquier
     subcarpeta) → si no hay ninguno, sugiere `/asig-recursos` (aviso, no
     obligatorio — a diferencia de unidad/temario/examen, no es
     obligatorio que exista).
   Ordena la lista por cercanía de fecha (lo más próximo primero), no
   por tipo de unidad.
6. Presenta el informe de esta asignatura como una unidad completa e
   independiente de cinco bloques: **Pendiente de revisión**, **Huecos
   de contenido**, **Próximos hitos**, **Incoherencias**, **Próxima
   preparación**. Si esta ejecución cubre más de una asignatura (ver
   "Rol" y la nota al principio de esta sección), no fusiones los
   bloques de distintas asignaturas en una sola lista compartida:
   presenta cada asignatura como su propia sección, claramente
   encabezada con su nombre, con sus cinco bloques completos dentro —
   un informe completo por asignatura, no un único juego de cinco
   bloques que simplemente menciona a varias asignaturas por dentro.
7. Si el usuario pide guardar el resumen, escríbelo en
   `DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/estado_<YYYY-MM-DD>.md` con la
   fecha de hoy — un único archivo que reproduce la misma estructura que
   el chat (una sección completa por asignatura si esta ejecución cubrió
   más de una).

## Modo resumen semanal (recordado por Calendar)

Un segundo modo, más corto y siempre visual, pensado para arrancar la
semana. No sustituye al informe completo (tareas 1-7): comparte la
misma lectura de datos pero condensa la ventana temporal y cambia la
salida.

1. **Disparo:** un evento semanal recurrente de Google Calendar
   ("VCF · Resumen semanal (/vcf-estado)", creado cuando solo existía
   VCF — el nombre del evento en sí no se renombra aquí, ver nota al
   final de esta sección —, igual de patrón que `/asig-mantenimiento`)
   recuerda al docente abrir Claude Code y ejecutar este modo. El
   evento es el único disparador — no hay ejecución en la nube por su
   cuenta; si nadie abre Claude Code esa semana, simplemente no se
   genera nada, y el evento vuelve a sonar la semana siguiente.
2. **Alcance:** recorre todas las asignaturas bajo
   `DEPARTAMENTO_DOCENTE/ASIGNATURAS/*/` (hoy VCF y MET). Cada
   asignatura es una sección independiente del artefacto — añadir una
   asignatura nueva más adelante no obliga a rediseñar nada, solo
   aparece una sección más.
3. **Ventana:** para cada asignatura, calcula una versión condensada de
   las tareas 1-5, pero centrada en lo urgente: hitos y unidades cuyo
   inicio cae en los próximos 14 días (no 30/45), separando
   explícitamente "esta semana" (hoy → +7 días) de "la semana
   siguiente" (+7 → +14 días).
4. **Casillas siempre calculadas, nunca manuales:** cada elemento de
   "huecos de contenido" y "próxima preparación" se marca como hecho o
   pendiente solo comprobando si el archivo esperado ya existe en el
   repositorio en el momento de generar el resumen (misma lógica que la
   tarea 5 del informe completo). El artefacto es una página estática
   sin backend — no hay ninguna casilla que el docente pueda marcar a
   mano y que se recuerde la semana siguiente; si algo sigue apareciendo
   como pendiente, es porque el archivo correspondiente sigue sin
   existir. Dilo así de explícito en el propio artefacto, para que no
   se espere una persistencia que no existe.
5. **Artefacto HTML:** construye la página siguiendo
   `.claude/skills/asig-estado/reference/plantilla_resumen_semanal.md`
   (paleta y tipografía FORMDEPOR, estructura por asignatura). Guarda
   primero el HTML en
   `DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/RESUMENES_SEMANALES/resumen_semanal_<YYYY-MM-DD>.html`
   (fecha del lunes de esa semana) y publícalo con la herramienta
   Artifact — cada semana es un archivo y una URL nueva, para que quede
   como registro histórico y no se pise el de la semana anterior.
6. **Borrador de Gmail:** crea un borrador (nunca lo envíes) a
   `formdepor.direccion@gmail.com` con `mcp__claude_ai_Gmail__create_draft`:
   asunto `Resumen semanal · Formdepor — semana del <DD/MM> al <DD/MM>`
   (mismo título de departamento que la cabecera del artefacto HTML, ver
   `reference/plantilla_resumen_semanal.md` — nunca nombra una
   asignatura concreta, porque el barrido siempre cubre todas), cuerpo
   con un resumen breve en texto de lo más urgente por asignatura y el
   enlace al artefacto publicado. El docente lo revisa y lo envía él
   mismo (o simplemente lo lee) desde Gmail.
7. Si el barrido no encuentra nada urgente en los próximos 14 días para
   ninguna asignatura, genera igualmente el artefacto (para que el
   docente vea que se comprobó y está todo al día) pero dilo en una
   frase destacada en la propia página, y en el asunto del borrador
   añade "— sin urgencias".

**Nota sobre el nombre "VCF" en el evento de Calendar:** el evento de
Calendar de este modo se creó con el literal "VCF · Resumen semanal"
cuando VCF era la única asignatura del repositorio. Este modo ya recorre
todas las asignaturas (paso 2), pero renombrar el evento real de
Calendar excede el alcance de esta skill: por la regla 5 de CLAUDE.md,
las integraciones con Calendar solo se tocan cuando el usuario las pide
explícitamente en ese momento (vía `/asig-calendar-sync`), nunca en
segundo plano ni como efecto colateral de otra tarea. Si el docente
quiere un nombre neutro ("Resumen semanal" a secas) para el evento, dilo
explícitamente y actualízalo entonces. Esto no afecta al asunto del
borrador de Gmail (paso 6): ese es contenido generado de nuevo cada
semana, no un artefacto externo fijo, así que ya usa directamente el
título de departamento sin necesitar esta misma justificación.

## Salidas

**Informe completo:** en el chat, un informe completo de cinco bloques
por cada asignatura cubierta en la ejecución (una sola si el usuario
pidió una asignatura concreta, todas las existentes si no especificó
ninguna — ver "Rol"), presentadas como secciones separadas cuando cubre
más de una. Opcionalmente, un archivo en `00_CENTRO_CONTROL/` con la
misma estructura.

**Resumen semanal:** un archivo HTML en
`00_CENTRO_CONTROL/RESUMENES_SEMANALES/`, su artefacto publicado
correspondiente, y un borrador en Gmail con el enlace.

## Límites

No modifica ni crea ningún documento de las carpetas 01-14 salvo el
propio informe en `00_CENTRO_CONTROL/`. No aprueba ni rechaza nada, solo
informa. El resumen semanal nunca envía el correo (solo deja el
borrador) ni inventa persistencia de casillas que no existe: todo lo
que muestra se recalcula desde cero cada vez, a partir del estado real
del repositorio.

## Validación humana

Ninguna para el contenido: es puramente informativo, el usuario decide
qué hacer con lo que reporta. Sí es el docente quien decide si envía
(o no) el borrador de Gmail que deja el modo semanal — nunca se envía
solo.
