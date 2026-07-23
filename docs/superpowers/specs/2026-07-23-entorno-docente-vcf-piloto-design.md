# Entorno docente vivo — Piloto VCF/TSEAS

Fecha: 2026-07-23
Estado: Aprobado por el usuario, pendiente de implementación

## Contexto y alcance

El documento `entorno_preparacion_clases_compacto.md` describe un departamento
docente digital completo: 3 niveles de arquitectura, 11 agentes especializados,
16 secciones por asignatura y 4 fases de implantación. Es demasiado grande para
diseñarse e implementarse de una vez, así que este spec cubre únicamente la
**Fase 0 (diseño base) + Fase 1 (piloto)** del documento original, aplicadas a
una sola asignatura real:

- **Centro:** Formdepor
- **Ciclo:** Técnico Superior en Enseñanza y Animación Sociodeportiva (TSEAS)
- **Módulo piloto:** Valoración de la Condición Física (VCF)
- **Comunidad autónoma:** Extremadura (normativa autonómica)
- **Curso objetivo:** 2026-2027

El resto de asignaturas, la analítica de resultados y la vigilancia normativa
automática quedan explícitamente fuera de este piloto (ver "Fuera de alcance").

Material existente de partida: `3. VALORACIÓN 25_26/`, con programaciones desde
18/19, temario, tareas y exámenes de varios cursos, y un borrador de
programación 26/27 en `o. programación 26_27/`.

## Decisiones de diseño (resumen de la conversación de brainstorming)

1. **Punto de partida:** piloto de una sola asignatura (VCF/TSEAS), no toda la
   arquitectura multi-asignatura de golpe.
2. **Almacenamiento:** local-first en esta carpeta, con integración asistida
   (bajo demanda, no automática en segundo plano) con Google Drive y Google
   Calendar.
3. **Prioridades del piloto:** auditoría y orden del material existente,
   programación y temporalización 26/27, generación de unidades y temario,
   evaluación (exámenes, rúbricas, banco de preguntas).
4. **Marco normativo:** RD estatal del título TSEAS + normativa autonómica de
   Extremadura para el módulo VCF.
5. **Estilo de interacción:** comandos explícitos (`/vcf-...`) respaldados por
   un `CLAUDE.md` común que da contexto y reglas a cualquier interacción, con
   o sin comando.
6. **Referencia histórica:** el temario y las tareas de cursos anteriores
   (18/19 → 25/26) se conservan accesibles como banco de referencia, no se
   descartan.

## Arquitectura

### Estructura de carpetas

```text
DEPARTAMENTO_DOCENTE/
├── 00_CENTRO_CONTROL/              # panel simplificado (estado, alertas, pendientes)
├── CLAUDE.md                       # cerebro común: contexto + reglas del sistema
└── ASIGNATURAS/
    └── VCF_TSEAS/
        ├── 00_FICHA/                # ficha.yaml (modelo de datos)
        ├── 01_NORMATIVA_CURRICULO/  # RD estatal + normativa Extremadura + matriz curricular
        ├── 02_PROGRAMACION/         # programación 26/27
        ├── 03_MAPA_CURRICULAR/
        ├── 04_TEMPORALIZACION/      # calendario de unidades/evaluaciones 26/27
        ├── 05_UNIDADES/
        ├── 06_TEMARIO/
        │   ├── VIGENTE/                  # temario actual (25/26 → 26/27)
        │   └── REFERENCIA_HISTORICA/     # temas de cursos anteriores (18_19 … 24_25), por año
        ├── 07_ACTIVIDADES_TAREAS/
        │   ├── VIGENTE/
        │   └── REFERENCIA_HISTORICA/     # tareas de cursos anteriores, por año
        ├── 08_EVALUACION/           # exámenes, rúbricas, banco de preguntas, solucionarios
        ├── 09_RECURSOS_DIGITALES/
        ├── 10_DIVERSIDAD/
        ├── 11_SEGUIMIENTO_RESULTADOS/
        ├── 12_RECUPERACION/
        ├── 13_MEMORIA_FINAL/
        └── 14_HISTORICO_CAMBIOS/
```

El material actual de `3. VALORACIÓN 25_26/` no se mueve ni se borra
automáticamente. El comando `/vcf-auditoria` es el único que decide, archivo a
archivo, si algo migra a `VIGENTE`, a `REFERENCIA_HISTORICA`, o se queda fuera
por obsoleto.

