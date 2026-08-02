# Centro de Control Docente — modo "registro" de /asig-estado — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Añadir un tercer modo ("registro") a la skill `/asig-estado` que genera, bajo demanda y para todas las asignaturas, un registro vivo de documentos (tabla "Documentos", doce campos) y un resumen por asignatura ("Panel general") — implementando el alcance A+B del spec aprobado.

**Architecture:** No hay backend ni base de datos: el "registro" es texto Markdown generado por la skill cada vez que se invoca, releyendo el repositorio desde cero (nada persiste entre ejecuciones). Vive como una sección nueva dentro de `.claude/skills/asig-estado/SKILL.md` — instrucciones que otra instancia de Claude sigue al ejecutar el modo — no como código de aplicación. El artefacto real es `DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/centro_control_<YYYY-MM-DD>.md`; un snapshot a Google Drive (conversión automática CSV → Google Sheet) es opcional y solo se genera cuando el docente lo pide en ese momento.

**Tech Stack:** Markdown (contenido de la skill y del artefacto generado), YAML (`ficha.yaml`, ya existente), git (versionado y verificación con `git log`/`grep`). No hay framework de tests tradicional — cada tarea se verifica releyendo el archivo modificado y, en la última tarea, ejecutando el modo a mano contra datos reales del repositorio.

## Global Constraints

- Ruta raíz del proyecto (repo git): `/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE/`. Todas las rutas de archivo de este plan son relativas a esa raíz.
- Alcance de documentos del registro: el mismo universo que ya recorre `/asig-revision` — los 4 documentos base (`01_NORMATIVA_CURRICULO/normativa_registro.md`, `03_MAPA_CURRICULAR/matriz_alineacion.md`, `02_PROGRAMACION/programacion_26_27.md`, `04_TEMPORALIZACION/calendario_26_27.md`), `05_UNIDADES/`, `06_TEMARIO/VIGENTE/`, `07_ACTIVIDADES_TAREAS/VIGENTE/` (sus 11 subcarpetas), `08_EVALUACION/` y `09_RECURSOS_DIGITALES/` (sus 6 subcarpetas). Queda fuera `06_TEMARIO/REFERENCIA_HISTORICA/`, `07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/` y, sin excepción, `10_DIVERSIDAD/INFORMES_ALUMNADO/`, `10_DIVERSIDAD/PLANES_ADAPTACION/` y `11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/`.
- "Vivo" significa recalculado bajo demanda desde cero, nunca un valor manual que sobreviva a la siguiente ejecución.
- "Fecha de próxima revisión" solo se rellena cuando hay una regla real detrás (BORRADOR estancado a 15 días, o unidad `APROBADO` con inicio próximo en `ficha.yaml`); en cualquier otro caso el campo queda vacío — nunca se inventa una fecha.
- Las integraciones de escritura/creación en Google Drive solo se ejecutan cuando el docente las pide explícitamente en ese momento (regla 5 de `CLAUDE.md`) — este plan nunca crea ni sube nada a Drive de forma automática; las lecturas (`search_files`) para resolver "Enlace al archivo" sí son parte del propio diseño aprobado y se ejercitan en la Tarea 4.
- Cada tarea termina con un commit de git.
- No existe herramienta de borrado ni de actualización de una hoja de Drive ya creada en este entorno — cualquier snapshot a Drive es siempre un archivo nuevo con fecha, nunca una hoja que se sobrescribe.

---

### Task 1: Modo "registro" — disparo, alcance y tabla "Documentos"

**Files:**
- Modify: `.claude/skills/asig-estado/SKILL.md:3` (frontmatter `description`)
- Modify: `.claude/skills/asig-estado/SKILL.md:12-15` ("Tiene dos modos" → "Tiene tres modos")
- Modify: `.claude/skills/asig-estado/SKILL.md` (insertar sección nueva entre la línea 169 y la línea 171 actuales, es decir, justo antes de `## Salidas`)

