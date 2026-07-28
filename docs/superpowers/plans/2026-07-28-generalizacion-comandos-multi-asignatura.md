# Generalización de comandos a multi-asignatura — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the VCF-specific `/vcf-*` command family (16 skills) and `CLAUDE.md` with a generic `/asig-*` family that resolves which asignatura it operates on from natural language, and scaffold `MET_TSEAS/` so the new commands have a second real subject to run against.

**Architecture:** Each `.claude/skills/vcf-<name>/` folder is copied to `.claude/skills/asig-<name>/` and edited in place: command self-references (`/vcf-X` → `/asig-X`), hardcoded `ASIGNATURAS/VCF_TSEAS/` paths replaced with a pointer to the shared resolution mechanism, and VCF-specific wording genericized. The resolution mechanism itself is defined once, in `CLAUDE.md`, so no skill repeats that logic. `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/` content is never touched except the `/vcf-*` → `/asig-*` command-name references inside its 15 `README.md` files (navigational docs, not curricular content — see Global Constraints).

**Tech Stack:** Markdown skill files (Claude Code skills), YAML (`ficha.yaml`), git. No code, no test runner — "tests" in this plan are grep-based verification commands and one end-to-end smoke test.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-07-28-generalizacion-comandos-multi-asignatura-design.md`.
- **Never modify** any file under `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/` except: the 15 `README.md` files (command-name references only, Task 3), and never touch `ficha.yaml`, any `05_UNIDADES/`, `06_TEMARIO/`, `07_ACTIVIDADES_TAREAS/`, `08_EVALUACION/`, or `09_RECURSOS_DIGITALES/` file.
- New command prefix: `asig-` (e.g. `/asig-estado`). No `/vcf-*` command exists after Task 23.
- New asignatura: código `MET`, carpeta `MET_TSEAS`, nombre completo "Metodología de la Enseñanza de Actividades Físico-Deportivas", ciclo "Técnico Superior en Enseñanza y Animación Sociodeportiva (TSEAS)", centro "Formdepor", comunidad autónoma "Extremadura", curso académico "2026-2027", docente "Mario Pérez Quintero" (all copied verbatim from `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml`, which uses identical values for these fields).
- `MET_TSEAS/00_FICHA/ficha.yaml` starts as an empty skeleton (identifying fields filled in, everything curricular at `null`/`[]`/`borrador`) — running `/asig-normativa`, `/asig-auditoria`, `/asig-programacion` etc. for real on METODOLOGÍA is explicitly out of scope of this plan.
- Every skill migration task must end with the specified grep verification returning the documented expected output before moving on.
- Work from the repo root: `/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE`.

---

### Task 1: Rewrite `CLAUDE.md` — generic rules + shared asignatura-resolution mechanism

**Files:**
- Modify: `CLAUDE.md`

**Interfaces:**
- Produces: a new `## Cómo se resuelve la asignatura` section (exact heading, other tasks link to it verbatim as `CLAUDE.md → "Cómo se resuelve la asignatura"`) and an updated `## Dónde está todo` section listing active asignaturas by código.

- [ ] **Step 1: Read the current file for reference**

Run: `cat "CLAUDE.md"`

This is the file you're rewriting — note the exact current section headers (`## Dónde está todo`, `## Comandos disponibles`, `## Reglas fijas...`) so you preserve the ones that don't need to change in place.

- [ ] **Step 2: Replace the title and first paragraph**

Replace:
```markdown
# Entorno docente — Formdepor / TSEAS / VCF

Este repositorio es el entorno docente vivo del módulo **Valoración de la
Condición Física (VCF)**, ciclo **Técnico Superior en Enseñanza y Animación
Sociodeportiva (TSEAS)**, centro **Formdepor**, comunidad autónoma
**Extremadura**, curso **2026-2027**.
```
With:
```markdown
# Entorno docente — Formdepor

Este repositorio es el entorno docente vivo del departamento de **Formdepor**,
ciclo **Técnico Superior en Enseñanza y Animación Sociodeportiva (TSEAS)**,
comunidad autónoma **Extremadura**, curso **2026-2027**. Cada asignatura vive
en su propia carpeta bajo `DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/`
(hoy: `VCF_TSEAS` y `MET_TSEAS`) y comparte la misma capa de comandos
`/asig-*` descrita más abajo.
```

- [ ] **Step 3: Replace "Dónde está todo"**

Replace the existing `## Dónde está todo` section body with:
```markdown
## Dónde está todo

- `DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/00_FICHA/ficha.yaml` —
  modelo de datos único de cada asignatura. Léelo antes de generar cualquier
  contenido para saber qué normativa, RA, criterios, contenidos y unidades ya
  existen. `asignatura.codigo` y `asignatura.nombre` son los campos que usan
  los comandos `/asig-*` para saber a qué asignatura te refieres (ver más
  abajo, "Cómo se resuelve la asignatura").
- `DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/` — las 15 carpetas
  numeradas del proyecto (normativa, programación, unidades, temario,
  evaluación...), iguales para cada asignatura. Cada una tiene un
  `README.md` explicando su propósito.
- Asignaturas activas hoy:
  - **VCF** — Valoración de la Condición Física (`VCF_TSEAS/`).
  - **MET** — Metodología de la Enseñanza de Actividades Físico-Deportivas
    (`MET_TSEAS/`).
- `3. VALORACIÓN 25_26/` y `3. METODOLOGÍA 25_26/` — material histórico
  original de cada asignatura. **Nunca se mueve ni se borra directamente**;
  solo `/asig-auditoria` puede copiar de aquí a `DEPARTAMENTO_DOCENTE/`, y
  solo tras confirmación explícita del usuario. Esas copias hacen crecer el
  repositorio de git con el tiempo, porque los binarios no son diffables,
  así que conviene hacer las migraciones grandes de forma deliberada y no
  todas de golpe.
```

- [ ] **Step 4: Add the new "Cómo se resuelve la asignatura" section**

Insert this new section immediately after "Dónde está todo" and before "Comandos disponibles":

