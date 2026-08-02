# Rutinas de información: informe diario y planificación semanal

Fecha: 2026-08-02
Estado: Aprobado por el usuario, pendiente de implementación

## Contexto y alcance

Este spec retoma el bloque **C (rutinas de información)** que quedó
explícitamente fuera de alcance de
`docs/superpowers/specs/2026-07-31-centro-control-registro-documentos-design.md`.
La propuesta externa original ("arquitectura automatizada.pdf") describía
cinco rutinas: informe diario, resumen semanal, planificación semanal,
revisión mensual y cierre trimestral.

De esas cinco:

- **Resumen semanal** ya existe (modo de `/asig-estado`, disparado los
  viernes por un recordatorio de Calendar) — no es parte de este spec.
- **Revisión mensual** y **cierre trimestral** necesitan datos de
  calificaciones reales ("rendimiento del grupo", "resultados",
  "alumnado en riesgo") que hoy no existen cargados en el proyecto
  (`/asig-analitica` está definida pero, según `CLAUDE.md`, "no es
  ejecutable todavía para ninguna asignatura: no hay calificaciones
  reales cargadas"). Quedan fuera de este spec; se diseñarán junto a
  `/asig-analitica` cuando haya calificaciones reales.
- **Informe diario** y **planificación semanal** son las dos rutinas
  nuevas que cubre este spec.

Ambas se diseñan como dos modos adicionales de `/asig-estado` (que
pasaría a tener cinco: informe completo, resumen semanal, registro,
informe diario, planificación semanal), no como una skill nueva —mismo
razonamiento que ya se aplicó al modo registro: es contenido puramente
informativo que reutiliza la misma lectura de `ficha.yaml`/calendario que
la skill ya tiene.

## Decisiones de diseño (resumen de la conversación de brainstorming)

1. **Ninguna de las dos rutinas se ejecuta de forma autónoma.** El patrón
   "automático a las 07:15 todos los días" de la propuesta original no es
   viable en esta plataforma (no hay cron durable indefinido). Ambas
   siguen el mismo patrón ya validado en el proyecto: un recordatorio
   recurrente de Google Calendar que el propio docente dispara abriendo
   Claude Code. Si nadie abre Claude Code ese día/domingo, simplemente no
   se genera nada.
2. **Informe diario solo suena en días con clase.** El recordatorio de
   Calendar se limita a los días de la semana en que al menos una
   asignatura (VCF o MET) tiene clase, calculado como la unión de
   `ficha.yaml → asignatura.horario_semanal` de ambas — evita un aviso
   vacío los días sin ninguna clase.
3. **Planificación semanal es una rutina separada del resumen semanal**,
   aunque su contenido se parece: el resumen semanal (viernes) es un
   panel de *estado* ("qué ha pasado, qué falta"); la planificación
   semanal (domingo) es un *checklist de preparación* para la semana que
   empieza el lunes. El docente prefiere mantener ambos touchpoints
   separados en vez de fusionarlos en uno solo.
4. **Ambas reutilizan cálculos ya existentes, no recorren el repositorio
   por su cuenta desde cero:**
   - El semáforo y las alertas del informe diario reutilizan
     directamente el **Panel general** y la tabla **Documentos** del
     modo registro (`docs/superpowers/specs/2026-07-31-...-design.md`):
     `Riesgo` (Alto/Medio/Bajo) se traduce a semáforo (Rojo/Ámbar/Verde).
   - La agenda del día reutiliza `calendario_<curso>.md` y las
     `actividadesPorSesion`/`actividadesFlexibles` que ya alimentan el
     calendario visual (el campo `**Sesión(es) sugerida(s):**` que
     `/asig-tarea` ya exige y `/asig-programacion` ya consume, ya
     retrofitado en las 121 tareas existentes de VCF y MET).
   - La planificación semanal reutiliza la misma ventana de "próxima
     preparación" (unidades próximas + qué material falta) que ya
     calcula el resumen semanal — solo cambia el encuadre (checklist de
     preparación, no panel de estado) y la ventana temporal.
5. **Se excluye del informe diario cualquier contenido que dependa de
   calificaciones**, en concreto "alumnado con entregas pendientes
   reiteradas" de la propuesta original — mismo motivo que en la
   decisión de dejar fuera revisión mensual/trimestral.
6. **Formato de salida: HTML publicado + borrador de Gmail para las dos**,
   igual que el resumen semanal ya existente — decisión explícita del
   docente incluso para el informe diario (más frecuente que el resumen
   semanal), priorizando la consistencia visual y la posibilidad de
   repasar cualquiera de los tres touchpoints semanales/diarios fuera de
   Claude Code (móvil) sobre el menor volumen de archivos generados.
7. **Este spec no crea los recordatorios de Calendar.** Su creación real
   (vía `/asig-calendar-sync`) es una acción explícita aparte, con
   confirmación del docente en el momento — mismo límite que ya aplica a
   toda integración de Calendar/Drive en el proyecto (regla 5 de
   `CLAUDE.md`).

## Arquitectura

### Informe diario

**Disparo:** recordatorio de Calendar limitado a los días de la unión de
horarios de VCF y MET (hoy: martes, miércoles y jueves para VCF, más los
días de MET). El docente lo ejecuta él mismo al sonar el recordatorio; no
hay ejecución en la nube.

**Contenido, en este orden:**

1. **Agenda del día.** Por cada asignatura con clase hoy: unidad y sesión
   correspondiente (de `calendario_<curso>.md`), sus actividades
   previstas (de `actividadesPorSesion` para el número de sesión de hoy),
   y material a revisar antes de la clase (documentos `BORRADOR` o
   incompletos ligados a esa unidad, según la tabla Documentos del modo
   registro).
2. **Alertas críticas.** Derivadas de la tabla Documentos del modo
   registro, sin recorrer el repositorio de nuevo:
   - Documento `BORRADOR` cuya unidad empieza en los próximos 3 días.
   - Examen `APROBADO` sin su solucionario `APROBADO` correspondiente (o
     viceversa).
   - Normativa con "Cambios detectados — pendientes de revisión" sin
     resolver en `normativa_registro.md`.
   - Sesión de hoy afectada por un día no lectivo (cruce contra los días
     no lectivos de Extremadura que ya usa `/asig-programacion` al
     generar el calendario).
3. **Próximos 7 días.** Exámenes, entregas y preparación de unidades cuyo
   inicio cae en los próximos 7 días — misma lógica que la tarea 5 del
   informe completo / el resumen semanal, con la ventana reducida a 7 en
   vez de 14/30/45.
4. **Semáforo de asignaturas.** La fila de Panel general de cada
   asignatura (VCF, MET), con su color (`Riesgo: Alto` → Rojo, `Medio` →
   Ámbar, `Bajo` → Verde).
5. **Acción prioritaria.** Una frase con el hallazgo más urgente de los
   puntos 2-4 (si hay alguno marcado como vencido o crítico); si no hay
   ninguno, una frase indicando que no hay nada urgente hoy.

**Artefacto:**
`DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/INFORMES_DIARIOS/informe_diario_<YYYY-MM-DD>.html`
(fecha de hoy), publicado con la herramienta Artifact, más un borrador de
Gmail (`Informe diario · Formdepor — <DD/MM>`) con el enlace y un resumen
breve en texto de la acción prioritaria.

### Planificación semanal

**Disparo:** recordatorio de Calendar los domingos por la tarde,
independiente del recordatorio de resumen semanal (viernes) ya existente.

**Contenido, en este orden:**

1. **Agenda de clases de la semana** que empieza mañana lunes, por
   asignatura.
2. **Materiales necesarios** para esas clases (de la tabla Documentos:
   qué existe, qué falta).
3. **Tareas `BORRADOR`** ligadas a esas unidades que deberían publicarse
   (pasar a `APROBADO` vía `/asig-revision`) antes de usarse.
4. **Huecos de contenido** de las unidades de las próximas 1-2 semanas —
   misma lógica que "próxima preparación" del resumen semanal, pero
   encuadrada como lista de tareas pendientes de generar, no como estado.
5. **Exámenes/solucionarios pendientes** de esas unidades.
6. **Prioridades de preparación:** lista ordenada (más urgente primero),
   derivada de los puntos 2-5 — no una sección nueva de cálculo, une lo
   ya listado arriba en un único orden de trabajo.

**Artefacto:**
`DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/PLANIFICACION_SEMANAL/planificacion_semanal_<YYYY-MM-DD>.html`
(fecha del domingo de generación), publicado con Artifact, más un
borrador de Gmail (`Planificación semanal · Formdepor — semana del
<DD/MM> al <DD/MM>`) con el enlace y las prioridades de preparación en
texto.

## Riesgos y mitigación

- **Riesgo: volumen de archivos.** Con informe diario (hasta 5-6
  veces/semana entre VCF y MET) y planificación semanal (1 vez/semana),
  además del resumen semanal ya existente, `00_CENTRO_CONTROL/` acumula
  bastantes artefactos HTML con el tiempo. Mitigación: es una decisión
  explícita del docente (ver decisión 6), y cada uno vive en su propia
  subcarpeta (`INFORMES_DIARIOS/`, `PLANIFICACION_SEMANAL/`,
  `RESUMENES_SEMANALES/`) para no mezclarse ni dificultar encontrar el
  más reciente de cada tipo.
- **Riesgo: redundancia real entre resumen semanal y planificación
  semanal**, pese a la decisión 3 de mantenerlos separados. Mitigación:
  no es un riesgo técnico sino de uso — si en la práctica resultan
  redundantes, se puede fusionar más adelante sin que este spec lo
  impida; de momento se implementan como dos modos distintos, tal como
  pidió el docente.
- **Riesgo: el cálculo del "semáforo" y las "alertas críticas" depende
  por completo de que el modo registro se ejecute primero (o de que su
  lógica se reutilice inline).** Mitigación: el informe diario no llama
  al modo registro como un paso previo separado — reutiliza literalmente
  las mismas reglas de cálculo ya escritas en `## Modo registro (Centro
  de Control Docente)` de `SKILL.md` (mismo barrido de documentos,
  mismas fórmulas de Riesgo), evitando así una dependencia de ejecución
  entre modos.

## Fuera de alcance (siguiente paso, no parte de este plan)

- Revisión mensual y cierre trimestral — pendientes de que haya
  calificaciones reales cargadas y `/asig-analitica` sea ejecutable.
- La creación real de los dos recordatorios de Calendar nuevos — acción
  explícita aparte, con confirmación del docente en el momento, vía
  `/asig-calendar-sync`.
- La taxonomía de 8 estados documentales (bloque D) — sigue pendiente,
  como su propio spec futuro.

## Siguiente paso

Invocar la skill `writing-plans` para convertir este diseño en un plan de
implementación paso a paso (que incluirá añadir los modos 4 y 5 a
`.claude/skills/asig-estado/SKILL.md`, y verificarlos contra datos reales
de VCF y MET, igual que se hizo con el modo registro).
