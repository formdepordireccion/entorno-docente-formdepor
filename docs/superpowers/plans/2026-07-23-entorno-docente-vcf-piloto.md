# Entorno docente vivo — Piloto VCF/TSEAS — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir el andamiaje de carpetas, el modelo de datos y los 7 comandos (`/vcf-estado`, `/vcf-normativa`, `/vcf-auditoria`, `/vcf-programacion`, `/vcf-unidad`, `/vcf-tema`, `/vcf-examen`) que implementan el piloto del entorno docente para el módulo Valoración de la Condición Física (VCF), ciclo TSEAS, Formdepor, Extremadura, curso 2026-2027.

**Architecture:** Sistema local-first sin backend ni base de datos: la estructura de carpetas es el almacén, `ficha.yaml` es el modelo de datos, `CLAUDE.md` es el contexto/reglas compartido, y cada agente del documento original es un [Claude Code Skill](https://docs.claude.com) de proyecto (`.claude/skills/<nombre>/SKILL.md`) invocable como `/vcf-<nombre>`. Git da el control de versiones.

**Tech Stack:** Markdown, YAML, Bash (scaffolding), git. No hay framework de tests tradicional (no es código de aplicación) — la verificación de cada tarea es estructural (comprobación de árbol de carpetas / frontmatter YAML con `find`/`grep`) más una invocación funcional del skill contra un caso real, comprobada contra una lista de criterios de aceptación explícita.

## Global Constraints

- Nunca se modifica normativa, calificaciones, ponderaciones o documentos oficiales sin revisión y autorización docente explícita (regla del spec).
- Todo documento generado queda en `estado: borrador` (o `BORRADOR` en el nombre de archivo); nada pasa a `aprobado`/`APROBADO` sin confirmación explícita del usuario.
- Ningún skill inventa datos personales ni diagnósticos de alumnado — aplica sobre todo a la sección de diversidad de `/vcf-unidad`.
- Contenido nuevo se genera en Markdown. Nomenclatura de archivo: `ASIGNATURA_TIPO_UD_CURSO_VERSION_ESTADO.ext` (ejemplo: `VCF_UNIDAD_UD03_2026-2027_V01_BORRADOR.md`).
- Las integraciones con Google Drive/Calendar son siempre bajo petición explícita del usuario en el momento de usarlas — nunca automáticas ni en segundo plano (fuera de alcance de este plan; no se implementan aquí).
- El material original de `3. VALORACIÓN 25_26/` nunca se mueve ni se borra; solo `/vcf-auditoria` puede copiarlo a la nueva estructura, y solo tras confirmación explícita del usuario.
- Cada tarea termina con un commit de git.
- Ruta raíz del proyecto (repo git): `/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE/`. Todas las rutas de archivo de este plan son relativas a esa raíz.

---

### Task 1: Andamiaje de carpetas de `DEPARTAMENTO_DOCENTE/`

**Files:**
- Create: `DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/01_NORMATIVA_CURRICULO/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/02_PROGRAMACION/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/03_MAPA_CURRICULAR/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/04_TEMPORALIZACION/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/05_UNIDADES/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/VIGENTE/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/REFERENCIA_HISTORICA/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS/VIGENTE/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/08_EVALUACION/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/09_RECURSOS_DIGITALES/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/10_DIVERSIDAD/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/11_SEGUIMIENTO_RESULTADOS/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/12_RECUPERACION/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/13_MEMORIA_FINAL/README.md`
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/14_HISTORICO_CAMBIOS/README.md`

**Interfaces:**
- Consumes: nada (primera tarea).
- Produces: el árbol completo de carpetas de `DEPARTAMENTO_DOCENTE/`, que todas las tareas siguientes usan como destino de escritura. Cada carpeta queda no vacía (README.md) y por tanto trackeada por git.

- [ ] **Step 1: Crear el árbol de carpetas**

```bash
cd "/Users/marioperezquintero/Claude/PROYECTO 3_ENTORNO DOCENTE"
mkdir -p "DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/01_NORMATIVA_CURRICULO"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/02_PROGRAMACION"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/03_MAPA_CURRICULAR"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/04_TEMPORALIZACION"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/05_UNIDADES"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/VIGENTE"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/REFERENCIA_HISTORICA"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS/VIGENTE"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/08_EVALUACION"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/09_RECURSOS_DIGITALES"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/10_DIVERSIDAD"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/11_SEGUIMIENTO_RESULTADOS"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/12_RECUPERACION"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/13_MEMORIA_FINAL"
mkdir -p "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/14_HISTORICO_CAMBIOS"
```

- [ ] **Step 2: Escribir un README.md por carpeta explicando su propósito**

Usa el editor de archivos (no bash) para crear cada `README.md` con este contenido exacto (una línea de propósito + qué comando la alimenta):

`DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/README.md`:
```markdown
# Centro de control

Panel simplificado del proyecto VCF/TSEAS: estado, alertas y pendientes.
Alimentado por `/vcf-estado`. No contiene documentos oficiales, solo informes.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/README.md`:
```markdown
# Ficha

Modelo de datos de la asignatura (`ficha.yaml`). Fuente única de verdad que
leen y actualizan todos los comandos `/vcf-*`.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/01_NORMATIVA_CURRICULO/README.md`:
```markdown
# Normativa y currículo

RD estatal del título TSEAS, normativa autonómica de Extremadura para el
módulo VCF, y matriz de alineación curricular. Alimentado por `/vcf-normativa`.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/02_PROGRAMACION/README.md`:
```markdown
# Programación didáctica

Programación didáctica del curso 2026-2027. Alimentado por `/vcf-programacion`.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/03_MAPA_CURRICULAR/README.md`:
```markdown
# Mapa curricular

Matriz que cruza resultados de aprendizaje, criterios de evaluación,
contenidos, unidades e instrumentos. Generado por `/vcf-normativa`.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/04_TEMPORALIZACION/README.md`:
```markdown
# Temporalización

Calendario de unidades, evaluaciones, entregas y recuperaciones del curso
2026-2027. Alimentado por `/vcf-programacion`.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/05_UNIDADES/README.md`:
```markdown
# Unidades didácticas

Unidades didácticas completas (objetivos, RA, criterios, contenidos,
metodología, actividades, recursos, diversidad, evaluación, recuperación,
ampliación). Alimentado por `/vcf-unidad`.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/VIGENTE/README.md`:
```markdown
# Temario vigente

Temario actual del curso 2026-2027: versión docente, apuntes de alumnado,
resúmenes, esquemas, glosarios y preguntas de repaso. Alimentado por `/vcf-tema`.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/REFERENCIA_HISTORICA/README.md`:
```markdown
# Referencia histórica — Temario

Temas de cursos anteriores (18/19 a 24/25) migrados desde
`3. VALORACIÓN 25_26/` por `/vcf-auditoria`, conservados como banco de
referencia para `/vcf-tema`. No se edita ni se marca como vigente.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS/VIGENTE/README.md`:
```markdown
# Actividades y tareas vigentes

Actividades y tareas del curso 2026-2027, vinculadas a resultados de
aprendizaje y criterios de evaluación.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/README.md`:
```markdown
# Referencia histórica — Tareas

Tareas de cursos anteriores migradas desde `3. VALORACIÓN 25_26/` por
`/vcf-auditoria`, conservadas como banco de referencia.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/08_EVALUACION/README.md`:
```markdown
# Evaluación

Exámenes, rúbricas, banco de preguntas y solucionarios. Alimentado por
`/vcf-examen`. Los solucionarios se guardan en archivo separado del
instrumento visible para el alumnado.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/09_RECURSOS_DIGITALES/README.md`:
```markdown
# Recursos digitales

Presentaciones, infografías, formularios y materiales para aula virtual.
Fuera de alcance del piloto (Fase 1); carpeta reservada para cuando se
active esta capacidad.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/10_DIVERSIDAD/README.md`:
```markdown
# Atención a la diversidad

Medidas DUA y de apoyo transversales a la asignatura. Las medidas
específicas por unidad viven dentro de cada unidad en `05_UNIDADES/`,
generadas por `/vcf-unidad`. Nunca contiene diagnósticos ni datos
personales de alumnado.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/11_SEGUIMIENTO_RESULTADOS/README.md`:
```markdown
# Seguimiento y resultados

Registro de sesiones impartidas, incidencias y comparación plan vs.
realidad. Fuera de alcance del piloto (Fase 1); carpeta reservada.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/12_RECUPERACION/README.md`:
```markdown
# Recuperación

Planes y materiales de recuperación por unidad o evaluación.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/13_MEMORIA_FINAL/README.md`:
```markdown
# Memoria final

Memoria final de curso. Fuera de alcance del piloto (Fase 1); carpeta
reservada para el cierre del curso 2026-2027.
```

`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/14_HISTORICO_CAMBIOS/README.md`:
```markdown
# Histórico de cambios

Registro legible de migraciones y cambios relevantes (complementario al
historial de git). `/vcf-auditoria` escribe aquí `migraciones.md`.
```

- [ ] **Step 3: Verificar el árbol de carpetas**

Run: `find DEPARTAMENTO_DOCENTE -type d | sort`

Expected (18 líneas):
```
DEPARTAMENTO_DOCENTE
DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL
DEPARTAMENTO_DOCENTE/ASIGNATURAS
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/01_NORMATIVA_CURRICULO
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/02_PROGRAMACION
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/03_MAPA_CURRICULAR
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/04_TEMPORALIZACION
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/05_UNIDADES
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/REFERENCIA_HISTORICA
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/VIGENTE
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS/VIGENTE
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/08_EVALUACION
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/09_RECURSOS_DIGITALES
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/10_DIVERSIDAD
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/11_SEGUIMIENTO_RESULTADOS
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/12_RECUPERACION
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/13_MEMORIA_FINAL
DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/14_HISTORICO_CAMBIOS
```

Run: `find DEPARTAMENTO_DOCENTE -name README.md | wc -l`

Expected: `18`

- [ ] **Step 4: Commit**

```bash
git add DEPARTAMENTO_DOCENTE
git commit -m "Scaffold DEPARTAMENTO_DOCENTE folder tree for VCF/TSEAS pilot"
```

---

### Task 2: Modelo de datos `ficha.yaml`

**Files:**
- Create: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml`

**Interfaces:**
- Consumes: carpeta `00_FICHA/` creada en Task 1.
- Produces: `ficha.yaml` con las claves `asignatura.{nombre,codigo,ciclo,centro,comunidad_autonoma,curso_academico,docente,horas_totales,horas_semanales}`, `normativa.{rd_estatal,decreto_curriculo_autonomico}`, `resultados_aprendizaje`, `criterios_evaluacion`, `contenidos`, `unidades`, `ponderaciones`, `calendario_ref`, `metodologia`, `instrumentos_evaluacion`, `estado`, `ultima_revision`, `proxima_revision`, `documentos_vinculados`. Todas las tareas siguientes (`/vcf-*`) leen y escriben sobre estas claves exactas — no renombrarlas.

- [ ] **Step 1: Escribir `ficha.yaml`**

```yaml
asignatura:
  nombre: Valoración de la Condición Física
  codigo: VCF
  ciclo: Técnico Superior en Enseñanza y Animación Sociodeportiva (TSEAS)
  centro: Formdepor
  comunidad_autonoma: Extremadura
  curso_academico: "2026-2027"
  docente: Mario Pérez Quintero
  horas_totales: null
  horas_semanales: null
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

- [ ] **Step 2: Verificar estructura del archivo**

Run:
```bash
grep -c "^asignatura:" "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml"
grep -c "^normativa:" "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml"
grep -c "^estado: borrador" "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml"
```

Expected: `1` en cada uno de los tres comandos.

- [ ] **Step 3: Commit**

```bash
git add "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml"
git commit -m "Add ficha.yaml data model for VCF/TSEAS"
```

---

### Task 3: `CLAUDE.md` — contexto y reglas comunes

**Files:**
- Create: `CLAUDE.md` (raíz del repo, para que Claude Code lo cargue automáticamente en cualquier sesión dentro de este proyecto)

**Interfaces:**
- Consumes: `ficha.yaml` (Task 2, referenciado por ruta), estructura de `DEPARTAMENTO_DOCENTE/` (Task 1).
- Produces: contexto de proyecto que todo skill de las Tasks 4-10 asume como ya cargado (no repiten estas reglas en su propio cuerpo, solo referencian casos concretos).

- [ ] **Step 1: Escribir `CLAUDE.md`**

```markdown
# Entorno docente — Formdepor / TSEAS / VCF

Este repositorio es el entorno docente vivo del módulo **Valoración de la
Condición Física (VCF)**, ciclo **Técnico Superior en Enseñanza y Animación
Sociodeportiva (TSEAS)**, centro **Formdepor**, comunidad autónoma
**Extremadura**, curso **2026-2027**.

Es el piloto (Fase 0 + Fase 1) de una arquitectura departamental más amplia
descrita en `entorno_preparacion_clases_compacto.md`. Ver
`docs/superpowers/specs/2026-07-23-entorno-docente-vcf-piloto-design.md`
para el diseño completo.

## Dónde está todo

- `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml` — modelo
  de datos único de la asignatura. Léelo antes de generar cualquier
  contenido para saber qué normativa, RA, criterios, contenidos y unidades
  ya existen.
- `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/` — las 15 carpetas numeradas
  del proyecto (normativa, programación, unidades, temario, evaluación...).
  Cada una tiene un `README.md` explicando su propósito.
- `3. VALORACIÓN 25_26/` — material histórico original (18/19 a 25/26).
  **Nunca se mueve ni se borra directamente**; solo el comando
  `/vcf-auditoria` puede copiar de aquí a `DEPARTAMENTO_DOCENTE/`, y solo
  tras confirmación explícita del usuario.

## Comandos disponibles

`/vcf-estado`, `/vcf-normativa`, `/vcf-auditoria`, `/vcf-programacion`,
`/vcf-unidad`, `/vcf-tema`, `/vcf-examen`. Cada uno vive en
`.claude/skills/<nombre>/SKILL.md` y documenta su propio rol, entradas,
tareas, salidas y límites.

## Reglas fijas (aplican siempre, con o sin comando explícito)

1. Normativa, calificaciones, ponderaciones y documentos oficiales **nunca**
   se modifican sin revisión y autorización explícita del docente.
2. Todo documento generado queda en `estado: borrador` / `BORRADOR` en el
   nombre de archivo. Nada pasa a `aprobado`/`APROBADO` sin que el usuario
   lo confirme explícitamente.
3. Nunca se inventan datos personales ni diagnósticos de alumnado —
   especialmente en las secciones de atención a la diversidad.
4. Contenido nuevo se escribe en Markdown. Nomenclatura de archivo:
   `ASIGNATURA_TIPO_UD_CURSO_VERSION_ESTADO.ext`
   (ejemplo: `VCF_UNIDAD_UD03_2026-2027_V01_BORRADOR.md`).
5. Las integraciones con Google Drive/Calendar se hacen solo cuando el
   usuario las pide explícitamente en ese momento — nunca en segundo plano.
6. Cada vez que el usuario aprueba un documento, se hace un commit de git
   con un mensaje que identifique el documento.
7. Si una norma, fecha o dato no se puede verificar con una fuente real, se
   dice explícitamente en vez de inventarlo.
```

- [ ] **Step 2: Verificar contenido mínimo**

Run:
```bash
grep -c "^## Reglas fijas" CLAUDE.md
grep -c "vcf-estado" CLAUDE.md
grep -c "ficha.yaml" CLAUDE.md
```

Expected: `1`, y al menos `1` en los otros dos (usa `grep -c` que cuenta líneas con coincidencia, no ocurrencias — basta con que sea ≥ 1).

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "Add root CLAUDE.md with VCF/TSEAS project context and rules"
```

---

### Task 4: Skill `/vcf-estado` (Coordinador / Centro de control)

**Files:**
- Create: `.claude/skills/vcf-estado/SKILL.md`

**Interfaces:**
- Consumes: `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml` (Task 2), árbol de carpetas (Task 1).
- Produces: nada persistente por defecto (solo reporta en el chat). Si el usuario pide guardarlo, escribe en `DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/estado_<YYYY-MM-DD>.md`.

- [ ] **Step 1: Escribir el skill**

```markdown
---
name: vcf-estado
description: Genera una foto de estado del proyecto VCF/TSEAS (rol de Coordinador / Centro de control) — qué falta en ficha.yaml, qué carpetas están vacías, próximos hitos del calendario e incoherencias detectadas. Úsalo cuando el usuario pida el estado, resumen, panel de control o "qué falta" de la asignatura VCF.
---

# /vcf-estado — Coordinador de la asignatura VCF/TSEAS

## Rol

Coordinador de asignatura: supervisa el proyecto VCF/TSEAS, no genera
contenido nuevo, solo informa.

## Entradas

- `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml`
- El contenido actual de las carpetas `01_NORMATIVA_CURRICULO/` a
  `14_HISTORICO_CAMBIOS/` dentro de `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/`
- `04_TEMPORALIZACION/calendario_26_27.md` si existe
- La fecha actual

## Tareas

1. Lee `ficha.yaml` y lista qué campos siguen a `null` o `[]` (p. ej.
   `normativa.rd_estatal`, `resultados_aprendizaje`, `unidades`).
2. Recorre cada carpeta numerada de `VCF_TSEAS/` (excluyendo los
   `README.md`) y, por carpeta, indica si tiene contenido generado o está
   vacía.
3. Si existe `calendario_26_27.md`, compáralo con la fecha actual y señala
   los hitos (unidades, evaluaciones, entregas) previstos en los próximos
   30 días.
4. Detecta incoherencias simples:
   - Unidades listadas en `ficha.yaml → unidades` sin archivo
     correspondiente en `05_UNIDADES/`.
   - Archivos con `BORRADOR` en el nombre que llevan más de 30 días sin
     modificarse (usa la fecha de última modificación del archivo).
5. Presenta un resumen con cuatro bloques: **Pendiente de revisión**,
   **Huecos de contenido**, **Próximos hitos**, **Incoherencias**.
6. Si el usuario pide guardar el resumen, escríbelo en
   `DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/estado_<YYYY-MM-DD>.md` con la
   fecha de hoy.

## Salidas

Resumen en el chat con los cuatro bloques anteriores. Opcionalmente, un
archivo en `00_CENTRO_CONTROL/`.

## Límites

No modifica ni crea ningún documento de las carpetas 01-14 salvo el propio
informe en `00_CENTRO_CONTROL/`. No aprueba ni rechaza nada, solo informa.

## Validación humana

Ninguna: es puramente informativo. El usuario decide qué hacer con lo que
reporta.
```

- [ ] **Step 2: Verificar frontmatter**

Run:
```bash
head -4 .claude/skills/vcf-estado/SKILL.md
```

Expected:
```
---
name: vcf-estado
description: Genera una foto de estado del proyecto VCF/TSEAS (rol de Coordinador / Centro de control) — qué falta en ficha.yaml, qué carpetas están vacías, próximos hitos del calendario e incoherencias detectadas. Úsalo cuando el usuario pida el estado, resumen, panel de control o "qué falta" de la asignatura VCF.
---
```

- [ ] **Step 3: Smoke test funcional**

Invoca el skill con el Skill tool (`skill: "vcf-estado"`) o escribiendo
`/vcf-estado` en el chat. Criterios de aceptación (todos deben cumplirse):

- El informe menciona explícitamente que `normativa.rd_estatal` está vacío
  (porque `/vcf-normativa` aún no se ha ejecutado).
- El informe lista las 15 carpetas de `VCF_TSEAS/` y marca todas como
  vacías salvo `00_FICHA/`.
- El informe no inventa fechas ni contenido que no exista todavía.

Si algún criterio falla, corrige el cuerpo del skill (Step 1) y repite este
paso antes de continuar.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/vcf-estado
git commit -m "Add /vcf-estado skill (coordinador / centro de control)"
```

---

### Task 5: Skill `/vcf-normativa` (Normativa y currículo)

**Files:**
- Create: `.claude/skills/vcf-normativa/SKILL.md`

**Interfaces:**
- Consumes: `ficha.yaml` (Task 2), carpeta `01_NORMATIVA_CURRICULO/` y `03_MAPA_CURRICULAR/` (Task 1). Usa la herramienta WebSearch para consultar BOE y el Diario Oficial de Extremadura (DOE).
- Produces: `01_NORMATIVA_CURRICULO/normativa_registro.md`, `03_MAPA_CURRICULAR/matriz_alineacion.md`, y actualiza en `ficha.yaml` las claves `normativa.rd_estatal`, `normativa.decreto_curriculo_autonomico`, `resultados_aprendizaje`, `criterios_evaluacion`, `contenidos`, `asignatura.horas_totales`, `asignatura.horas_semanales`. Estas claves las consumen las Tasks 7, 8 y 10.

- [ ] **Step 1: Escribir el skill**

```markdown
---
name: vcf-normativa
description: Localiza y registra la normativa oficial (RD estatal del título TSEAS y normativa autonómica de Extremadura) del módulo Valoración de la Condición Física, extrae resultados de aprendizaje/criterios/contenidos/horas, y genera la matriz de alineación curricular. Úsalo cuando el usuario pida buscar, actualizar o verificar la normativa/currículo de VCF.
---

# /vcf-normativa — Normativa y currículo (VCF/TSEAS)

## Rol

Localiza normas oficiales en BOE y en el Diario Oficial de Extremadura
(DOE), registra fuente/fecha/norma, y extrae competencias, resultados de
aprendizaje, criterios, contenidos y horas del módulo VCF dentro del
título TSEAS.

## Entradas

- `ficha.yaml` (para saber qué campos de normativa ya están rellenos)
- Título: Técnico Superior en Enseñanza y Animación Sociodeportiva (TSEAS)
- Módulo: Valoración de la Condición Física (VCF)
- Comunidad autónoma: Extremadura

## Tareas

1. Con WebSearch, busca en boe.es el Real Decreto que regula el título
   TSEAS y localiza dentro de él el módulo profesional correspondiente a
   "Valoración de la Condición Física" (comprueba el nombre oficial exacto
   del módulo, puede diferir ligeramente).
2. Extrae del RD: resultados de aprendizaje, criterios de evaluación,
   contenidos y horas mínimas del módulo.
3. Con WebSearch, busca en el Diario Oficial de Extremadura (DOE) el
   decreto autonómico que desarrolla el currículo de TSEAS en Extremadura,
   y localiza las horas/contenidos específicos de VCF si los hay.
4. Escribe `01_NORMATIVA_CURRICULO/normativa_registro.md` con, para cada
   norma encontrada: título de la norma, URL fuente, fecha de publicación,
   fecha de consulta de hoy, y artículos/anexos relevantes citados
   literalmente.
5. Actualiza `ficha.yaml`:
   - `normativa.rd_estatal`: identificador y URL del RD.
   - `normativa.decreto_curriculo_autonomico`: identificador y URL del
     decreto de Extremadura.
   - `resultados_aprendizaje`, `criterios_evaluacion`, `contenidos`: listas
     extraídas de la norma (texto literal o resumen fiel, citando el
     artículo de origen).
   - `asignatura.horas_totales`, `asignatura.horas_semanales`.
   - `estado` permanece en `borrador`.
6. Genera `03_MAPA_CURRICULAR/matriz_alineacion.md`: una tabla que cruza
   cada resultado de aprendizaje con sus criterios de evaluación y
   contenidos asociados.
7. Presenta un resumen al usuario y pide confirmación explícita antes de
   que cualquier otro comando trate estos datos como definitivos.

## Salidas

`normativa_registro.md`, `matriz_alineacion.md`, `ficha.yaml` actualizado.

## Límites

No marca `ficha.yaml.estado` como `aprobado`. Si no encuentra la norma
exacta o algún dato no puede verificarse, lo dice explícitamente ("no he
podido confirmar X, pendiente de verificación manual") en vez de inventar
artículos, fechas u horas.

## Validación humana

Obligatoria: el docente debe confirmar que el RD y el decreto localizados
son los correctos antes de que `/vcf-programacion`, `/vcf-unidad`, `/vcf-tema`
o `/vcf-examen` usen estos datos.
```

- [ ] **Step 2: Verificar frontmatter**

Run: `head -4 .claude/skills/vcf-normativa/SKILL.md`

Expected: bloque `---` / `name: vcf-normativa` / `description: ...` / `---`.

- [ ] **Step 3: Smoke test funcional**

Invoca `/vcf-normativa`. Criterios de aceptación:

- Cita al menos una URL real de boe.es como fuente del RD del título TSEAS.
- Si no logra confirmar el decreto autonómico de Extremadura con una fuente
  real, lo dice explícitamente en vez de inventar un número de decreto.
- Actualiza `ficha.yaml` dejando `estado: borrador` (no lo cambia a
  `aprobado`).
- Pide confirmación explícita al usuario al final.

Si algún criterio falla, corrige el cuerpo del skill y repite.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/vcf-normativa
git commit -m "Add /vcf-normativa skill (normativa y currículo)"
```

---

### Task 6: Skill `/vcf-auditoria` (Auditoría de contenidos existentes)

**Files:**
- Create: `.claude/skills/vcf-auditoria/SKILL.md`

**Interfaces:**
- Consumes: `3. VALORACIÓN 25_26/` (material real existente), carpetas `06_TEMARIO/{VIGENTE,REFERENCIA_HISTORICA}/` y `07_ACTIVIDADES_TAREAS/{VIGENTE,REFERENCIA_HISTORICA}/` (Task 1), `ficha.yaml` (Task 2, para contrastar contenidos vigentes).
- Produces: copias de archivos dentro de `06_TEMARIO/` y `07_ACTIVIDADES_TAREAS/`, y `14_HISTORICO_CAMBIOS/migraciones.md`.

- [ ] **Step 1: Escribir el skill**

```markdown
---
name: vcf-auditoria
description: Audita el material existente en "3. VALORACIÓN 25_26/" (programaciones, temario y tareas de 18/19 a 25/26), lo clasifica como vigente/reutilizable/obsoleto, y propone y ejecuta (tras confirmación) su copia a DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO y 07_ACTIVIDADES_TAREAS. Úsalo cuando el usuario pida auditar, ordenar, clasificar o migrar el material antiguo de VCF.
---

# /vcf-auditoria — Auditoría de contenidos (VCF/TSEAS)

## Rol

Audita el material acumulado de cursos anteriores y decide, con el usuario,
qué migra a la nueva estructura y qué queda fuera.

## Entradas

- `3. VALORACIÓN 25_26/` completa: subcarpetas `0. VALORACIÓN FORMDEPOR
  18_19` a `24_25`, `TAREAS 25_26/`, `TAEXAMENES 25_26/`, `o. programación
  26_27/`, y los archivos de temario sueltos (`TEMA 0` a `TEMA 8`).
- `ficha.yaml` (contenidos vigentes, si `/vcf-normativa` ya se ejecutó).

## Tareas

1. Lista recursivamente todos los archivos de `3. VALORACIÓN 25_26/` con su
   ruta completa.
2. Clasifica cada archivo por tipo (TEMARIO si el nombre contiene "TEMA" o
   está en una carpeta de presentaciones/temario; TAREA si el nombre
   contiene "TAREA" o está en `TAREAS_25_26`/`TAEXAMENES_25_26`; PROGRAMACIÓN
   si está en `o. programación 26_27/`; OTRO en cualquier otro caso) y por
   antigüedad (VIGENTE si es de 25/26 o del borrador 26/27;
   REFERENCIA_HISTORICA si es de 24/25 o anterior).
3. Para los archivos de TEMARIO clasificados VIGENTE, compara sus temas
   contra `ficha.yaml → contenidos` (si existe) y márcalos como
   potencialmente obsoletos si no encuentras correspondencia.
4. Presenta una tabla al usuario con columnas: `Origen | Tipo | Clasificación
   | Destino propuesto`. El destino sigue siempre uno de estos cuatro
   patrones:
   - `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/VIGENTE/`
   - `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/REFERENCIA_HISTORICA/`
   - `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS/VIGENTE/`
   - `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/`
5. No copies nada todavía. Espera confirmación explícita del usuario, que
   puede aprobar la tabla completa o pedir cambios fila por fila.
6. Tras confirmación, **copia** (nunca muevas ni borres el original) cada
   archivo confirmado a su destino, conservando el nombre original.
7. Añade una entrada a `14_HISTORICO_CAMBIOS/migraciones.md` con la fecha
   de hoy y la lista de archivos copiados (origen → destino).

## Salidas

Tabla de propuesta de migración, archivos copiados tras confirmación,
`migraciones.md` actualizado.

## Límites

Nunca borra ni mueve el material original de `3. VALORACIÓN 25_26/` — solo
copia. Nunca copia un archivo sin que el usuario lo haya confirmado
explícitamente para ese archivo o para el bloque que lo contiene.

## Validación humana

Obligatoria antes de cada copia (puede darse en bloque para varios archivos
a la vez si el usuario lo dice explícitamente, p. ej. "copia todos los de
TAREAS 25_26 como vigentes").
```

- [ ] **Step 2: Verificar frontmatter**

Run: `head -4 .claude/skills/vcf-auditoria/SKILL.md`

Expected: bloque `---` / `name: vcf-auditoria` / `description: ...` / `---`.

- [ ] **Step 3: Smoke test funcional**

Invoca `/vcf-auditoria`. Criterios de aceptación:

- Produce la tabla `Origen | Tipo | Clasificación | Destino propuesto`
  cubriendo al menos los archivos de `TAREAS 25_26/` y de
  `0. VALORACIÓN FORMDEPOR 24_25/TAREAS 24_25/`.
- No copia ningún archivo antes de pedir confirmación.
- Tras confirmar solo un archivo de prueba (p. ej. una tarea de 24/25),
  comprueba que aparece copiado (no movido) en
  `06_TEMARIO/REFERENCIA_HISTORICA/` o `07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/`
  según corresponda, y que el original sigue existiendo en
  `3. VALORACIÓN 25_26/`.
- `migraciones.md` registra esa copia con fecha de hoy.

Verifica con:
```bash
ls "3. VALORACIÓN 25_26/0. VALORACIÓN FORMDEPOR 24_25/TAREAS 24_25/" | head -1
find "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA" -type f
cat "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/14_HISTORICO_CAMBIOS/migraciones.md"
```

Si algún criterio falla, corrige el cuerpo del skill y repite.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/vcf-auditoria DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/07_ACTIVIDADES_TAREAS DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/14_HISTORICO_CAMBIOS
git commit -m "Add /vcf-auditoria skill and smoke-test migration output"
```

---

### Task 7: Skill `/vcf-programacion` (Planificación y temporalización)

**Files:**
- Create: `.claude/skills/vcf-programacion/SKILL.md`

**Interfaces:**
- Consumes: `ficha.yaml` (claves `resultados_aprendizaje`, `criterios_evaluacion`, `contenidos`, `asignatura.horas_totales`, `asignatura.horas_semanales` — producidas por Task 5), `3. VALORACIÓN 25_26/o. programación 26_27/1.Modulo Profesional Valoracion de la CF_Mario_Curso 2026-2027.md` (borrador existente, nombre real del archivo sin tildes) o el `.docx` homólogo con tildes en la misma carpeta, carpetas `02_PROGRAMACION/` y `04_TEMPORALIZACION/` (Task 1). Usa WebSearch para el calendario escolar de Extremadura 26/27.
- Produces: `02_PROGRAMACION/programacion_26_27.md`, `04_TEMPORALIZACION/calendario_26_27.md`, y actualiza en `ficha.yaml` la clave `unidades` (lista de `{nombre, fechas}`).

- [ ] **Step 1: Escribir el skill**

```markdown
---
name: vcf-programacion
description: Cierra la programación didáctica 26/27 de VCF a partir del borrador existente y de ficha.yaml, y genera el calendario de temporalización (unidades, evaluaciones, entregas, recuperación) descontando festivos y no lectivos de Extremadura. Úsalo cuando el usuario pida programación, temporalización o calendario del curso 26/27.
---

# /vcf-programacion — Planificación y temporalización (VCF/TSEAS)

## Rol

Genera los planes anual/trimestral y el calendario de unidades y
evaluaciones del curso 2026-2027, descontando festivos, vacaciones y días
no lectivos de Extremadura.

## Entradas

- `ficha.yaml`: `resultados_aprendizaje`, `criterios_evaluacion`,
  `contenidos`, `asignatura.horas_totales`, `asignatura.horas_semanales`.
  Si estos campos están vacíos, avisa al usuario de que conviene ejecutar
  `/vcf-normativa` antes, pero puedes continuar con lo que el usuario te
  dé directamente si insiste.
- `3. VALORACIÓN 25_26/o. programación 26_27/1.Modulo Profesional
  Valoracion de la CF_Mario_Curso 2026-2027.md` (borrador ya existente,
  nombre real del archivo sin tildes; hay también un `.docx` homólogo con
  tildes en la misma carpeta).
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
7. Actualiza `ficha.yaml → unidades` con la lista de unidades y sus
   fechas de inicio/fin previstas. `estado` permanece en `borrador`.

## Salidas

`programacion_26_27.md`, `calendario_26_27.md`, `ficha.yaml` actualizado.

## Límites

No inventa fechas de festivos sin fuente verificada — si no puede
confirmarlas, las marca como "pendiente de verificar por el docente" en
vez de asumir un calendario genérico. No fija ponderaciones de
calificación sin que el docente las confirme.

## Validación humana

El docente debe aprobar la programación y el calendario (pasar
`estado` a `aprobado` explícitamente) antes de subirlos a Drive/Calendar.
```

- [ ] **Step 2: Verificar frontmatter**

Run: `head -4 .claude/skills/vcf-programacion/SKILL.md`

Expected: bloque `---` / `name: vcf-programacion` / `description: ...` / `---`.

- [ ] **Step 3: Smoke test funcional**

Invoca `/vcf-programacion`. Criterios de aceptación:

- Lee y referencia contenido real del borrador
  `1.Modulo Profesional Valoracion de la CF_Mario_Curso 2026-2027.md`.
- Si no puede confirmar el calendario escolar oficial de Extremadura con
  una fuente real, lo dice explícitamente en el documento generado en vez
  de inventar fechas de festivos.
- Genera `programacion_26_27.md` y `calendario_26_27.md`.
- `ficha.yaml → estado` sigue en `borrador` tras la ejecución.

Verifica con:
```bash
ls "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/02_PROGRAMACION/"
ls "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/04_TEMPORALIZACION/"
grep "^estado:" "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml"
```

Si algún criterio falla, corrige el cuerpo del skill y repite.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/vcf-programacion DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/02_PROGRAMACION DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/04_TEMPORALIZACION DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml
git commit -m "Add /vcf-programacion skill and smoke-test 26/27 programación"
```

---

### Task 8: Skill `/vcf-unidad` (Diseño de unidades)

**Files:**
- Create: `.claude/skills/vcf-unidad/SKILL.md`

**Interfaces:**
- Consumes: `ficha.yaml` (`resultados_aprendizaje`, `criterios_evaluacion`, `contenidos`, `unidades`, `calendario_ref` — producidas por Tasks 5 y 7), `06_TEMARIO/REFERENCIA_HISTORICA/` (Task 6, opcional como inspiración), carpeta `05_UNIDADES/` (Task 1).
- Produces: archivos `05_UNIDADES/VCF_UNIDAD_UD<NN>_2026-2027_V01_BORRADOR.md`, y actualiza `ficha.yaml → unidades[i]` añadiendo la referencia al archivo generado.

- [ ] **Step 1: Escribir el skill**

```markdown
---
name: vcf-unidad
description: Genera o actualiza una unidad didáctica completa de VCF (justificación, objetivos, RA, criterios, contenidos, metodología, actividades, recursos, diversidad, evaluación, recuperación, ampliación) y la guarda en 05_UNIDADES con la nomenclatura oficial. Úsalo cuando el usuario pida crear, redactar o revisar una unidad didáctica de VCF.
---

# /vcf-unidad — Diseño de unidades didácticas (VCF/TSEAS)

## Rol

Genera unidades didácticas completas de VCF, vinculadas a los resultados
de aprendizaje y criterios de evaluación registrados en `ficha.yaml`.

## Entradas

- `ficha.yaml`: `resultados_aprendizaje`, `criterios_evaluacion`,
  `contenidos`, `unidades`, `calendario_ref`.
- Número o nombre de unidad que pida el usuario (si no lo da, pregúntalo).
- `06_TEMARIO/REFERENCIA_HISTORICA/` como posible fuente de inspiración
  para actividades y enfoque, si ya contiene material relevante.

## Tareas

1. Si el usuario no especifica qué unidad, pregúntale número/nombre y qué
   contenidos/RA de `ficha.yaml` debe cubrir.
2. Redacta la unidad con estas secciones obligatorias:
   - Justificación (por qué esta unidad, relación con el resto del curso)
   - Duración en sesiones (usa `04_TEMPORALIZACION/calendario_26_27.md`
     si existe para ajustar el número real de sesiones disponibles)
   - Objetivos
   - Resultados de aprendizaje y criterios de evaluación vinculados
     (copiados literalmente de `ficha.yaml`, citando cuáles aplican)
   - Contenidos
   - Metodología (elige según el tipo de contenido: motriz, teórico,
     práctico — justifica la elección en una frase)
   - Actividades: inicio/motivación, desarrollo, prácticas
   - Recursos necesarios
   - Atención a la diversidad: medidas genéricas (DUA, agrupamientos
     flexibles, materiales alternativos, graduación de dificultad) — nunca
     menciones alumnos concretos ni diagnósticos
   - Evaluación e instrumentos, con evidencias esperadas
   - Actividades de recuperación y de ampliación
3. Guarda el resultado en
   `05_UNIDADES/VCF_UNIDAD_UD<NN>_2026-2027_V01_BORRADOR.md`, donde `<NN>`
   es el número de unidad con dos dígitos (p. ej. `UD03`).
4. Actualiza `ficha.yaml → unidades`: si la unidad ya existía en la lista,
   añade/actualiza el campo `archivo` con la ruta generada; si no existía,
   añade una entrada nueva `{nombre, archivo}`.

## Salidas

Archivo de unidad en `05_UNIDADES/`, `ficha.yaml` actualizado.

## Límites

La sección de diversidad usa exclusivamente medidas genéricas aplicables a
cualquier grupo — nunca datos personales ni diagnósticos de alumnado
concreto. El archivo se guarda siempre en estado `BORRADOR`.

## Validación humana

La unidad queda en `BORRADOR` hasta que el docente la revise. Si el
docente confirma que está lista, renombra el archivo cambiando
`V01_BORRADOR` por `V01_APROBADO` (o la versión que corresponda) y haz un
commit específico para esa aprobación.
```

- [ ] **Step 2: Verificar frontmatter**

Run: `head -4 .claude/skills/vcf-unidad/SKILL.md`

Expected: bloque `---` / `name: vcf-unidad` / `description: ...` / `---`.

- [ ] **Step 3: Smoke test funcional**

Invoca `/vcf-unidad` pidiendo una unidad de prueba (p. ej. "genera la
unidad sobre el sistema cardiorrespiratorio, UD03"). Criterios de
aceptación:

- El archivo generado en `05_UNIDADES/` sigue exactamente el patrón
  `VCF_UNIDAD_UD03_2026-2027_V01_BORRADOR.md`.
- Contiene las 10 secciones obligatorias listadas en el Step 1 (verificar
  que ninguna falte).
- La sección de diversidad no menciona ningún alumno concreto ni
  diagnóstico.
- `ficha.yaml → unidades` incluye una entrada para esta unidad con el
  campo `archivo` apuntando al archivo generado.

Verifica con:
```bash
ls "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/05_UNIDADES/"
grep -E "^## (Justificación|Objetivos|Metodología|Evaluación)" \
  "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/05_UNIDADES/"*.md
```

Si algún criterio falla, corrige el cuerpo del skill y repite.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/vcf-unidad DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/05_UNIDADES DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml
git commit -m "Add /vcf-unidad skill and smoke-test unidad borrador"
```

---

### Task 9: Skill `/vcf-tema` (Contenidos y temario)

**Files:**
- Create: `.claude/skills/vcf-tema/SKILL.md`

**Interfaces:**
- Consumes: `06_TEMARIO/REFERENCIA_HISTORICA/` (Task 6), `ficha.yaml → contenidos` (Task 5), carpeta `06_TEMARIO/VIGENTE/` (Task 1).
- Produces: archivos `06_TEMARIO/VIGENTE/VCF_TEMA_UD<NN>_2026-2027_V01_BORRADOR_<TIPO>.md` (TIPO ∈ {DOCENTE, ALUMNADO, RESUMEN, ESQUEMA, GLOSARIO, REPASO}).

- [ ] **Step 1: Escribir el skill**

```markdown
---
name: vcf-tema
description: Genera el temario vigente de un tema de VCF (versión docente, apuntes de alumnado, resumen, esquema, glosario, preguntas de repaso) apoyándose en el material histórico ya migrado a REFERENCIA_HISTORICA. Úsalo cuando el usuario pida generar, actualizar o auditar un tema/temario de VCF.
---

# /vcf-tema — Contenidos y temario (VCF/TSEAS)

## Rol

Audita el temario histórico disponible y genera la versión vigente de un
tema en varios formatos derivados.

## Entradas

- Tema pedido por el usuario (nombre o número de unidad).
- `06_TEMARIO/REFERENCIA_HISTORICA/` — temas de cursos anteriores ya
  migrados por `/vcf-auditoria` (PDF/DOCX).
- `ficha.yaml → contenidos` — contenidos vigentes según la normativa
  registrada por `/vcf-normativa`.

## Tareas

1. Busca en `06_TEMARIO/REFERENCIA_HISTORICA/` archivos relacionados con
   el tema pedido. Si no encuentras nada, dilo explícitamente y genera el
   tema desde cero a partir de `ficha.yaml → contenidos`.
2. Si encuentras material histórico, extrae su texto (de PDF/DOCX) y
   contrástalo contra `ficha.yaml → contenidos`: qué sigue vigente, qué
   falta añadir, qué ya no corresponde al currículo actual.
3. Genera, como archivos Markdown separados en `06_TEMARIO/VIGENTE/`:
   - `..._DOCENTE.md`: versión completa para el profesor.
   - `..._ALUMNADO.md`: apuntes para el alumnado.
   - `..._RESUMEN.md`: resumen breve.
   - `..._ESQUEMA.md`: esquema/mapa conceptual en texto.
   - `..._GLOSARIO.md`: glosario de términos clave.
   - `..._REPASO.md`: preguntas de repaso (sin soluciones — las soluciones
     son responsabilidad de `/vcf-examen`, no de este comando).
   Nomenclatura: `VCF_TEMA_UD<NN>_2026-2027_V01_BORRADOR_<TIPO>.md`.

## Salidas

Seis archivos Markdown en `06_TEMARIO/VIGENTE/` por tema procesado.

## Límites

No modifica ni elimina nada en `REFERENCIA_HISTORICA/` — solo lee de ahí.
Si el tema pedido no tiene referencia histórica, lo dice explícitamente en
vez de simular que sí la tiene.

## Validación humana

Los seis archivos quedan en `BORRADOR`. El docente los revisa y, si los
aprueba, pide explícitamente el cambio a `APROBADO` en el nombre de
archivo.
```

- [ ] **Step 2: Verificar frontmatter**

Run: `head -4 .claude/skills/vcf-tema/SKILL.md`

Expected: bloque `---` / `name: vcf-tema` / `description: ...` / `---`.

- [ ] **Step 3: Smoke test funcional**

Invoca `/vcf-tema` para un tema con referencia histórica conocida (p. ej.
"genera el tema del sistema cardiorrespiratorio, UD03", que tiene
`TEMA 3 VCF TSEAS 25_26 SIST CARDIORESPI` como referencia si ya fue migrado
por `/vcf-auditoria` en la Task 6; si no se migró aún, pide primero migrar
ese archivo). Criterios de aceptación:

- Genera los 6 archivos con la nomenclatura exacta
  `VCF_TEMA_UD03_2026-2027_V01_BORRADOR_<TIPO>.md`.
- El archivo `..._REPASO.md` no contiene las respuestas.
- Si usó material de `REFERENCIA_HISTORICA/`, lo menciona explícitamente
  (qué archivo origen usó).

Verifica con:
```bash
ls "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/VIGENTE/"
```

Si algún criterio falla, corrige el cuerpo del skill y repite.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/vcf-tema DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/06_TEMARIO/VIGENTE
git commit -m "Add /vcf-tema skill and smoke-test tema borrador set"
```

---

### Task 10: Skill `/vcf-examen` (Evaluación)

**Files:**
- Create: `.claude/skills/vcf-examen/SKILL.md`

**Interfaces:**
- Consumes: `ficha.yaml` (`resultados_aprendizaje`, `criterios_evaluacion` — Task 5), `07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/` y `08_EVALUACION/` como banco de referencia (Task 6), carpeta `08_EVALUACION/` (Task 1).
- Produces: archivos `08_EVALUACION/VCF_EXAMEN_UD<NN>_2026-2027_V01_BORRADOR.md` y `08_EVALUACION/VCF_EXAMEN_UD<NN>_2026-2027_V01_BORRADOR_SOLUCIONARIO.md`.

- [ ] **Step 1: Escribir el skill**

```markdown
---
name: vcf-examen
description: Genera instrumentos de evaluación de VCF (exámenes, rúbricas, banco de preguntas) vinculados a resultados de aprendizaje y criterios de evaluación, con su solucionario en archivo separado. Úsalo cuando el usuario pida un examen, rúbrica, banco de preguntas o solucionario de VCF.
---

# /vcf-examen — Evaluación (VCF/TSEAS)

## Rol

Genera pruebas de evaluación y sus solucionarios, controlando cobertura de
RA/criterios y dificultad.

## Entradas

- Unidad o bloque de contenidos a evaluar (pedirlo si no se especifica).
- `ficha.yaml`: `resultados_aprendizaje`, `criterios_evaluacion`.
- `07_ACTIVIDADES_TAREAS/REFERENCIA_HISTORICA/` y `08_EVALUACION/` como
  banco de referencia de exámenes/preguntas anteriores.

## Tareas

1. Si no se especifica, pregunta qué tipo de instrumento quiere el usuario:
   examen tipo test, de desarrollo, práctico, rúbrica, o banco de
   preguntas.
2. Identifica en `ficha.yaml` los RA y criterios del bloque a evaluar.
3. Redacta cada pregunta/ítem vinculado explícitamente a un RA y un
   criterio concreto (indícalo entre paréntesis junto a la pregunta).
   Verifica cobertura: todos los RA del bloque deben estar representados
   por al menos una pregunta.
4. Varía la dificultad (al menos un tercio de nivel básico, un tercio
   intermedio, un tercio de aplicación/análisis).
5. Si es examen: genera también una segunda versión alternativa (mismas
   preguntas reordenadas o con variantes equivalentes) pensada para
   recuperación.
6. Si es rúbrica: genera una escala de niveles de desempeño (p. ej.
   Insuficiente/Suficiente/Notable/Excelente) por cada criterio.
7. Guarda el instrumento visible en
   `08_EVALUACION/VCF_EXAMEN_UD<NN>_2026-2027_V01_BORRADOR.md` y el
   solucionario en un archivo **separado**:
   `08_EVALUACION/VCF_EXAMEN_UD<NN>_2026-2027_V01_BORRADOR_SOLUCIONARIO.md`.

## Salidas

Instrumento(s) + solucionario en `08_EVALUACION/`.

## Límites

El solucionario nunca va en el mismo archivo que el examen visible para el
alumnado. Este comando no pondera notas ni decide calificaciones — eso es
exclusivamente manual del docente.

## Validación humana

Aprobación docente obligatoria (cambio explícito de `BORRADOR` a
`APROBADO` en el nombre de archivo) antes de aplicar el examen al
alumnado.
```

- [ ] **Step 2: Verificar frontmatter**

Run: `head -4 .claude/skills/vcf-examen/SKILL.md`

Expected: bloque `---` / `name: vcf-examen` / `description: ...` / `---`.

- [ ] **Step 3: Smoke test funcional**

Invoca `/vcf-examen` pidiendo un examen de prueba para una unidad con RA
ya definidos en `ficha.yaml` (p. ej. la unidad generada en la Task 8).
Criterios de aceptación:

- Genera dos archivos: el examen y el solucionario, en archivos separados
  con la nomenclatura exacta indicada.
- Cada pregunta cita el RA/criterio que evalúa.
- Todos los RA del bloque están cubiertos por al menos una pregunta.
- El archivo del examen (no el solucionario) no contiene las respuestas.

Verifica con:
```bash
ls "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/08_EVALUACION/"
grep -L "SOLUCIONARIO" "DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/08_EVALUACION/"*BORRADOR.md
```

Si algún criterio falla, corrige el cuerpo del skill y repite.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/vcf-examen DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/08_EVALUACION
git commit -m "Add /vcf-examen skill and smoke-test exam + solucionario"
```

---

## Post-plan (no forma parte de este plan)

Una vez completadas las 10 tareas, el piloto queda operativo end-to-end:
carpetas, modelo de datos, contexto y los 7 comandos. Uso real y continuado
(auditar todo el material histórico, cerrar la programación 26/27 completa,
generar todas las unidades del curso) es trabajo de *uso* del sistema, no
de construcción — se hace invocando los comandos ya construidos, sesión a
sesión, según lo vaya necesitando el usuario. La vigilancia normativa
automática, la integración activa con Drive/Calendar, la analítica y la
extensión a otras asignaturas quedan para planes futuros, tal como fija el
spec en "Fuera de alcance".