```markdown
## Cómo se resuelve la asignatura

Todo comando `/asig-*` que necesite saber sobre qué asignatura trabajar
sigue esta regla, sin excepciones:

1. Recorre `DEPARTAMENTO_DOCENTE/ASIGNATURAS/*/00_FICHA/ficha.yaml` y
   compara lo que ha dicho el usuario contra `asignatura.codigo`
   (coincidencia exacta o de prefijo, insensible a mayúsculas — "met",
   "MET" → `MET`) y `asignatura.nombre` (coincidencia de subcadena,
   insensible a mayúsculas/acentos — "metodología" → `MET`).
2. Si resuelve a **exactamente una** asignatura, sigue con esa — sin pedir
   confirmación adicional.
3. Si resuelve a **cero o a más de una**, pregunta explícitamente al
   usuario cuál de las asignaturas existentes quiere decir, antes de
   generar, modificar o aprobar nada. Nunca asume "la primera" ni "la más
   reciente".
4. Excepción: los comandos de solo lectura/informe (`/asig-estado`,
   `/asig-mantenimiento`, y la verificación normativa de `/asig-vigilancia`)
   invocados sin mencionar ninguna asignatura recorren **todas** las que
   existan, en vez de preguntar.
```

- [ ] **Step 5: Replace "Comandos disponibles"**

Replace the existing `## Comandos disponibles` section body with:
```markdown
## Comandos disponibles

`/asig-estado`, `/asig-normativa`, `/asig-auditoria`, `/asig-programacion`,
`/asig-unidad`, `/asig-tema`, `/asig-tarea`, `/asig-examen`,
`/asig-revision`, `/asig-drive`, `/asig-calendar-sync`, `/asig-vigilancia`,
`/asig-diversidad`, `/asig-recursos`, `/asig-analitica`,
`/asig-mantenimiento`. Cada uno vive en `.claude/skills/<nombre>/SKILL.md`
y documenta su propio rol, entradas, tareas, salidas y límites, y todos
resuelven la asignatura sobre la que operan según la sección anterior.
`/asig-revision` es el punto de entrada para revisar y aprobar en bloque lo
que generan los demás; `/asig-drive` y `/asig-calendar-sync` suben a
Drive/Calendar lo ya aprobado; `/asig-vigilancia` comprueba si ha cambiado
la normativa (a mano o vía la ejecución trimestral programada);
`/asig-recursos` genera presentaciones (Gamma) y paquetes para NotebookLM,
extensible a más plataformas; `/asig-diversidad` y `/asig-analitica` son
las dos excepciones deliberadas a la regla 3 de abajo — trabajan con datos
reales de alumnado (necesidades especiales y calificaciones
respectivamente), que nunca salen de este disco. `/asig-analitica` está
definido pero no es ejecutable todavía para ninguna asignatura: no hay
calificaciones reales cargadas. `/asig-mantenimiento` es el barrido
quincenal de salud de cada asignatura: detecta desactualizaciones, dispara
otras skills para regenerar contenido en `BORRADOR`, propone (sin aplicar)
mejoras a otras skills, y deja un borrador de email si hay hallazgos — se
ejecuta en local (nunca en la nube, porque necesita escribir en el
repositorio), recordado cada 15 días por un evento de Google Calendar.
`/asig-estado` añade un modo de resumen semanal con el mismo patrón:
recordado por un evento semanal de Google Calendar (el docente sigue
disparándolo él mismo desde ahí, no hay ejecución en la nube por su
cuenta), recorre todas las asignaturas de `ASIGNATURAS/` y publica un
artefacto HTML con lo pendiente de cada una esa semana — casillas
calculadas solo a partir de si el archivo correspondiente ya existe, nunca
marcadas a mano — y deja un borrador en Gmail con el enlace, sin enviarlo
nunca.
```

- [ ] **Step 6: Genericize "Reglas fijas"**

The 8 rules stay numbered and in the same order. Apply these exact
replacements (leave everything else in each rule untouched):

- Rule 3: replace `secciones de atención a la diversidad genéricas de cada unidad. **Dos excepciones únicas y deliberadas:** /vcf-diversidad maneja datos reales (no inventados) de alumnado con necesidades especiales, aportados legítimamente por el docente en 10_DIVERSIDAD/INFORMES_ALUMNADO/; /vcf-analitica maneja calificaciones reales en 11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/` with the same text but `/vcf-diversidad` → `/asig-diversidad` and `/vcf-analitica` → `/asig-analitica`. Also replace `de /vcf-drive, de /vcf-calendar-sync, de /vcf-revision y del detalle de /vcf-estado` with `de /asig-drive, de /asig-calendar-sync, de /asig-revision y del detalle de /asig-estado`. Also replace `Los informes agregados que produce /vcf-analitica` with `Los informes agregados que produce /asig-analitica`.
- Rule 5: replace `/vcf-drive`, `/vcf-calendar-sync` with `/asig-drive`, `/asig-calendar-sync`; replace `Única excepción explícita: /vcf-vigilancia sí corre` with `Única excepción explícita: /asig-vigilancia sí corre`; replace `ver .claude/skills/vcf-vigilancia/` with `ver .claude/skills/asig-vigilancia/`.
- Rule 6: no changes.
- Rule 8: replace `/vcf-mantenimiento puede disparar otras skills de generación de contenido (/vcf-unidad, /vcf-tema, /vcf-tarea, /vcf-examen, /vcf-programacion)` with `/asig-mantenimiento puede disparar otras skills de generación de contenido (/asig-unidad, /asig-tema, /asig-tarea, /asig-examen, /asig-programacion)`; replace `nunca dispara /vcf-auditoria ni /vcf-normativa` with `nunca dispara /asig-auditoria ni /asig-normativa`.
- Leave rules 1, 2, 4, 7 exactly as they are (they don't mention VCF or any command name).

- [ ] **Step 7: Verify no `vcf-` references remain**

Run: `grep -n "vcf-\|VCF_TSEAS" "CLAUDE.md"`

Expected: no output (empty). If anything prints, fix it before continuing.

- [ ] **Step 8: Commit**

```bash
git add "CLAUDE.md"
git commit -m "$(cat <<'EOF'
Generaliza CLAUDE.md a multi-asignatura (/asig-*)

Sustituye la capa /vcf-* por /asig-*, define el mecanismo único de
resolución de asignatura (código/nombre en ficha.yaml, pregunta si es
ambiguo), y lista VCF y MET como asignaturas activas. Primer paso de
docs/superpowers/specs/2026-07-28-generalizacion-comandos-multi-asignatura-design.md.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Scaffold `MET_TSEAS/`

**Files:**
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/00_FICHA/ficha.yaml`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/{00_FICHA,01_NORMATIVA_CURRICULO,02_PROGRAMACION,03_MAPA_CURRICULAR,04_TEMPORALIZACION,05_UNIDADES,06_TEMARIO,07_ACTIVIDADES_TAREAS,08_EVALUACION,09_RECURSOS_DIGITALES,10_DIVERSIDAD,11_SEGUIMIENTO_RESULTADOS,12_RECUPERACION,13_MEMORIA_FINAL,14_HISTORICO_CAMBIOS}/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/06_TEMARIO/{VIGENTE,REFERENCIA_HISTORICA}/.gitkeep`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/07_ACTIVIDADES_TAREAS/{VIGENTE,REFERENCIA_HISTORICA}/.gitkeep`

**Interfaces:**
- Consumes: nothing (this task has no dependency on Task 1's content, only on the naming decided in Global Constraints).
- Produces: `MET_TSEAS/00_FICHA/ficha.yaml` with `asignatura.codigo: MET`, which Task 22's smoke test and every skill's asignatura-resolution mechanism (Task 1, Step 4) will match against.

- [ ] **Step 1: Create the folder tree**

```bash
cd "/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/00_FICHA"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/01_NORMATIVA_CURRICULO"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/02_PROGRAMACION"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/03_MAPA_CURRICULAR"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/04_TEMPORALIZACION"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/05_UNIDADES"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/06_TEMARIO/VIGENTE"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/06_TEMARIO/REFERENCIA_HISTORICA"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/07_ACTIVIDADES_TAREAS/VIGENTE"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/08_EVALUACION"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/09_RECURSOS_DIGITALES"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/10_DIVERSIDAD/INFORMES_ALUMNADO"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/10_DIVERSIDAD/PLANES_ADAPTACION"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/11_SEGUIMIENTO_RESULTADOS/INFORMES"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/12_RECUPERACION"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/13_MEMORIA_FINAL"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/14_HISTORICO_CAMBIOS"
touch "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/06_TEMARIO/VIGENTE/.gitkeep"
touch "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/06_TEMARIO/REFERENCIA_HISTORICA/.gitkeep"
touch "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/07_ACTIVIDADES_TAREAS/VIGENTE/.gitkeep"
touch "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/.gitkeep"
```

Before creating each `.gitignore`-worthy personal-data folder, check how VCF_TSEAS excludes them:

Run: `grep -n "10_DIVERSIDAD\|CALIFICACIONES" "/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE/.gitignore"`

Expected: lines matching `**/10_DIVERSIDAD/INFORMES_ALUMNADO/`, `**/10_DIVERSIDAD/PLANES_ADAPTACION/`, `**/11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/` (or an equivalent glob covering all asignaturas, not just `VCF_TSEAS/...`). If the existing `.gitignore` hardcodes `VCF_TSEAS/10_DIVERSIDAD/...` instead of a `**/10_DIVERSIDAD/...` glob, edit `.gitignore` now to generalize those 3 lines the same way (glob prefix `**/` instead of `VCF_TSEAS/`) so `MET_TSEAS`'s personal-data folders are excluded too. This is a required correction, not optional — personal data folders must never be trackable for any asignatura.

- [ ] **Step 2: Write each README.md**

Use the content of VCF_TSEAS's equivalent file as the base (`cat "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/<carpeta>/README.md"`), with two changes applied to every one: replace every `/vcf-` with `/asig-`, and replace any mention of "VCF" as the specific subject (e.g. "normativa autonómica de Extremadura para el módulo VCF") with generic wording ("normativa autonómica de Extremadura para esta asignatura"). `06_TEMARIO/README.md` and `07_ACTIVIDADES_TAREAS/README.md` are empty in VCF_TSEAS too — leave them empty (zero-byte) in MET_TSEAS as well, just create the files with `touch`.

- [ ] **Step 3: Write `00_FICHA/ficha.yaml`**

```yaml
asignatura:
  nombre: Metodología de la Enseñanza de Actividades Físico-Deportivas
  codigo: MET
  ciclo: Técnico Superior en Enseñanza y Animación Sociodeportiva (TSEAS)
  centro: Formdepor
  comunidad_autonoma: Extremadura
  curso_academico: "2026-2027"
  docente: Mario Pérez Quintero
  horas_totales:
    valor: null
    confirmado_extremadura: false
    fuente: null
  horas_semanales:
    valor: null
    confirmado_extremadura: false
    fuente: null
  horario_semanal: {}
