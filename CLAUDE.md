# Entorno docente — Formdepor

Este repositorio es el entorno docente vivo del departamento de **Formdepor**,
comunidad autónoma **Extremadura**, curso **2026-2027**. Cubre varios ciclos
formativos, no uno solo — hoy **Técnico Superior en Enseñanza y Animación
Sociodeportiva (TSEAS)** y **Técnico en Guía en el Medio Natural y de Tiempo
Libre (GUIA)**, y crecerá con más según se vayan incorporando asignaturas.
Cada asignatura vive en su propia carpeta bajo
`DEPARTAMENTO_DOCENTE/ASIGNATURAS/<CODIGO>_<CICLO>/` (hoy: `VCF_TSEAS`,
`MET_TSEAS` y `NAT_GUIA`) y comparte la misma capa de comandos `/asig-*`
descrita más abajo — el ciclo concreto de cada una vive en su propio
`ficha.yaml → asignatura.ciclo`, nunca hay que asumir que todas
comparten el mismo.

Es el piloto (Fase 0 + Fase 1) de una arquitectura departamental más amplia
descrita en `entorno_preparacion_clases_compacto.md`. Ver
`docs/superpowers/specs/2026-07-23-entorno-docente-vcf-piloto-design.md`
para el diseño completo.

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
  - **VCF** — Valoración de la Condición Física, ciclo TSEAS (`VCF_TSEAS/`).
  - **MET** — Metodología de la Enseñanza de Actividades Físico-Deportivas,
    ciclo TSEAS (`MET_TSEAS/`).
  - **NAT** — Técnicas de Natación, ciclo GUIA (Técnico en Guía en el Medio
    Natural y de Tiempo Libre) (`NAT_GUIA/`).
- `3. VALORACIÓN 25_26/`, `3. METODOLOGÍA 25_26/` y `Tecnicas de natación/`
  — material histórico original de cada asignatura (el nombre exacto de
  cada carpeta no sigue un patrón fijo, es simplemente como llegó del
  docente). **Nunca se mueve ni se borra directamente**; solo
  `/asig-auditoria` puede copiar de aquí a `DEPARTAMENTO_DOCENTE/`, y solo
  tras confirmación explícita del usuario. Esas copias hacen crecer el
  repositorio de git con el tiempo, porque los binarios no son diffables,
  así que conviene hacer las migraciones grandes de forma deliberada y no
  todas de golpe.

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

## Reglas fijas (aplican siempre, con o sin comando explícito)

1. Normativa, calificaciones, ponderaciones y documentos oficiales **nunca**
   se modifican sin revisión y autorización explícita del docente.
2. Todo documento generado queda en `estado: borrador` / `BORRADOR` en el
   nombre de archivo. Nada pasa a `aprobado`/`APROBADO` sin que el usuario
   lo confirme explícitamente.
3. Nunca se inventan datos personales ni diagnósticos de alumnado —
   especialmente en las secciones de atención a la diversidad genéricas
   de cada unidad. **Dos excepciones únicas y deliberadas:**
   `/asig-diversidad` maneja datos reales (no inventados) de alumnado con
   necesidades especiales, aportados legítimamente por el docente en
   `10_DIVERSIDAD/INFORMES_ALUMNADO/`; `/asig-analitica` maneja
   calificaciones reales en `11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/`.
   Esas tres carpetas (`INFORMES_ALUMNADO/`, `PLANES_ADAPTACION/`,
   `CALIFICACIONES/`) contienen datos personales de alumnado real y
   **nunca salen de este disco local**: excluidas de git (`.gitignore`),
   de `/asig-drive`, de `/asig-calendar-sync`, de `/asig-revision` y del
   detalle de `/asig-estado`, sin excepción, aunque se pida explícitamente
   "todo". Los informes *agregados* que produce `/asig-analitica` en
   `11_SEGUIMIENTO_RESULTADOS/INFORMES/` sí son documentos normales
   (anónimos por diseño: nunca identifican a un alumno o alumna
   concretos).
4. Contenido nuevo se escribe en Markdown. Nomenclatura de archivo:
   `ASIGNATURA_TIPO_UD_CURSO_VERSION_ESTADO.ext`
   (ejemplo: `VCF_UNIDAD_UD03_2026-2027_V01_BORRADOR.md`).

   El `<NN>` de `UD<NN>` es la posición (empezando en 0) de la unidad entre
   las unidades docentes reales de `ficha.yaml → unidades`, excluyendo los
   bloques de evaluación o recuperación puros, que no reciben su propio
   archivo UD numerado. Para subunidades que resultan de dividir una
   unidad (p. ej. UT3a, UT3b, UT3c), se añade una letra minúscula al mismo
   número de dos dígitos en vez de incrementarlo. Así, si `ficha.yaml →
   unidades` contiene UT0, UT1, UT2, UT3a, UT3b, UT3c y UT4, la
   correspondencia es UD00, UD01, UD02, UD03a, UD03b, UD03c y UD04.
5. Las integraciones con Google Drive/Calendar (`/asig-drive`,
   `/asig-calendar-sync`) se hacen solo cuando el usuario las pide
   explícitamente en ese momento — nunca en segundo plano. Única
   excepción explícita: `/asig-vigilancia` sí corre en segundo plano de
   forma programada (trimestral, ver `.claude/skills/asig-vigilancia/`),
   pero solo lee/compara normativa — nunca escribe en `ficha.yaml` ni en
   documentos aprobados sin confirmación explícita posterior del docente.
6. Cada vez que el usuario aprueba un documento, o confirma una migración o
   copia de archivos (p. ej. en `/asig-auditoria`), se hace un commit de git
   con un mensaje que identifique el documento o la operación.
7. Si una norma, fecha o dato no se puede verificar con una fuente real, se
   dice explícitamente en vez de inventarlo.
8. `/asig-mantenimiento` puede disparar otras skills de generación de
   contenido (`/asig-unidad`, `/asig-tema`, `/asig-tarea`, `/asig-examen`,
   `/asig-programacion`) automáticamente para corregir desactualizaciones,
   pero el resultado siempre queda en `BORRADOR` (regla 2) y nunca
   dispara `/asig-auditoria` ni `/asig-normativa` por su cuenta. Ninguna
   skill edita el `SKILL.md` de otra (ni el suyo propio) de forma
   autónoma — como mucho, propone un cambio en
   `00_CENTRO_CONTROL/propuestas_mejora_skills/` para que el docente lo
   revise y decida.