### Modelo de datos: `00_FICHA/ficha.yaml`

Archivo estructurado único que todos los comandos leen y actualizan:

```yaml
asignatura:
  nombre: Valoración de la Condición Física
  codigo: VCF
  ciclo: Técnico Superior en Enseñanza y Animación Sociodeportiva (TSEAS)
  centro: Formdepor
  comunidad_autonoma: Extremadura
  curso_academico: 2026-2027
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

Ningún comando inventa resultados de aprendizaje, criterios o normativa: todo
sale de una fuente oficial (BOE/DOE) registrada, o de lo que el usuario
apruebe explícitamente.

### Comandos (agentes del piloto)

| Comando | Agente del documento original | Qué hace |
|---|---|---|
| `/vcf-normativa` | Normativa y currículo | Busca el RD estatal del título TSEAS y la normativa autonómica de Extremadura para VCF, registra fuente/fecha/norma, extrae RA/criterios/contenidos/horas, genera la matriz de alineación curricular |
| `/vcf-auditoria` | Contenidos (auditoría) | Recorre `3. VALORACIÓN 25_26/`, clasifica cada archivo (vigente / reutilizable / obsoleto), propone migración a la nueva estructura |
| `/vcf-programacion` | Planificación y temporalización | Cierra la programación 26/27 y genera el calendario de unidades/evaluaciones, descontando festivos y no lectivos de Extremadura |
| `/vcf-unidad` | Diseño de unidades | Genera/actualiza una unidad didáctica completa (objetivos, RA, criterios, contenidos, metodología, actividades, recursos, diversidad, evaluación, recuperación) |
| `/vcf-tema` | Contenidos y temario | Genera versión docente, apuntes, resumen, esquema, glosario y preguntas de repaso de un tema, usando `REFERENCIA_HISTORICA` como fuente de apoyo |
| `/vcf-examen` | Evaluación | Genera exámenes, rúbricas, banco de preguntas, solucionarios y versiones alternativas, vinculados a RA/criterios |
| `/vcf-estado` | Coordinador / Centro de control | Da una foto del proyecto: qué falta, qué está pendiente de revisión, próximas fechas, incoherencias detectadas |

Todo comando termina en `estado: borrador`. Nada pasa a `aprobado` sin
confirmación explícita del usuario (regla del documento original: normativa,
calificaciones y documentos oficiales nunca se modifican sin revisión).

### Integraciones (asistidas, no automáticas)

No hay n8n conectado ni tareas en segundo plano. Bajo petición explícita del
usuario:

- Subir a Google Drive los documentos aprobados (Docs/Sheets) para acceso
  desde el móvil.
- Crear/actualizar eventos en Google Calendar a partir de
  `04_TEMPORALIZACION/calendario_26_27.md`.

### Formatos

Contenido nuevo generado en Markdown (versionable, editable). Los `.docx`/PDF
existentes se usan como fuente de lectura; los `.key` (Keynote) no se pueden
leer ni editar directamente y quedan solo como referencia de archivo.

### Versionado

Repositorio git en la raíz del proyecto. Cada aprobación de documento
(`estado: aprobado`) se corresponde con un commit, dando histórico real con
diffs. La nomenclatura de archivo del documento original se mantiene:

`ASIGNATURA_TIPO_UD_CURSO_VERSION_ESTADO.ext`

Ejemplo: `VCF_TEMA_UD03_2026-2027_V02_APROBADO.md`

## Fuera de alcance (fases posteriores)

- Otras asignaturas del centro (Fase 4 — escalado).
- Analítica de resultados/calificaciones (Fase 3 — no hay datos de
  calificaciones todavía).
- Agente de Atención a la diversidad como comando independiente — por ahora
  vive como sección dentro de `/vcf-unidad` (medidas DUA genéricas, sin
  inventar diagnósticos ni datos personales).
- Generación de recursos digitales (presentaciones vía Gamma, formularios,
  gamificación) — extensión posible una vez el temario y las unidades estén
  asentados.
- Vigilancia normativa automática y recordatorios programados (Fase 2 —
  requeriría n8n u otro mecanismo de tareas programadas).

## Siguiente paso

Invocar la skill `writing-plans` para convertir este diseño en un plan de
implementación paso a paso.