normativa:
  rd_estatal: null
  decreto_curriculo_autonomico: null
resultados_aprendizaje: []
criterios_evaluacion: []
contenidos: []
unidades: []
ponderaciones: {}
calendario_ref: 04_TEMPORALIZACION/calendario_26_27.md
metodologia: []
instrumentos_evaluacion: []
estado: borrador
ultima_revision: null
proxima_revision: null
documentos_vinculados: []
```

- [ ] **Step 4: Verify the YAML parses**

Run: `python3 -c "import yaml; yaml.safe_load(open('DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/00_FICHA/ficha.yaml'))" && echo "YAML OK"`

Expected: `YAML OK`. If `python3` doesn't have `yaml` installed, use `ruby -ryaml -e "YAML.load_file('DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/00_FICHA/ficha.yaml'); puts 'YAML OK'"` instead.

- [ ] **Step 5: Verify the folder tree matches VCF_TSEAS's**

Run:
```bash
diff <(cd "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS" && find . -type d | sort) \
     <(cd "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS" && find . -type d | sort)
```
Expected: no output, except VCF_TSEAS may show extra subfolders under `09_RECURSOS_DIGITALES/` (content-generated, not structural) and `07_ACTIVIDADES_TAREAS/VIGENTE/<category>/` subfolders — those are fine to differ; the 15 top-level numbered folders plus `06_TEMARIO/{VIGENTE,REFERENCIA_HISTORICA}` and `07_ACTIVIDADES_TAREAS/{VIGENTE,REFERENCIA_HISTORICA}` and `10_DIVERSIDAD/{INFORMES_ALUMNADO,PLANES_ADAPTACION}` and `11_SEGUIMIENTO_RESULTADOS/{CALIFICACIONES,INFORMES}` must match exactly.

- [ ] **Step 6: Commit**

```bash
git add "DEPARTAMENTO_DOCENTE/ASIGNATURAS/MET_TSEAS/" ".gitignore"
git commit -m "$(cat <<'EOF'
Crea el esqueleto de MET_TSEAS (Metodología, código MET)

Mismas 15 carpetas que VCF_TSEAS y un ficha.yaml inicial con solo los
campos identificativos rellenos (nombre, código, ciclo, centro, curso) —
todo lo curricular queda en null/[]/borrador hasta que se ejecuten
/asig-normativa, /asig-auditoria y /asig-programacion para METODOLOGÍA
(fuera de alcance de este plan).

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Update VCF_TSEAS's 15 `README.md` files — command references only

**Files:**
- Modify: all 15 `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/*/README.md` (not `06_TEMARIO/README.md` or `07_ACTIVIDADES_TAREAS/README.md`, which are empty)

**Interfaces:**
- Consumes: nothing.
- Produces: nothing other tasks depend on — this is a leaf task, but it must happen so VCF_TSEAS never references a dead `/vcf-*` command name after Task 23.

- [ ] **Step 1: List current command mentions**

Run: `grep -rn "vcf-" "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/"*/README.md`

Note every file listed — you'll edit each one.

- [ ] **Step 2: Replace `/vcf-` with `/asig-` in every match**

For each file from Step 1, replace every occurrence of `vcf-` with `asig-` (this only ever appears as part of a command name like `` `/vcf-normativa` `` in these files — confirmed by Step 1's output). Do not change anything else in these files: the wording ("Alimentado por...", "Fuente única de verdad...") stays as-is, including any remaining literal mentions of "VCF" as the subject name (e.g. "normativa autonómica de Extremadura para el módulo VCF" in `01_NORMATIVA_CURRICULO/README.md` stays — that sentence is describing VCF_TSEAS specifically and is accurate, unlike the command name which is being renamed department-wide).

- [ ] **Step 3: Verify**

Run: `grep -rln "vcf-" "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/"*/README.md`

Expected: no output (empty — every file from Step 1 has been fixed).

- [ ] **Step 4: Commit**

```bash
git add "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/"*/README.md
git commit -m "$(cat <<'EOF'
Actualiza referencias /vcf-* a /asig-* en los README de VCF_TSEAS

Solo el nombre de comando citado en cada README (navegación, no
contenido curricular) — nada del contenido aprobado de VCF cambia.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Migrate `vcf-normativa` → `asig-normativa`

**Files:**
- Create: `.claude/skills/asig-normativa/SKILL.md`
- Delete (Task 23 only, not now): `.claude/skills/vcf-normativa/`

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1).

- [ ] **Step 1: Copy the file**

```bash
mkdir -p ".claude/skills/asig-normativa"
cp ".claude/skills/vcf-normativa/SKILL.md" ".claude/skills/asig-normativa/SKILL.md"
```

- [ ] **Step 2: Edit frontmatter and title**

In `.claude/skills/asig-normativa/SKILL.md`:
- `name: vcf-normativa` → `name: asig-normativa`
- `description:` currently: "Localiza y registra la normativa oficial (RD estatal del título TSEAS y normativa autonómica de Extremadura) del módulo Valoración de la Condición Física, extrae resultados de aprendizaje/criterios/contenidos/horas, y genera la matriz de alineación curricular. Úsalo cuando el usuario pida buscar, actualizar o verificar la normativa/currículo de VCF." — replace with: "Localiza y registra la normativa oficial (RD estatal del título y normativa autonómica de Extremadura) del módulo de la asignatura indicada, extrae resultados de aprendizaje/criterios/contenidos/horas, y genera la matriz de alineación curricular. Úsalo cuando el usuario pida buscar, actualizar o verificar la normativa/currículo de una asignatura (resuelta según CLAUDE.md → \"Cómo se resuelve la asignatura\")."
- `# /vcf-normativa — Normativa y currículo (VCF/TSEAS)` → `# /asig-normativa — Normativa y currículo`

- [ ] **Step 3: Genericize the body**

- Line with "aprendizaje, criterios, contenidos y horas del módulo VCF dentro del" → "aprendizaje, criterios, contenidos y horas del módulo de la asignatura resuelta (ver CLAUDE.md → \"Cómo se resuelve la asignatura\") dentro del"
- Line "- Módulo: Valoración de la Condición Física (VCF)" → replace with "- Módulo: el de la asignatura resuelta (nombre y código en su `ficha.yaml → asignatura`)."
- Line "y localiza las horas/contenidos específicos de VCF si los hay." → "y localiza las horas/contenidos específicos de la asignatura si los hay."
- Any `ASIGNATURAS/VCF_TSEAS/` path mentioned → `ASIGNATURAS/<CODIGO>_<CICLO>/` (the asignatura resolved per CLAUDE.md).

- [ ] **Step 4: Verify**

Run: `grep -n "vcf-\|VCF_TSEAS\|\bVCF\b" ".claude/skills/asig-normativa/SKILL.md"`

Expected: no output.

- [ ] **Step 5: Commit**

```bash
git add ".claude/skills/asig-normativa/"
git commit -m "Migra /vcf-normativa a /asig-normativa (genérico multi-asignatura)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 5: Migrate `vcf-auditoria` → `asig-auditoria`

**Files:**
- Create: `.claude/skills/asig-auditoria/SKILL.md`

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1).

- [ ] **Step 1: Copy the file**

```bash
mkdir -p ".claude/skills/asig-auditoria"
cp ".claude/skills/vcf-auditoria/SKILL.md" ".claude/skills/asig-auditoria/SKILL.md"
```

- [ ] **Step 2: Edit frontmatter and title**

- `name: vcf-auditoria` → `name: asig-auditoria`
- `description:` currently references `"3. VALORACIÓN 25_26/"` and `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMORIO`/`07_ACTIVIDADES_TAREAS` and "material antiguo de VCF" — replace with: "Audita el material histórico existente de la asignatura indicada (p. ej. \"3. VALORACIÓN 25_26/\" para VCF, \"3. METODOLOGÍA 25_26/\" para MET — una carpeta por asignatura en la raíz del proyecto), lo clasifica como vigente/reutilizable/obsoleto, y propone y ejecuta (tras confirmación) su copia a `DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/06_TEMARIO` y `07_ACTIVIDADES_TAREAS`. Úsalo cuando el usuario pida auditar, ordenar, clasificar o migrar el material antiguo de una asignatura."
- `# /vcf-auditoria — Auditoría de contenidos (VCF/TSEAS)` → `# /asig-auditoria — Auditoría de contenidos`

- [ ] **Step 3: Genericize hardcoded paths**

Replace every one of these 5 lines' `VCF_TSEAS` with the generic path pattern:
```
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/VIGENTE/
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/REFERENCIA_HISTORICA/
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS/VIGENTE/
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/02_PROGRAMACION/REFERENCIA_HISTORICA/
```
become (same 5 lines, `VCF_TSEAS` → `<CODIGO>_<CICLO>` where `<CODIGO>_<CICLO>` is the resolved asignatura's folder):
```
DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/06_TEMARIO/VIGENTE/
DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/06_TEMARIO/REFERENCIA_HISTORICA/
DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/07_ACTIVIDADES_TAREAS/VIGENTE/
DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/
DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/02_PROGRAMACION/REFERENCIA_HISTORICA/
```
Add one clarifying sentence right before this list if not already clear from context: "`<CODIGO>_<CICLO>` es la carpeta de la asignatura resuelta según CLAUDE.md → \"Cómo se resuelve la asignatura\"."

- [ ] **Step 4: Verify**

Run: `grep -n "vcf-\|VCF_TSEAS\|\bVCF\b" ".claude/skills/asig-auditoria/SKILL.md"`

Expected: no output.

- [ ] **Step 5: Commit**

```bash
git add ".claude/skills/asig-auditoria/"
git commit -m "Migra /vcf-auditoria a /asig-auditoria (genérico multi-asignatura)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 6: Migrate `vcf-programacion` → `asig-programacion`

**Files:**
- Create: `.claude/skills/asig-programacion/SKILL.md`

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1).

- [ ] **Step 1: Copy the file**

```bash
mkdir -p ".claude/skills/asig-programacion"
cp ".claude/skills/vcf-programacion/SKILL.md" ".claude/skills/asig-programacion/SKILL.md"
```

- [ ] **Step 2: Edit frontmatter, title, body**

- `name: vcf-programacion` → `name: asig-programacion`
- `description:` "Cierra la programación didáctica 26/27 de VCF a partir del borrador existente y de ficha.yaml..." → "Cierra la programación didáctica 26/27 de la asignatura resuelta a partir de su borrador existente y de su ficha.yaml..." (keep the rest of the sentence about calendario/festivos unchanged).
- `# /vcf-programacion — Planificación y temporalización (VCF/TSEAS)` → `# /asig-programacion — Planificación y temporalización`
- Read the rest of the file (`cat ".claude/skills/asig-programacion/SKILL.md"`) and replace any remaining hardcoded `VCF_TSEAS` path or standalone "VCF" subject mention using the same pattern as Task 4/5 (`VCF_TSEAS` → `<CODIGO>_<CICLO>`, "de VCF" → "de la asignatura").

- [ ] **Step 3: Verify**

Run: `grep -n "vcf-\|VCF_TSEAS\|\bVCF\b" ".claude/skills/asig-programacion/SKILL.md"`

Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/asig-programacion/"
git commit -m "Migra /vcf-programacion a /asig-programacion (genérico multi-asignatura)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 7: Migrate `vcf-unidad` → `asig-unidad`

**Files:**
- Create: `.claude/skills/asig-unidad/SKILL.md`

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1).

- [ ] **Step 1: Copy the file**

```bash
mkdir -p ".claude/skills/asig-unidad"
cp ".claude/skills/vcf-unidad/SKILL.md" ".claude/skills/asig-unidad/SKILL.md"
```

- [ ] **Step 2: Edit frontmatter, title, body**

- `name: vcf-unidad` → `name: asig-unidad`
- `description:` "Genera o actualiza una unidad didáctica completa de VCF ... Úsalo cuando el usuario pida crear, redactar o revisar una unidad didáctica de VCF." → same sentence with "de VCF" → "de la asignatura resuelta" in both places.
- `# /vcf-unidad — Diseño de unidades didácticas (VCF/TSEAS)` → `# /asig-unidad — Diseño de unidades didácticas`
- "Genera unidades didácticas completas de VCF, vinculadas a los resultados" → "Genera unidades didácticas completas de la asignatura resuelta, vinculadas a los resultados"
- `cat ".claude/skills/asig-unidad/SKILL.md"` and fix any remaining `VCF_TSEAS` path the same way as prior tasks.

- [ ] **Step 3: Verify**

Run: `grep -n "vcf-\|VCF_TSEAS\|\bVCF\b" ".claude/skills/asig-unidad/SKILL.md"`

Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/asig-unidad/"
git commit -m "Migra /vcf-unidad a /asig-unidad (genérico multi-asignatura)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 8: Migrate `vcf-tema` → `asig-tema`

**Files:**
- Create: `.claude/skills/asig-tema/SKILL.md`

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1).