**Interfaces:**
- Consumes: la estructura de carpetas y `ficha.yaml → unidades[].ra` (lista, p. ej. `[RA7, RA8, RA9]`), `ficha.yaml → unidades[].fechas.inicio/fin`, `ficha.yaml → unidades[].archivo`, `ficha.yaml → unidades[].estado` — todos ya existentes y verificados en `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml`.
- Produces: la cabecera de sección exacta `## Modo registro (Centro de Control Docente)` y, dentro de ella, una **tabla de referencia de dos columnas** (`Columna | Cómo se rellena`) con doce filas — una por cada campo que deberá tener la tabla ancha "Documentos" del artefacto final: `Asignatura, Unidad, Tipo, Curso, Estado, Versión, Última revisión, Próxima revisión, RA/Criterios, Enlace, Observaciones, Acción pendiente`. Esta tabla de referencia vive dentro del `SKILL.md` (instrucciones); la tabla ancha real de doce columnas (una fila por documento) solo existe en el artefacto generado `centro_control_<fecha>.md` que produce la Tarea 4 — no hace falta ni tiene sentido que el propio `SKILL.md` contenga esa tabla ancha rellena. Tarea 2 añade la subsección "Panel general" a continuación de esta misma sección.

- [ ] **Step 1: Actualizar la descripción del frontmatter**

En `.claude/skills/asig-estado/SKILL.md`, sustituye la línea 3 completa por:

```yaml
description: Genera una foto de estado de las asignaturas del departamento (rol de Coordinador / Centro de control) — qué falta en cada ficha.yaml, qué carpetas están vacías, próximos hitos del calendario, incoherencias detectadas, y qué unidades próximas necesitan material todavía. Incluye un modo de resumen semanal que publica un artefacto HTML visual por asignatura y deja un borrador en Gmail con el enlace, y un modo de registro que genera una tabla viva de todos los documentos con ciclo BORRADOR/APROBADO (estado, versión, RA/criterios, enlace a Drive, acciones pendientes) más un panel resumen por asignatura. Úsalo cuando el usuario pida el estado, resumen, panel de control, "qué falta", qué preparar la semana que viene, el registro de documentos, el centro de control, o cuando toque el recordatorio semanal de Google Calendar (VCF · Resumen semanal).
```

- [ ] **Step 2: Actualizar "Tiene dos modos" a "Tiene tres modos"**

Sustituye las líneas 12-15 actuales:

```markdown
seguir creciendo), no genera contenido nuevo, solo informa. Tiene dos
modos: el informe completo bajo demanda (tareas 1-7 más abajo) y el
resumen semanal condensado y multi-asignatura (ver "Modo resumen
semanal").
```

por:

```markdown
seguir creciendo), no genera contenido nuevo, solo informa. Tiene tres
modos: el informe completo bajo demanda (tareas 1-7 más abajo), el
resumen semanal condensado y multi-asignatura (ver "Modo resumen
semanal"), y el registro de documentos con su panel general (ver "Modo
registro").
```

- [ ] **Step 3: Insertar la sección "Modo registro" (disparo, alcance, universo y tabla Documentos)**

Justo antes de la línea `## Salidas` (línea 171 en el archivo original, ahora desplazada por los cambios del Step 1-2), inserta esta sección completa:

```markdown
## Modo registro (Centro de Control Docente)

Un tercer modo, pensado para tener una vista tabular de todos los
documentos con ciclo de vida (`BORRADOR`/`APROBADO`) del departamento,
con su estado, versión y qué acción pendiente tiene cada uno. No
sustituye al informe completo ni al resumen semanal: los tres comparten
la misma lectura del repositorio, pero este modo la presenta como dos
tablas en vez de como texto narrativo.

1. **Disparo:** a demanda ("actualiza el centro de control", "genera el
   registro de documentos"). No tiene recordatorio de Calendar propio.
   Si el docente lo pide explícitamente en el mismo momento que ejecuta
   el resumen semanal, puede generarse a continuación de este, pero son
   invocaciones independientes.
2. **Alcance:** siempre recorre todas las asignaturas bajo
   `DEPARTAMENTO_DOCENTE/ASIGNATURAS/*/` — igual que el resumen semanal,
   no sigue la distinción de la nota al principio de "Tareas".
3. **Universo de documentos:** el mismo que ya recorre `/asig-revision`
   — los 4 documentos base, `05_UNIDADES/`, `06_TEMARIO/VIGENTE/`,
   `07_ACTIVIDADES_TAREAS/VIGENTE/` (sus 11 subcarpetas) y
   `08_EVALUACION/` y `09_RECURSOS_DIGITALES/` (sus subcarpetas por
   tipo). Nunca incluye `REFERENCIA_HISTORICA/` (no tiene ciclo de
   estado) ni, sin excepción, `10_DIVERSIDAD/INFORMES_ALUMNADO/`,
   `10_DIVERSIDAD/PLANES_ADAPTACION/` ni
   `11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/`.
4. **Tabla «Documentos»:** una fila por documento del universo anterior,
   con estas doce columnas:

   | Columna | Cómo se rellena |
   |---|---|
   | Asignatura | `ficha.yaml → asignatura.codigo` |
   | Unidad | token `UD<NN>` del nombre de archivo; `—` para los 4 documentos base |
   | Tipo | carpeta contenedora: `Documento base`, `Unidad`, `Temario`, `Tarea`, `Examen` o `Recurso digital` |
   | Curso | `ficha.yaml → asignatura.curso_academico` |
   | Estado | `BORRADOR`/`APROBADO` del nombre de archivo; para los 4 documentos base, el marcador `**Estado:** ...` de su cabecera |
   | Versión | token `V0X` del nombre de archivo |
   | Última revisión | fecha del último commit que tocó ese archivo (`git log -1 --format=%as -- <ruta>`) |
   | Próxima revisión | si `Estado = BORRADOR` y han pasado ≥15 días desde "Última revisión" (mismo umbral que usa `/asig-mantenimiento` para "BORRADOR estancados"): esa fecha límite ya vencida, marcada como tal; si `Estado = APROBADO` y el documento pertenece a una unidad cuyo `ficha.yaml → unidades[].fechas.inicio` cae dentro de los próximos 45 días: esa fecha de inicio; en cualquier otro caso, vacío |
   | RA/Criterios | si el propio documento cita un criterio literal (patrón `RA\d+\.[a-z]` o `RA\d+`, típico en tareas y exámenes — usa `grep -oE 'RA[0-9]+(\.[a-z])?'` sobre el archivo y toma los valores únicos encontrados), esos valores; si no cita ninguno, el contenido completo de `ficha.yaml → unidades[].ra` para la unidad de ese documento (lista, p. ej. `RA7, RA8, RA9`); para los 4 documentos base, vacío |
   | Enlace | ver algoritmo siguiente |
   | Observaciones | marcas ya presentes en el propio documento: `[NUEVO]`, "pendiente de verificación manual", "sin respaldo histórico", o cualquier discrepancia que el documento señale explícitamente — misma extracción que ya hace `/asig-revision` al listar avisos |
   | Acción pendiente | `Revisar y aprobar en /asig-revision` si `Estado = BORRADOR`; `Subir a Drive` si `Estado = APROBADO` y `Enlace = "no subido a Drive"`; en otro caso, vacío |

   **Algoritmo para "Enlace"** (evita una búsqueda de Drive por cada
   documento; agrupa por subcarpeta):
   1. Por asignatura, una única búsqueda:
      `search_files` con
      `title = '<CODIGO>_<CICLO> <curso_academico>' and mimeType = 'application/vnd.google-apps.folder'`
      (p. ej. `title = 'VCF_TSEAS 2026-2027' and mimeType = 'application/vnd.google-apps.folder'`).
      Si no hay resultado, todos los documentos de esa asignatura quedan
      con Enlace = "no subido a Drive" sin más búsquedas.
   2. Por cada subcarpeta local que tenga al menos un documento en la
      tabla (p. ej. `05_UNIDADES`, `06_TEMARIO`,
      `07_ACTIVIDADES_TAREAS/<N_CARPETA>`, `08_EVALUACION`,
      `09_RECURSOS_DIGITALES/<TIPO>`), resuélvela dentro de Drive
      navegando por título un nivel cada vez: `search_files` con
      `title = '<nombre carpeta>' and parentId = '<id de la carpeta padre ya resuelta>'`.
      Si algún nivel no aparece, todos los documentos locales de esa
      subcarpeta quedan con Enlace = "no subido a Drive" sin más
      búsquedas para esa subcarpeta.
   3. Con la subcarpeta de Drive ya resuelta, una única llamada
      `search_files` con `parentId = '<id de la subcarpeta>'` devuelve
      todos sus archivos. Cruza esos títulos contra los nombres de
      archivo locales (sin extensión para los que Drive convirtió a
      Google Doc/Sheet). Si el título aparece, el Enlace es su
      `viewUrl`; si no, "no subido a Drive".
```

- [ ] **Step 4: Verificar que la sección se insertó correctamente**

```bash
cd "/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE"
grep -n "^## Modo registro" .claude/skills/asig-estado/SKILL.md
grep -n "^## Salidas" .claude/skills/asig-estado/SKILL.md
```

Expected: la línea de `## Modo registro (Centro de Control Docente)` aparece
**antes** que la línea de `## Salidas` en la salida (número de línea menor).
Después, lee el archivo completo y confirma visualmente que la tabla de
referencia `Columna | Cómo se rellena` tiene exactamente doce filas de datos
(una por cada campo listado en "Produces" más arriba, ni de más ni de
menos), que la fila separadora tiene el mismo número de columnas que la de
cabecera (`|---|---|`, dos columnas), y que no ha quedado ningún nivel de
encabezado Markdown duplicado o mal anidado (un único `## Modo
registro...`, con `1.`-`4.` como lista numerada dentro, no como `###`).

- [ ] **Step 5: Commit**

```bash
cd "/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE"
git add .claude/skills/asig-estado/SKILL.md
git commit -m "$(cat <<'EOF'
Añade el modo 'registro' a /asig-estado: disparo, alcance y tabla Documentos

Primera parte del modo registro descrito en
docs/superpowers/specs/2026-07-31-centro-control-registro-documentos-design.md:
disparo a demanda, alcance multi-asignatura, universo de documentos
(mismo que /asig-revision) y la tabla "Documentos" de doce columnas con
su regla de origen exacta por columna, incluida la resolución eficiente
del enlace a Drive por subcarpeta.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Subsección "Panel general"

**Files:**
- Modify: `.claude/skills/asig-estado/SKILL.md` (añadir dentro de `## Modo registro...`, como punto `5.` de la lista numerada, a continuación del punto `4.` que añadió la Tarea 1)

**Interfaces:**
- Consumes: la tabla "Documentos" producida por la Tarea 1 (mismas filas, misma asignatura) — el Panel general se calcula agregando esas filas, nunca leyendo el repositorio de forma independiente.
- Produces: la cabecera de subsección `5. **Panel general:**` con una **tabla de referencia de dos columnas** (`Columna | Cómo se calcula`) con seis filas — una por cada campo que deberá tener la tabla ancha "Panel general" del artefacto final: `Asignatura, % Preparación, Unidad actual, Próxima evaluación, Pendientes, Riesgo`. Igual que en la Tarea 1, esta es la tabla de referencia dentro del `SKILL.md`; la tabla ancha real (una fila por asignatura) solo existe en el artefacto generado. La Tarea 3 la referenciará al describir el artefacto local completo (dos tablas anchas en el mismo archivo).

- [ ] **Step 1: Insertar el punto 5 de la lista numerada**

Al final del punto `4.` (la tabla "Documentos" y su algoritmo de Enlace,
añadidos en la Tarea 1), antes de que termine la lista numerada de
`## Modo registro...`, añade:

```markdown
5. **Panel general:** una fila por asignatura, calculada agregando las
   filas de la tabla "Documentos" de esa misma asignatura — nunca una
   lectura independiente del repositorio:

   | Columna | Cómo se calcula |
   |---|---|
   | Asignatura | `ficha.yaml → asignatura.codigo` |
   | % Preparación | (nº de filas con `Estado = APROBADO`) ÷ (nº total de filas) de esa asignatura, redondeado a entero |
   | Unidad actual | la unidad de `ficha.yaml → unidades` cuyo rango `fechas.inicio`-`fechas.fin` contiene la fecha de hoy; `—` si ninguna |
   | Próxima evaluación | la fecha del examen más próximo en `08_EVALUACION/` cuya unidad todavía no ha llegado a su `fechas.fin`; `—` si no hay ninguno pendiente |
   | Pendientes | recuento de filas de "Documentos" de esa asignatura con "Acción pendiente" no vacía |
   | Riesgo | `Alto` si hay al menos una fila con "Próxima revisión" ya vencida (caso BORRADOR estancado) próxima a una unidad que empieza en menos de 14 días; `Medio` si "Pendientes" > 0 pero sin ese caso urgente; `Bajo` si "Pendientes" = 0 |
```

- [ ] **Step 2: Verificar la subsección**

```bash
cd "/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE"
grep -n "Panel general" .claude/skills/asig-estado/SKILL.md
```

Expected: aparece dentro de `## Modo registro (Centro de Control
Docente)`, como punto `5.` de su lista numerada (no como sección `##`
independiente). Confirma visualmente que la tabla de referencia `Columna
| Cómo se calcula` tiene exactamente seis filas de datos (una por cada
campo listado en "Produces" más arriba), y que la fila separadora tiene
el mismo número de columnas que la de cabecera (`|---|---|`, dos
columnas).

- [ ] **Step 3: Commit**

```bash
cd "/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE"
git add .claude/skills/asig-estado/SKILL.md
git commit -m "$(cat <<'EOF'
Añade la subsección 'Panel general' al modo registro de /asig-estado

Segunda parte del modo registro: resumen de seis columnas por
asignatura, calculado agregando la tabla "Documentos" ya descrita
(nunca como fuente independiente), según
docs/superpowers/specs/2026-07-31-centro-control-registro-documentos-design.md.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Mecánica de generación, y actualización de "Salidas" y "Límites"

**Files:**
- Modify: `.claude/skills/asig-estado/SKILL.md` (añadir puntos `6.` y `7.` dentro de `## Modo registro...`)
- Modify: `.claude/skills/asig-estado/SKILL.md` (sección `## Salidas`, la que sigue inmediatamente después de `## Modo registro...` tras las tareas anteriores)
- Modify: `.claude/skills/asig-estado/SKILL.md` (sección `## Límites`)

**Interfaces:**
- Consumes: la tabla "Documentos" (Tarea 1) y el "Panel general" (Tarea 2) — este paso solo describe dónde y cómo se escriben, no cambia su contenido.
- Produces: la ruta exacta del artefacto local
  `DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/centro_control_<YYYY-MM-DD>.md`
  y el nombre exacto de la carpeta de Drive para snapshots,
  `00_CENTRO_CONTROL 2026-2027` — ambos nombres los usa la Tarea 4 al
  verificar.

- [ ] **Step 1: Insertar los puntos 6 y 7 de la lista numerada**

Al final del punto `5.` (Panel general, añadido en la Tarea 2), cierra la
lista numerada de `## Modo registro...` con:

```markdown
6. **Artefacto local (fuente real):** un único archivo Markdown en
   `DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/centro_control_<YYYY-MM-DD>.md`
   (fecha de hoy), con dos secciones en este orden: `## Panel general`
   primero (la tabla de seis columnas del punto 5, una fila por
   asignatura), `## Documentos` después (la tabla de doce columnas del
   punto 4, agrupada por asignatura y, dentro de cada asignatura, por
   Tipo). Es el mismo patrón que ya usa el informe completo con
   `estado_<YYYY-MM-DD>.md`: un archivo nuevo por ejecución, versionado
   en git, sin pretender ser una única hoja que se sobrescribe.
7. **Snapshot opcional a Drive:** solo si el docente lo pide
   explícitamente en el momento de ejecutar este modo. Genera el
   contenido de cada tabla como CSV (cabecera + filas, sin la fila
   separadora Markdown) y súbelo con `create_file`
   (`contentMimeType: "text/csv"`, sin `disableConversionToGoogleType`,
   para que Drive lo convierta automáticamente a Google Sheet). Antes de
   subir, localiza la carpeta de Drive `00_CENTRO_CONTROL 2026-2027` en
   la raíz de Drive (`search_files` con
   `title = '00_CENTRO_CONTROL 2026-2027' and mimeType = 'application/vnd.google-apps.folder' and parentId = 'root'`);
   si no existe, créala primero con `create_file`
   (`contentMimeType: "application/vnd.google-apps.folder"`, sin
   `parentId` para que quede en la raíz de Drive). Sube dos archivos
   separados: `Centro de Control · Panel general · <YYYY-MM-DD>` y
   `Centro de Control · Documentos · <YYYY-MM-DD>`. Cada snapshot es un
   archivo nuevo — no hay forma de sobrescribir uno anterior con las
   herramientas disponibles; el docente puede acumularlos o borrarlos a
   mano desde Drive.
```

- [ ] **Step 2: Actualizar la sección "Salidas"**

Localiza la sección `## Salidas` (la que sigue a `## Modo registro...`
tras el Step 1 de este task) y añade, a continuación del párrafo que
empieza con "**Resumen semanal:**", un tercer párrafo:

```markdown
**Registro:** un archivo Markdown en `00_CENTRO_CONTROL/` con las tablas
"Panel general" y "Documentos", y opcionalmente un snapshot de cada
tabla como hoja de cálculo en Drive (carpeta `00_CENTRO_CONTROL
2026-2027`), solo si el docente lo pide en el momento.
```

- [ ] **Step 3: Actualizar la sección "Límites"**

En la sección `## Límites`, al final del párrafo ya existente (el que
empieza con "No modifica ni crea ningún documento..."), añade esta
frase:

```markdown
El modo registro nunca sube nada a Drive salvo que el docente lo pida
explícitamente en esa misma ejecución (regla 5 de `CLAUDE.md`); sus
lecturas de Drive para resolver el campo "Enlace" no crean ni modifican
nada. Ninguno de los tres modos guarda un valor manual que sobreviva a
la siguiente ejecución — todo se recalcula desde cero cada vez.
```

- [ ] **Step 4: Verificar**

```bash
cd "/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE"
grep -n "^## " .claude/skills/asig-estado/SKILL.md
```

Expected: el orden de secciones `##` es exactamente `Rol`, `Entradas`,
`Tareas`, `Modo resumen semanal (recordado por Calendar)`, `Modo
registro (Centro de Control Docente)`, `Salidas`, `Límites`, `Validación
humana` — sin secciones duplicadas ni fuera de orden.

- [ ] **Step 5: Commit**

```bash
cd "/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE"
git add .claude/skills/asig-estado/SKILL.md
git commit -m "$(cat <<'EOF'
Completa el modo registro de /asig-estado: artefacto local, snapshot a Drive, Salidas y Límites

Cierra la descripción del modo registro con dónde y cómo se escribe el
artefacto (local, fuente real) y el snapshot opcional a Drive (nunca
automático), y actualiza las secciones compartidas Salidas y Límites
del SKILL.md para reflejar el tercer modo, según
docs/superpowers/specs/2026-07-31-centro-control-registro-documentos-design.md.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Verificación — ejecutar el modo registro a mano contra datos reales

**Files:**
- Create: `DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/centro_control_<fecha-de-ejecución-real>.md`
- Modify (solo si la verificación encuentra que una instrucción de las Tareas 1-3 no se puede seguir tal cual está escrita): `.claude/skills/asig-estado/SKILL.md`

**Interfaces:**
- Consumes: el `## Modo registro (Centro de Control Docente)` completo escrito en las Tareas 1-3, y el estado real de `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/` y `DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/`.
- Produces: un artefacto real que demuestra que las instrucciones son
  seguibles tal cual están escritas, o una corrección concreta en el
  `SKILL.md` allí donde no lo eran.

No hay test automatizado que ejecutar: esta tarea consiste en que quien
implementa el plan actúe él mismo como si fuera la skill, siguiendo al
pie de la letra las instrucciones que acaba de escribir, sobre datos
reales. Es la única forma de comprobar que el modo registro descrito en
las Tareas 1-3 realmente se puede seguir sin ambigüedad.

- [ ] **Step 1: Reunir el universo de documentos de VCF_TSEAS para dos subcarpetas completas**

Para mantener la verificación acotada, cubre el universo completo de dos
subcarpetas de una sola asignatura (no las 250+ documentos de todo el
proyecto) más un cruce con la otra asignatura en el Panel general (Step
4). Lista los documentos de `05_UNIDADES/` y `08_EVALUACION/` de VCF:

```bash
cd "/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE"
find "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/05_UNIDADES" -maxdepth 1 -type f -name "*.md" | sort
find "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/08_EVALUACION" -maxdepth 1 -type f -name "*.md" | sort
```

- [ ] **Step 2: Rellenar la tabla "Documentos" a mano para esos archivos**

Para cada archivo listado en el Step 1, sigue literalmente el punto 4
de `## Modo registro...` (Tarea 1): extrae Asignatura, Unidad, Tipo,
Curso, Estado, Versión (del nombre de archivo o de `ficha.yaml`), la
fecha de última revisión (`git log -1 --format=%as -- <ruta>`), aplica
la regla de "Próxima revisión", extrae RA/Criterios (`grep -oE
'RA[0-9]+(\.[a-z])?' <ruta>` y, si no hay coincidencias, usa
`ficha.yaml → unidades[].ra` de la unidad correspondiente), resuelve
"Enlace" con el algoritmo de tres pasos (VCF ya tiene documentos subidos
a Drive de una sesión anterior — comprueba que el algoritmo efectivamente
encuentra esos enlaces reales, no solo que produce "no subido a Drive"
para todo), y deriva Observaciones y Acción pendiente.

Si en algún campo la instrucción escrita en las Tareas 1-3 no permite
llegar a un valor concreto sin inventar nada (por ejemplo, un patrón de
`grep` que no encuentra lo que se esperaba, o un campo de `ficha.yaml`
con un nombre distinto al documentado), corrige el texto del `SKILL.md`
en ese mismo momento para que describa lo que de verdad funciona, y
anota el cambio para el Step 6.

- [ ] **Step 3: Escribir el archivo local con las dos tablas para VCF**

Crea `DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/centro_control_<fecha de
hoy en formato YYYY-MM-DD>.md` con dos secciones — `## Panel general`
primero (de momento, aunque solo tengas el detalle completo de VCF, ver
Step 4 para completar la fila de MET) y `## Documentos` después, con la
tabla de doce columnas rellenada en el Step 2, agrupada por Tipo dentro
de VCF.

- [ ] **Step 4: Completar la fila de Panel general de MET_TSEAS**

Sin repetir el detalle fila por fila (eso ya está probado con VCF en los
Steps 1-3), calcula la fila de Panel general de MET_TSEAS aplicando el
punto 5 de `## Modo registro...` (Tarea 2) a un barrido rápido de sus
documentos:

```bash
cd "/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE"
find "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS" \( -path "*05_UNIDADES/*" -o -path "*06_TEMARIO/VIGENTE/*" -o -path "*07_ACTIVIDADES_TAREAS/VIGENTE/*" -o -path "*08_EVALUACION/*" -o -path "*09_RECURSOS_DIGITALES/*" \) -type f \( -name "*APROBADO*" -o -name "*BORRADOR*" \) | wc -l
find "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS" \( -path "*05_UNIDADES/*" -o -path "*06_TEMARIO/VIGENTE/*" -o -path "*07_ACTIVIDADES_TAREAS/VIGENTE/*" -o -path "*08_EVALUACION/*" -o -path "*09_RECURSOS_DIGITALES/*" \) -type f -name "*APROBADO*" | wc -l
```

Con esos dos recuentos calcula `% Preparación` (aprobados ÷ total), y
completa `Unidad actual` y `Próxima evaluación` leyendo
`DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/00_FICHA/ficha.yaml →
unidades` contra la fecha de hoy. Añade la fila de MET a la tabla
"Panel general" del archivo creado en el Step 3, junto a la de VCF.

- [ ] **Step 5: Revisar el artefacto completo**

Lee `DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/centro_control_<fecha>.md`
entero y confirma: ambas tablas tienen el número de columnas correcto en
cada fila, ninguna celda contiene un valor inventado (todo campo vacío
lo está porque la regla correspondiente así lo determina, no porque
faltara tiempo para rellenarlo), y al menos un documento de VCF muestra
un enlace de Drive real (no "no subido a Drive") si ese documento se
subió en una sesión anterior — si todos los enlaces salen vacíos y
sabes que hay documentos de VCF ya subidos a Drive, el algoritmo de
"Enlace" tiene un fallo que hay que corregir en el `SKILL.md` antes de
seguir.

- [ ] **Step 6: Commit**

```bash
cd "/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE"
git add DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/centro_control_*.md .claude/skills/asig-estado/SKILL.md
git commit -m "$(cat <<'EOF'
Verifica el modo registro de /asig-estado contra datos reales de VCF y MET

Ejecuta a mano el modo registro descrito en SKILL.md sobre
05_UNIDADES/ y 08_EVALUACION/ de VCF_TSEAS (detalle completo, incluida
la resolución de enlaces de Drive reales) y sobre un barrido agregado de
MET_TSEAS (fila de Panel general), produciendo el primer
centro_control_<fecha>.md real. [Si hubo correcciones al SKILL.md,
añadir aquí: "Corrige además <campo/regla concreta> en SKILL.md, que no
se podía seguir tal cual estaba escrito: <qué se cambió>."]

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

## Fuera de alcance de este plan

- Cualquier smoke test que suba de verdad un snapshot a Drive: por la
  regla 5 de `CLAUDE.md` (integraciones de Drive solo bajo petición
  explícita del docente en el momento), la primera vez que el snapshot a
  Drive se ejercite de verdad debe ser porque el docente lo pidió en una
  sesión real, no como parte de la verificación automatizada de este
  plan.
- Añadir un recordatorio de Calendar para este modo (fuera de alcance
  del spec — parte de la rutina C, no diseñada todavía).
- La taxonomía de 8 estados documentales, y las pestañas "Plan docente"
  y "Evaluación" de la propuesta original — ambas fuera de alcance del
  spec aprobado.