- [ ] **Step 1: Copy the file**

```bash
mkdir -p ".claude/skills/asig-tema"
cp ".claude/skills/vcf-tema/SKILL.md" ".claude/skills/asig-tema/SKILL.md"
```

- [ ] **Step 2: Edit frontmatter, title, body**

- `name: vcf-tema` → `name: asig-tema`
- `description:` "Genera el temario vigente de un tema de VCF ... Úsalo cuando el usuario pida generar, actualizar o auditar un tema/temario de VCF." → "de VCF" → "de la asignatura resuelta" in both places.
- `# /vcf-tema — Contenidos y temario (VCF/TSEAS)` → `# /asig-tema — Contenidos y temario`
- `cat ".claude/skills/asig-tema/SKILL.md"` and fix any remaining `VCF_TSEAS` path the same way as prior tasks.

- [ ] **Step 3: Verify**

Run: `grep -n "vcf-\|VCF_TSEAS\|\bVCF\b" ".claude/skills/asig-tema/SKILL.md"`

Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/asig-tema/"
git commit -m "Migra /vcf-tema a /asig-tema (genérico multi-asignatura)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 9: Migrate `vcf-tarea` → `asig-tarea`

**Files:**
- Create: `.claude/skills/asig-tarea/SKILL.md`

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1).

- [ ] **Step 1: Copy the file**

```bash
mkdir -p ".claude/skills/asig-tarea"
cp ".claude/skills/vcf-tarea/SKILL.md" ".claude/skills/asig-tarea/SKILL.md"
```

- [ ] **Step 2: Edit frontmatter, title, body**

- `name: vcf-tarea` → `name: asig-tarea`
- `description:` "Genera actividades y tareas nuevas para VCF ... Úsalo cuando el usuario pida crear, diseñar o generar una actividad o tarea nueva de VCF." → "para VCF" → "para la asignatura resuelta"; "de VCF" → "de la asignatura resuelta".
- `# /vcf-tarea — Actividades y tareas (VCF/TSEAS)` → `# /asig-tarea — Actividades y tareas`
- `cat ".claude/skills/asig-tarea/SKILL.md"` and fix any remaining `VCF_TSEAS` path the same way as prior tasks.

- [ ] **Step 3: Verify**

Run: `grep -n "vcf-\|VCF_TSEAS\|\bVCF\b" ".claude/skills/asig-tarea/SKILL.md"`

Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/asig-tarea/"
git commit -m "Migra /vcf-tarea a /asig-tarea (genérico multi-asignatura)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 10: Migrate `vcf-examen` → `asig-examen`

**Files:**
- Create: `.claude/skills/asig-examen/SKILL.md`

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1).

- [ ] **Step 1: Copy the file**

```bash
mkdir -p ".claude/skills/asig-examen"
cp ".claude/skills/vcf-examen/SKILL.md" ".claude/skills/asig-examen/SKILL.md"
```

- [ ] **Step 2: Edit frontmatter, title, body**

- `name: vcf-examen` → `name: asig-examen`
- `description:` "Genera instrumentos de evaluación de VCF ... Úsalo cuando el usuario pida un examen, rúbrica, banco de preguntas o solucionario de VCF." → "de VCF" → "de la asignatura resuelta" in both places.
- `# /vcf-examen — Evaluación (VCF/TSEAS)` → `# /asig-examen — Evaluación`
- `cat ".claude/skills/asig-examen/SKILL.md"` and fix any remaining `VCF_TSEAS` path the same way as prior tasks.

- [ ] **Step 3: Verify**

Run: `grep -n "vcf-\|VCF_TSEAS\|\bVCF\b" ".claude/skills/asig-examen/SKILL.md"`

Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/asig-examen/"
git commit -m "Migra /vcf-examen a /asig-examen (genérico multi-asignatura)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 11: Migrate `vcf-drive` → `asig-drive`

**Files:**
- Create: `.claude/skills/asig-drive/SKILL.md`

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1).

- [ ] **Step 1: Copy the file**

```bash
mkdir -p ".claude/skills/asig-drive"
cp ".claude/skills/vcf-drive/SKILL.md" ".claude/skills/asig-drive/SKILL.md"
```

- [ ] **Step 2: Edit frontmatter, title, body**

- `name: vcf-drive` → `name: asig-drive`
- `description:` "Sube a Google Drive los documentos de VCF que ya están APROBADO, replicando la estructura de carpetas del proyecto dentro de una carpeta \"VCF_TSEAS 2026-2027\". Úsalo cuando el usuario pida subir, sincronizar o compartir por Drive los documentos aprobados de VCF." → replace with "Sube a Google Drive los documentos de la asignatura resuelta que ya están APROBADO, replicando la estructura de carpetas del proyecto dentro de una carpeta \"<CODIGO>_<CICLO> <curso académico>\". Úsalo cuando el usuario pida subir, sincronizar o compartir por Drive los documentos aprobados de una asignatura."
- `# /vcf-drive — Integración con Google Drive (VCF/TSEAS)` → `# /asig-drive — Integración con Google Drive`
- "ejecución, los documentos de VCF que ya tienen `APROBADO` en el nombre de" → "ejecución, los documentos de la asignatura resuelta que ya tienen `APROBADO` en el nombre de"
- "`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/` (unidades, temario," → "`DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/` (unidades, temario,"
- "superior llamada **`VCF_TSEAS 2026-2027`**." → "superior llamada **`<CODIGO>_<CICLO> <curso académico>`** (p. ej. `VCF_TSEAS 2026-2027` o `MET_TSEAS 2026-2027`)."
- "Carpeta `VCF_TSEAS 2026-2027` en Google Drive con la estructura y los" → "Carpeta `<CODIGO>_<CICLO> <curso académico>` en Google Drive con la estructura y los"

- [ ] **Step 3: Verify**

Run: `grep -n "vcf-\|VCF_TSEAS\|\bVCF\b" ".claude/skills/asig-drive/SKILL.md"`

Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/asig-drive/"
git commit -m "Migra /vcf-drive a /asig-drive (genérico multi-asignatura)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 12: Migrate `vcf-calendar-sync` → `asig-calendar-sync`

**Files:**
- Create: `.claude/skills/asig-calendar-sync/SKILL.md`

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1).

- [ ] **Step 1: Copy the file**

```bash
mkdir -p ".claude/skills/asig-calendar-sync"
cp ".claude/skills/vcf-calendar-sync/SKILL.md" ".claude/skills/asig-calendar-sync/SKILL.md"
```

- [ ] **Step 2: Edit frontmatter, title, body**

- `name: vcf-calendar-sync` → `name: asig-calendar-sync`
- `description:` "...calendario_26_27.md y de ficha.yaml → unidades ... Úsalo cuando el usuario pida sincronizar, subir o crear en Calendar el calendario del curso de VCF." → "el calendario del curso de VCF" → "el calendario del curso de una asignatura"
- `# /vcf-calendar-sync — Integración con Google Calendar (VCF/TSEAS)` → `# /asig-calendar-sync — Integración con Google Calendar`
- "del calendario de temporalización real de VCF, bajo petición explícita" → "del calendario de temporalización real de la asignatura resuelta, bajo petición explícita"
- "`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/04_TEMPORALIZACION/calendario_26_27.md`" → "`DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/04_TEMPORALIZACION/calendario_26_27.md`"

- [ ] **Step 3: Verify**

Run: `grep -n "vcf-\|VCF_TSEAS\|\bVCF\b" ".claude/skills/asig-calendar-sync/SKILL.md"`

Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/asig-calendar-sync/"
git commit -m "Migra /vcf-calendar-sync a /asig-calendar-sync (genérico multi-asignatura)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 13: Migrate `vcf-vigilancia` → `asig-vigilancia`

**Files:**
- Create: `.claude/skills/asig-vigilancia/SKILL.md`

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1).

- [ ] **Step 1: Copy the file**

```bash
mkdir -p ".claude/skills/asig-vigilancia"
cp ".claude/skills/vcf-vigilancia/SKILL.md" ".claude/skills/asig-vigilancia/SKILL.md"
```

- [ ] **Step 2: Edit frontmatter, title, body**

- `name: vcf-vigilancia` → `name: asig-vigilancia`
- `description:` "Comprueba si ha cambiado alguna de las normas ya verificadas de VCF (RD 653/2017, Decreto 106/2018, Instrucción 13/2024) ... Úsalo cuando el usuario pida comprobar, vigilar o revisar si ha cambiado la normativa de VCF, y en la ejecución trimestral programada." → replace with "Comprueba, para cada asignatura que tenga normativa ya verificada, si esa normativa ha cambiado, o si se ha publicado calendario escolar de Extremadura para el curso siguiente, y avisa solo si encuentra algo nuevo. Úsalo cuando el usuario pida comprobar, vigilar o revisar si ha cambiado la normativa de una asignatura (o de todas, si no especifica ninguna), y en la ejecución trimestral programada."
- `# /vcf-vigilancia — Vigilancia normativa (VCF/TSEAS)` → `# /asig-vigilancia — Vigilancia normativa`
- Read the rest of the file (`cat ".claude/skills/asig-vigilancia/SKILL.md"`). Its "Tareas" section currently describes checking 3 specific norms (RD 653/2017, Decreto 106/2018, Instrucción 13/2024) hardcoded for VCF — reword step 1 of "Tareas" to say it repeats this check **for every asignatura's own `normativa_registro.md`** (per the "sin nivel compartido" decision — VCF and MET each have their own copy, checked independently, even though today they cite the same norms), instead of naming VCF's 3 specific norms as if they were the only ones that exist. Any per-asignatura path (`01_NORMATIVA_CURRICULO/normativa_registro.md`, `ficha.yaml → asignatura.curso_academico`) stays relative to "la asignatura en curso de esta comprobación" (this skill already loops per Task 1 Step 4's exception rule for report-type commands with no asignatura specified).

- [ ] **Step 3: Verify**

Run: `grep -n "vcf-\|VCF_TSEAS\|\bVCF\b" ".claude/skills/asig-vigilancia/SKILL.md"`

Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/asig-vigilancia/"
git commit -m "Migra /vcf-vigilancia a /asig-vigilancia (genérico multi-asignatura)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 14: Migrate `vcf-diversidad` → `asig-diversidad`

**Files:**
- Create: `.claude/skills/asig-diversidad/SKILL.md`

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1).

- [ ] **Step 1: Copy the file**

```bash
mkdir -p ".claude/skills/asig-diversidad"
cp ".claude/skills/vcf-diversidad/SKILL.md" ".claude/skills/asig-diversidad/SKILL.md"
```

- [ ] **Step 2: Edit frontmatter, title, body**

- `name: vcf-diversidad` → `name: asig-diversidad`
- `# /vcf-diversidad — Atención a la diversidad individual (VCF/TSEAS)` → `# /asig-diversidad — Atención a la diversidad individual`
- `cat ".claude/skills/asig-diversidad/SKILL.md"` and fix any `VCF_TSEAS` path or "de VCF" wording the same way as prior tasks. This skill's `description` had zero VCF/vcf- mentions per the earlier survey — double check with the grep in Step 3 regardless.

- [ ] **Step 3: Verify**

Run: `grep -n "vcf-\|VCF_TSEAS\|\bVCF\b" ".claude/skills/asig-diversidad/SKILL.md"`

Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/asig-diversidad/"
git commit -m "Migra /vcf-diversidad a /asig-diversidad (genérico multi-asignatura)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 15: Migrate `vcf-analitica` → `asig-analitica`

**Files:**
- Create: `.claude/skills/asig-analitica/SKILL.md`

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1).

- [ ] **Step 1: Copy the file**

```bash
mkdir -p ".claude/skills/asig-analitica"
cp ".claude/skills/vcf-analitica/SKILL.md" ".claude/skills/asig-analitica/SKILL.md"
```

- [ ] **Step 2: Edit frontmatter, title, body**

- `name: vcf-analitica` → `name: asig-analitica`
- `description:` "Analiza calificaciones reales del alumnado de VCF por RA/criterio ... Úsalo cuando el usuario pida analizar resultados, calificaciones o rendimiento de VCF; si no hay datos, informa de ello en vez de generar nada." → "del alumnado de VCF" → "del alumnado de la asignatura resuelta"; "de VCF;" → "de una asignatura;"
- `# /vcf-analitica — Analítica y mejora (VCF/TSEAS)` → `# /asig-analitica — Analítica y mejora`
- `cat ".claude/skills/asig-analitica/SKILL.md"` and fix any remaining `VCF_TSEAS` path the same way as prior tasks.

- [ ] **Step 3: Verify**

Run: `grep -n "vcf-\|VCF_TSEAS\|\bVCF\b" ".claude/skills/asig-analitica/SKILL.md"`

Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/asig-analitica/"
git commit -m "Migra /vcf-analitica a /asig-analitica (genérico multi-asignatura)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 16: Migrate `vcf-recursos` → `asig-recursos` (includes `reference/` and `scripts/`)

**Files:**
- Create: `.claude/skills/asig-recursos/SKILL.md`
- Create: `.claude/skills/asig-recursos/reference/FORMDEPOR_especificaciones_tecnicas_powerpoint.md`
- Create: `.claude/skills/asig-recursos/scripts/generar_pptx.py`
- Create: any other file currently under `.claude/skills/vcf-recursos/` (check with Step 1 below — the survey earlier in this session found a `reference/` folder whose full contents weren't enumerated)

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1).

- [ ] **Step 1: See everything that needs to move**

Run: `find ".claude/skills/vcf-recursos" -type f`

Copy every file listed to the same relative path under `.claude/skills/asig-recursos/`:
```bash
mkdir -p ".claude/skills/asig-recursos"
cp -r ".claude/skills/vcf-recursos/." ".claude/skills/asig-recursos/"
```

- [ ] **Step 2: Edit `SKILL.md` frontmatter, title, body**

- `name: vcf-recursos` → `name: asig-recursos`
- `# /vcf-recursos — Recursos digitales (VCF/TSEAS)` → `# /asig-recursos — Recursos digitales`
- The skill body references "VCF/TSEAS es contenido de **FORMDEPOR Formación**" as the reason it defaults to `--marca formacion` — reword to: "El contenido curricular de este departamento es de **FORMDEPOR Formación** (formación profesional, enseñanzas deportivas, documentación académica e institucional — sección 4.1 de la guía), así que el script usa `--marca formacion` por defecto..." (keep the rest of that sentence about the hex colors unchanged).
- Any path like `09_RECURSOS_DIGITALES/POWERPOINT/<UD>_esquema.md` or `.claude/skills/vcf-recursos/scripts/generar_pptx.py` referenced inside the body: replace `vcf-recursos` → `asig-recursos`, and any `ASIGNATURAS/VCF_TSEAS/09_RECURSOS_DIGITALES/...` → `ASIGNATURAS/<CODIGO>_<CICLO>/09_RECURSOS_DIGITALES/...`.
- The Gamma and NotebookLM subsections: replace any "de VCF" with "de la asignatura resuelta".

- [ ] **Step 3: Check `generar_pptx.py` for hardcoded paths**

Run: `grep -n "vcf\|VCF" ".claude/skills/asig-recursos/scripts/generar_pptx.py"`

If this prints matches referring to file paths or defaults (not just incidental text in a comment), fix them the same way (`vcf-recursos` → `asig-recursos`, `VCF_TSEAS` → generic). If it only matches things like a `--marca` value unrelated to path resolution, leave it — the script takes `--input`/`--output` as CLI arguments already, it doesn't hardcode an asignatura path itself.

- [ ] **Step 4: Verify**

Run: `grep -rn "vcf-\|VCF_TSEAS" ".claude/skills/asig-recursos/" | grep -v "reference/FORMDEPOR_especificaciones"`

Expected: no output (the FORMDEPOR spec file is excluded from this check only because Task instructions above didn't touch it — but confirm separately that it never mentions `vcf-` or `VCF_TSEAS` either):

Run: `grep -n "vcf-\|VCF_TSEAS" ".claude/skills/asig-recursos/reference/FORMDEPOR_especificaciones_tecnicas_powerpoint.md"`

Expected: no output.

- [ ] **Step 5: Commit**

```bash
git add ".claude/skills/asig-recursos/"
git commit -m "Migra /vcf-recursos a /asig-recursos (genérico multi-asignatura)

Incluye reference/ (guía FORMDEPOR, ya genérica de marca) y scripts/
(generar_pptx.py, sin cambios de lógica).

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 17: Migrate `vcf-estado` → `asig-estado` (includes `reference/`, generalize full-report mode)

**Files:**
- Create: `.claude/skills/asig-estado/SKILL.md`
- Create: `.claude/skills/asig-estado/reference/plantilla_resumen_semanal.md`

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1).
- Produces: the artifact template path `.claude/skills/asig-estado/reference/plantilla_resumen_semanal.md`, which the SKILL.md's "Modo resumen semanal" section must reference by its new path.

- [ ] **Step 1: Copy the files**

```bash
mkdir -p ".claude/skills/asig-estado/reference"
cp ".claude/skills/vcf-estado/SKILL.md" ".claude/skills/asig-estado/SKILL.md"
cp ".claude/skills/vcf-estado/reference/plantilla_resumen_semanal.md" ".claude/skills/asig-estado/reference/plantilla_resumen_semanal.md"
```

- [ ] **Step 2: Edit `SKILL.md` frontmatter and title**

- `name: vcf-estado` → `name: asig-estado`
- `# /vcf-estado — Coordinador de las asignaturas del departamento` → `# /asig-estado — Coordinador de las asignaturas del departamento` (only the command name token changes; the rest of this title was already generalized in an earlier session and needs no further edit).

- [ ] **Step 3: Check the full-report mode (Tareas 1-7) is genuinely multi-asignatura**

This skill's weekly-digest mode was already generalized to loop over `ASIGNATURAS/*/` in a previous session, but the on-demand full-report mode (Tareas 1-7) may still implicitly assume a single asignatura in places. Run: `cat ".claude/skills/asig-estado/SKILL.md"` and check task 1-7's wording:
- If the user asks for "el estado" without naming an asignatura and there is more than one `ASIGNATURAS/*/ficha.yaml`, the full report must cover **all** of them (one full five-block report per asignatura), matching the exception rule in `CLAUDE.md → "Cómo se resuelve la asignatura"` step 4.
- If the user names a specific asignatura ("el estado de MET"), the full report covers only that one, resolved per the standard 3-step rule.
- Add this distinction explicitly to the "Rol" or "Tareas" section if it isn't already unambiguous after the Task 1 rewrite — the existing text ("Coordinador de asignaturas: supervisa todas las asignaturas que existan bajo `DEPARTAMENTO_DOCENTE/ASIGNATURAS/`") already implies this; make sure task 6 ("Presenta un resumen con cinco bloques... Si hay más de una asignatura, un bloque por asignatura") reads as applying whether the user asked for "el estado" (all) or "el estado de MET" (all bloques, but only for MET) — reword task 6 if it currently reads as always covering every asignatura regardless of what the user asked.

- [ ] **Step 4: Update the reference path in the "Modo resumen semanal" section**

Find the line referencing `.claude/skills/vcf-estado/reference/plantilla_resumen_semanal.md` and change it to `.claude/skills/asig-estado/reference/plantilla_resumen_semanal.md`.

- [ ] **Step 5: Check `reference/plantilla_resumen_semanal.md` itself**

Run: `grep -n "vcf-\|VCF_TSEAS\|\bVCF\b" ".claude/skills/asig-estado/reference/plantilla_resumen_semanal.md"`

If anything prints (the file was written generically already, referring to "cada asignatura" — but verify), fix it the same way as prior tasks.

- [ ] **Step 6: Verify SKILL.md**

Run: `grep -n "vcf-\|VCF_TSEAS\|\bVCF\b" ".claude/skills/asig-estado/SKILL.md"`

Expected: no output.

- [ ] **Step 7: Commit**

```bash
git add ".claude/skills/asig-estado/"
git commit -m "Migra /vcf-estado a /asig-estado (genérico multi-asignatura)

El modo resumen semanal ya recorría todas las asignaturas; ahora el
informe completo bajo demanda también cubre todas cuando no se
especifica ninguna, igual que el resto de comandos informativos.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 18: Migrate `vcf-revision` → `asig-revision` (update cross-references)

**Files:**
- Create: `.claude/skills/asig-revision/SKILL.md`

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1); the final `/asig-*` names from Tasks 4-17 and 19 (this skill lists sibling commands by name).

- [ ] **Step 1: Copy the file**

```bash
mkdir -p ".claude/skills/asig-revision"
cp ".claude/skills/vcf-revision/SKILL.md" ".claude/skills/asig-revision/SKILL.md"
```

- [ ] **Step 2: Edit frontmatter and title**

- `name: vcf-revision` → `name: asig-revision`
- `# /vcf-revision — Revisión y aprobación de documentos (VCF/TSEAS)` → `# /asig-revision — Revisión y aprobación de documentos`

- [ ] **Step 3: Update every hardcoded `VCF_TSEAS` path**

Run: `grep -n "VCF_TSEAS" ".claude/skills/asig-revision/SKILL.md"`

This skill's "Entradas" section lists several fixed paths (`05_UNIDADES/`, `06_TEMARIO/VIGENTE/`, `07_ACTIVIDADES_TAREAS/VIGENTE/`, `08_EVALUACION/`, the 4 base documents, `09_RECURSOS_DIGITALES/`) — none of these currently spell out `VCF_TSEAS` explicitly (they're written as relative paths already, per the file surveyed earlier this session), but confirm with the grep above and prepend `DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/` context if any absolute-looking path is missing it. Add one sentence near the top of "Entradas" clarifying: "Todas las rutas de esta sección son relativas a la asignatura resuelta según CLAUDE.md → \"Cómo se resuelve la asignatura\" — si el usuario no especifica ninguna y hay más de una, pregúntale cuál."

- [ ] **Step 4: Update every `/vcf-*` cross-reference**

Run: `grep -n "vcf-" ".claude/skills/asig-revision/SKILL.md"`

Replace every match with the `asig-` equivalent (this skill mentions `/vcf-unidad`, `/vcf-tema`, `/vcf-tarea`, `/vcf-examen`, `/vcf-programacion`, `/vcf-normativa`, `/vcf-recursos`, `/vcf-auditoria` — confirm the exact set with the grep, since the count found earlier this session was 18 matches, more than these 8 command names alone, so some matches are the skill's own `vcf-revision` self-references and the `10_DIVERSIDAD`/`11_SEGUIMIENTO_RESULTADOS` exclusion list mentioning `/vcf-drive`, `/vcf-calendar-sync`, `/vcf-estado` too).

- [ ] **Step 5: Verify**

Run: `grep -n "vcf-\|\bVCF\b" ".claude/skills/asig-revision/SKILL.md"`

Expected: no output (note: `VCF_TSEAS` isn't in this grep because Step 3 already handled path context via prose rather than literal string replacement — re-run `grep -n "VCF_TSEAS" ".claude/skills/asig-revision/SKILL.md"` too and confirm it's also empty).

- [ ] **Step 6: Commit**

```bash
git add ".claude/skills/asig-revision/"
git commit -m "Migra /vcf-revision a /asig-revision (genérico multi-asignatura)

Actualiza las referencias cruzadas a las demás skills (unidad, tema,
tarea, examen, programacion, normativa, recursos, auditoria, drive,
calendar-sync, estado) a sus nuevos nombres /asig-*.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 19: Migrate `vcf-mantenimiento` → `asig-mantenimiento` (update cross-references)

**Files:**
- Create: `.claude/skills/asig-mantenimiento/SKILL.md`

**Interfaces:**
- Consumes: `CLAUDE.md → "Cómo se resuelve la asignatura"` (Task 1); the final `/asig-*` names from Tasks 4-18 (this skill lists and triggers sibling commands by name).

- [ ] **Step 1: Copy the file**

```bash
mkdir -p ".claude/skills/asig-mantenimiento"
cp ".claude/skills/vcf-mantenimiento/SKILL.md" ".claude/skills/asig-mantenimiento/SKILL.md"
```

- [ ] **Step 2: Edit frontmatter and title**

- `name: vcf-mantenimiento` → `name: asig-mantenimiento`
- `# /vcf-mantenimiento — Mantenimiento y salud del proyecto (VCF/TSEAS)` → `# /asig-mantenimiento — Mantenimiento y salud del proyecto`

- [ ] **Step 3: Genericize the scope description**

This skill's "Rol" and "Entradas" describe sweeping "todo `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/`" — reword to sweep every asignatura by default when none is specified (matching the exception rule in `CLAUDE.md → "Cómo se resuelve la asignatura"`, same pattern as `asig-estado`'s weekly digest): "todo `DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/` de cada asignatura existente (o solo de la indicada, si el usuario menciona una)". Apply the same rewording anywhere else `VCF_TSEAS` appears as a literal path.

- [ ] **Step 4: Update every `/vcf-*` cross-reference**

Run: `grep -n "vcf-" ".claude/skills/asig-mantenimiento/SKILL.md"`

This skill mentions (per the 30 matches found in the earlier survey) `/vcf-unidad`, `/vcf-tema`, `/vcf-tarea`, `/vcf-examen`, `/vcf-programacion`, `/vcf-auditoria`, `/vcf-normativa`, `/vcf-recursos`, `/vcf-diversidad`, `/vcf-analitica`, `/vcf-revision`, plus its own `vcf-mantenimiento` self-references and the `propuestas_mejora_skills/<skill>_<YYYY-MM-DD>.md` pattern. Replace every command-name match with its `asig-` equivalent.

- [ ] **Step 5: Verify**

Run: `grep -n "vcf-\|VCF_TSEAS\|\bVCF\b" ".claude/skills/asig-mantenimiento/SKILL.md"`

Expected: no output.

- [ ] **Step 6: Commit**

```bash
git add ".claude/skills/asig-mantenimiento/"
git commit -m "Migra /vcf-mantenimiento a /asig-mantenimiento (genérico multi-asignatura)

Barre todas las asignaturas por defecto (o solo la indicada) y
actualiza las referencias cruzadas a las demás skills a sus nuevos
nombres /asig-*.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 20: Update the 2 Google Calendar event descriptions

**Files:** none (Google Calendar API only, no repo files).

**Interfaces:**
- Consumes: the final command names `/asig-mantenimiento` and `/asig-estado` (Tasks 17, 19).

- [ ] **Step 1: Find the two events**

Use `mcp__claude_ai_Google_Calendar__search_events` with query `"mantenimiento"` and separately with query `"resumen semanal"`. Confirm you get the recurring event "VCF · Mantenimiento quincenal (/vcf-mantenimiento)" (`recurringEventId` starting `odtc3pbkqsi...`) and "VCF · Resumen semanal (/vcf-estado)" (id `6sn755eekbo7c1u1hj0aorpq8o`).

- [ ] **Step 2: Update the mantenimiento event's description**

Use `mcp__claude_ai_Google_Calendar__update_event` on the recurring event id found in Step 1, changing only the `description` field from:
```
Recordatorio para abrir Claude Code en el proyecto "PROYECTO 3_ENTORNO DOCENTE" y ejecutar /vcf-mantenimiento: barrido de coherencia de todo el proyecto VCF, regeneración automática en BORRADOR de lo desactualizado, y aviso de hallazgos. Se ejecuta en local (necesita escribir en el repositorio) — este evento es el único disparador, no hay ejecución automática en la nube.
```
to:
```
Recordatorio para abrir Claude Code en el proyecto "PROYECTO 3_ENTORNO DOCENTE" y ejecutar /asig-mantenimiento: barrido de coherencia de todas las asignaturas del departamento, regeneración automática en BORRADOR de lo desactualizado, y aviso de hallazgos. Se ejecuta en local (necesita escribir en el repositorio) — este evento es el único disparador, no hay ejecución automática en la nube.
```
Do not change the event's `summary` (title) or recurrence — only `description`.

- [ ] **Step 3: Update the resumen semanal event's description**

Use `mcp__claude_ai_Google_Calendar__update_event` on event id `6sn755eekbo7c1u1hj0aorpq8o`, changing `description` from:
```
Recordatorio para abrir Claude Code en el proyecto "PROYECTO 3_ENTORNO DOCENTE" y ejecutar /vcf-estado en modo resumen semanal: genera un artefacto HTML visual con lo pendiente de cada asignatura esta semana y la que viene (casillas calculadas automáticamente según si el archivo ya existe, no manuales) y deja un borrador en Gmail con el enlace, sin enviarlo. Se ejecuta en local — este evento es el único disparador, no hay ejecución automática en la nube.
```
to:
```
Recordatorio para abrir Claude Code en el proyecto "PROYECTO 3_ENTORNO DOCENTE" y ejecutar /asig-estado en modo resumen semanal: genera un artefacto HTML visual con lo pendiente de cada asignatura esta semana y la que viene (casillas calculadas automáticamente según si el archivo ya existe, no manuales) y deja un borrador en Gmail con el enlace, sin enviarlo. Se ejecuta en local — este evento es el único disparador, no hay ejecución automática en la nube.
```
Do not change the event's `summary` or recurrence — only `description`.

- [ ] **Step 4: Verify**

Re-run `mcp__claude_ai_Google_Calendar__search_events` with query `"asig-"` and confirm both events now appear with the updated description, and re-run query `"vcf-mantenimiento"` / `"vcf-estado"` and confirm the description text no longer matches (the event `summary` still literally contains "VCF" in its title by design — per the spec, titles stay as-is; only descriptions change).

No commit for this task (no repo files changed).

---

### Task 21: Cross-reference sweep across all `asig-*` skills and `CLAUDE.md`

**Files:** none created/modified (verification only — fixes go back into the relevant task's files if anything is found).

**Interfaces:**
- Consumes: every file produced by Tasks 1, 4-19.

- [ ] **Step 1: Sweep for stray `vcf-` references**

Run: `grep -rn "vcf-" ".claude/skills/asig-"*/  "CLAUDE.md"`

Expected: no output. If anything prints, open that file, fix the reference to its `asig-` equivalent following the same pattern used in that file's migration task, and re-run this grep until it's empty.

- [ ] **Step 2: Sweep for stray literal `VCF_TSEAS` references**

Run: `grep -rln "VCF_TSEAS" ".claude/skills/asig-"*/`

Expected: no output. Fix any hit the same way (replace with `<CODIGO>_<CICLO>` language per the pattern established in Tasks 4-19).

- [ ] **Step 3: Confirm the old `vcf-*` skills are untouched (not yet deleted)**

Run: `ls -d ".claude/skills/vcf-"*/ | wc -l`

Expected: `16` (they're deleted in Task 23, not here — this step is just confirming nothing was accidentally deleted early).

- [ ] **Step 4: Confirm all 16 new skills exist**

Run: `ls -d ".claude/skills/asig-"*/ | sort`

Expected: exactly these 16 directories: `asig-analitica/`, `asig-auditoria/`, `asig-calendar-sync/`, `asig-diversidad/`, `asig-drive/`, `asig-estado/`, `asig-examen/`, `asig-mantenimiento/`, `asig-normativa/`, `asig-programacion/`, `asig-recursos/`, `asig-revision/`, `asig-tarea/`, `asig-tema/`, `asig-unidad/`, `asig-vigilancia/`.

No commit for this task unless Step 1 or 2 found something to fix (in which case, commit that fix with a message identifying which skill's leftover reference was corrected).

---

### Task 22: Smoke test — run `/asig-estado` for VCF and compare to the prior report

**Files:** none created/modified — this is a manual verification task.

**Interfaces:**
- Consumes: `asig-estado` (Task 17), `MET_TSEAS/` (Task 2).

- [ ] **Step 1: Run the generalized full report for VCF specifically**

In a real conversation turn (not scriptable), invoke `/asig-estado` and ask for the state of VCF specifically (e.g. "dame el estado de VCF"). Confirm:
- It resolves to `VCF_TSEAS` without asking for clarification (only one asignatura named "VCF" or matching code `VCF` exists).
- The five blocks (Pendiente de revisión, Huecos de contenido, Próximos hitos, Incoherencias, Próxima preparación) come back **empty or near-empty** for huecos de contenido (VCF's content is fully approved as of the `/vcf-revision` session earlier today) and reflect the real state of the repo (no unidades/temario/tareas/examen gaps, since all of it is APROBADO).

- [ ] **Step 2: Run the same report with no asignatura specified**

Ask for "el estado" with no asignatura named. Confirm it now returns a report covering **both** VCF and MET (MET's report should show every block as "todo pendiente" / huecos everywhere, since `MET_TSEAS/ficha.yaml` is still an empty skeleton — that's the expected, correct output, not a bug).

- [ ] **Step 3: Run the same report for MET specifically**

Ask for "el estado de MET" or "el estado de metodología". Confirm it resolves to `MET_TSEAS` (via `asignatura.nombre` substring match, testing the "nombre" branch of the resolution rule, not just "codigo") and returns a report showing the empty-skeleton state accurately (ficha.yaml fields null, no unidades, no folders populated) without erroring or falling back to VCF's data.

- [ ] **Step 4: Test the ambiguous/no-match path on a content-generation command**

Ask `/asig-unidad` to generate something without naming any asignatura (e.g. "genera la unidad 1"). Confirm it does **not** guess — it asks which asignatura (VCF or MET) before doing anything, per `CLAUDE.md → "Cómo se resuelve la asignatura"` step 3. This is the one step in this task that must NOT produce any file — if it generates content without asking, that's a defect in whichever skill's resolution logic didn't get genericized correctly; go back to that skill's migration task and fix it.

If all four checks pass, this task is done — no commit needed (nothing was written to the repo by this task itself, beyond whatever the assistant may have asked/confirmed in conversation).

---

### Task 23: Remove the old `vcf-*` skill folders

**Files:**
- Delete: all 16 `.claude/skills/vcf-*/` directories

**Interfaces:**
- Consumes: Task 21 (cross-reference sweep clean) and Task 22 (smoke test passed) — **do not run this task until both have passed.**

- [ ] **Step 1: Delete**

```bash
cd "/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE"
git rm -r ".claude/skills/vcf-analitica" ".claude/skills/vcf-auditoria" \
  ".claude/skills/vcf-calendar-sync" ".claude/skills/vcf-diversidad" \
  ".claude/skills/vcf-drive" ".claude/skills/vcf-estado" \
  ".claude/skills/vcf-examen" ".claude/skills/vcf-mantenimiento" \
  ".claude/skills/vcf-normativa" ".claude/skills/vcf-programacion" \
  ".claude/skills/vcf-recursos" ".claude/skills/vcf-revision" \
  ".claude/skills/vcf-tarea" ".claude/skills/vcf-tema" \
  ".claude/skills/vcf-unidad" ".claude/skills/vcf-vigilancia"
```

- [ ] **Step 2: Verify**

Run: `ls -d ".claude/skills/vcf-"*/ 2>&1`

Expected: `ls: cannot access '.claude/skills/vcf-*/': No such file or directory` (or equivalent "no such file" message — the glob matches nothing).

Run: `ls -d ".claude/skills/asig-"*/ | wc -l`

Expected: `16`.

- [ ] **Step 3: Commit**

```bash
git commit -m "$(cat <<'EOF'
Elimina las 16 skills /vcf-* ya migradas a /asig-*

Última confirmación antes de borrar: la barrida de referencias cruzadas
(sin vcf- ni VCF_TSEAS sueltos en .claude/skills/asig-*/ ni CLAUDE.md) y
la prueba de humo de /asig-estado sobre VCF y MET han pasado. Cierra
docs/superpowers/specs/2026-07-28-generalizacion-comandos-multi-asignatura-design.md.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

## Self-Review Notes

**Spec coverage:** decisions 1-2 (generalize, `/asig-*` prefix) → Tasks 1, 4-19, 23. Decision 3 (natural-language + short code resolution) → Task 1 Step 4, exercised in Task 22. Decision 4 (normativa without shared ciclo level) → Task 13 Step 2 explicitly keeps per-asignatura checks; Task 2 does not introduce any ciclo-level folder. Decision 5 (all 16 skills, not just the core) → Tasks 4-19 cover all 16. Decision 6 (zero changes to VCF content except README command names) → Global Constraints + Task 3 scoped exactly to that. "Efectos secundarios" (Calendar events) → Task 20. "Riesgos y mitigación" (smoke test, cross-reference sweep) → Tasks 21-22. "Fuera de alcance" (populating MET_TSEAS with real content) → explicitly not present in any task; Task 2 only creates the empty skeleton, matching the spec's carve-out.

**Placeholder scan:** every task has commands with expected output, or concrete before/after text for edits. No "TBD"/"handle appropriately" language.

**Type consistency:** the folder-name token `<CODIGO>_<CICLO>` and the section anchor `CLAUDE.md → "Cómo se resuelve la asignatura"` are used identically (same wording) across Tasks 1 and 4-19, so a fresh implementer reading any single task recognizes the same reference.
