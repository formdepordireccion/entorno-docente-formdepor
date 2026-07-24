---
name: vcf-mantenimiento
description: Barrido quincenal de todo el proyecto VCF — detecta desactualizaciones, incoherencias y errores estructurales, dispara las skills correspondientes para generar correcciones en BORRADOR, propone (sin aplicar) mejoras a otras skills cuando detecta patrones repetidos de fricción, y deja un borrador de email resumen si hay hallazgos. Úsalo cuando el usuario pida revisar la salud del proyecto, hacer mantenimiento, o cuando toque la ejecución quincenal recordada por calendario.
---

# /vcf-mantenimiento — Mantenimiento y salud del proyecto (VCF/TSEAS)

## Rol

Es al proyecto entero lo que `/vcf-vigilancia` es a la normativa: un
barrido periódico, pero de alcance mucho más amplio — coherencia interna,
contenido desactualizado, errores estructurales — y con capacidad de
disparar otras skills para generar correcciones (siempre en `BORRADOR`).
No sustituye a `/vcf-vigilancia` (normativa externa) ni la duplica: lee
su último resultado y actúa sobre lo que haya dejado pendiente.

## Entradas

- Todo `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/` (estructura,
  `ficha.yaml`, documentos generados), **excepto**
  `10_DIVERSIDAD/INFORMES_ALUMNADO/`, `10_DIVERSIDAD/PLANES_ADAPTACION/`
  y `11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/` (datos personales, fuera
  de alcance de este barrido por completo).
- `01_NORMATIVA_CURRICULO/normativa_registro.md`, sección "Cambios
  detectados — pendientes de revisión" si `/vcf-vigilancia` la dejó.
- `git log` / `git status` del proyecto.
- Los propios `.claude/skills/vcf-*/SKILL.md`.

## Tareas

### 1. Barrido de coherencia

Comprueba, en este orden, y registra cada hallazgo:

1. **`ficha.yaml` válido**: parsea sin errores; `estado` no ha cambiado
   fuera de una aprobación explícita registrada en el historial de git.
2. **Unidades ↔ archivos**: cada `ficha.yaml → unidades[].archivo`
   apunta a un archivo que existe; cada archivo de
   `05_UNIDADES/*.md` (salvo README) tiene entrada correspondiente en
   `ficha.yaml`.
3. **Drift de contenido**: para una muestra de unidades/temario/exámenes
   ya generados, compara los RA/criterios que citan contra el texto
   actual de `ficha.yaml → resultados_aprendizaje` /
   `criterios_evaluacion`. Si no coinciden (p. ej. porque
   `/vcf-normativa` se volvió a ejecutar y algo cambió), es un hallazgo
   de tipo "desactualizado".
4. **Documentos base coherentes entre sí**: `programacion_26_27.md` y
   `calendario_26_27.md` siguen reflejando las mismas fechas que
   `ficha.yaml → unidades`.
5. **Clasificación de carpetas**: nada en `06_TEMARIO/VIGENTE/` ni
   `07_ACTIVIDADES_TAREAS/VIGENTE/` que en realidad sea material
   migrado sin pasar por un comando de generación (mismo tipo de bug ya
   corregido una vez — ver `git log` para el patrón).
6. **Nomenclatura**: archivos que no siguen
   `ASIGNATURA_TIPO_UD_CURSO_VERSION_ESTADO.ext`.
7. **`BORRADOR` estancados**: más de 15 días sin modificarse (fecha de
   última modificación del archivo). Esto no se "repara": se lista para
   que el docente los revise en `/vcf-revision`.
8. **Auditoría de datos personales**: `git ls-files` no debe listar nada
   bajo `INFORMES_ALUMNADO/`, `PLANES_ADAPTACION/` ni `CALIFICACIONES/`
   salvo los `README.md`. Si aparece algo más, es un hallazgo
   **crítico** — repórtalo el primero, no esperes al resto del barrido.
9. **Normativa pendiente**: si `normativa_registro.md` tiene una sección
   "Cambios detectados — pendientes de revisión" de `/vcf-vigilancia`
   sin resolver, inclúyelo como hallazgo prioritario.
10. **Material nuevo sin auditar**: si `3. VALORACIÓN 25_26/` tiene
    contenido más reciente que la última entrada de
    `14_HISTORICO_CAMBIOS/migraciones.md`, señálalo.
11. **Recursos digitales ausentes**: para cada unidad `APROBADO`, indica
    si `09_RECURSOS_DIGITALES/` tiene algo generado para ella (cualquier
    plataforma). Esto **no es una carencia como la de unidad/temario/
    examen** — no hay ninguna regla que exija una presentación por
    unidad — así que se lista solo como sugerencia informativa, nunca
    como hallazgo a reparar.

### 2. Auto-remediación (siempre termina en `BORRADOR`)

Para los hallazgos de los puntos 2-6 del barrido:

- **Drift de contenido en unidad/tema/examen**: ejecuta `/vcf-unidad`,
  `/vcf-tema`, `/vcf-tarea` o `/vcf-examen` (según corresponda) para
  regenerarlo. Si el archivo afectado ya está `APROBADO`, la nueva
  versión se guarda incrementando `VERSION` (`V01` → `V02`) y en
  `BORRADOR`, **sin tocar ni borrar el `APROBADO` existente** — queda
  pendiente de que el docente decida vía `/vcf-revision`.
- **Documentos base desactualizados**: ejecuta `/vcf-programacion`
  (misma lógica de versión).
- **Clasificación de carpeta incorrecta o nomenclatura incorrecta**:
  corrígelo directamente con `git mv` (es una operación mecánica de
  reorganización, no genera contenido nuevo) y regístralo en
  `14_HISTORICO_CAMBIOS/migraciones.md`.

**Nunca** ejecutes `/vcf-auditoria` (copiar desde `3. VALORACIÓN 25_26/`)
ni `/vcf-normativa` (cambiar RA/criterios/horas legales) de forma
automática — ambos requieren confirmación explícita del docente por
diseño; este barrido solo los señala como hallazgo, nunca los dispara.
Tampoco ejecutes nunca `/vcf-recursos` automáticamente — aunque
PowerPoint local no tiene límite de cuota, generar una presentación
sigue siendo una decisión del docente para una unidad concreta, no algo
que deba pasar solo porque falta (punto 11 del barrido: es sugerencia,
no reparación). Tampoco toca nunca `/vcf-diversidad` ni `/vcf-analitica`.

### 3. Propuestas de mejora de otras skills (nunca se aplican solas)

Si detectas un patrón repetido de fricción entre ejecuciones (p. ej. una
skill que sistemáticamente no encuentra referencia histórica para cierto
tipo de RA, o un paso que el docente corrige a mano cada vez), redacta
una propuesta de cambio sobre el `SKILL.md` afectado — incluido, si
aplica, este mismo archivo — como un diff propuesto con su
justificación. Guárdala en
`DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/propuestas_mejora_skills/<skill>_<YYYY-MM-DD>.md`.
**Nunca edites el `SKILL.md` real directamente** — la propuesta se aplica
solo si el docente la confirma explícitamente en una sesión posterior.

### 4. Aviso al docente

Si hubo cualquier hallazgo o cambio, crea un borrador de correo (Gmail,
destinatario `formdepor.direccion@gmail.com`) resumiendo: qué se
detectó, qué se regeneró automáticamente (en `BORRADOR`, listo para
`/vcf-revision`), qué quedó solo señalado (normativa pendiente, material
sin auditar, hallazgos críticos de datos personales si los hubiera), y
qué propuestas de mejora de skill esperan revisión. **Solo un borrador
— nunca se envía automáticamente** (no existe una herramienta de envío
de correo en este entorno). Si el barrido no encuentra nada, no crees
ningún borrador.

## Salidas

Contenido regenerado en `BORRADOR` donde aplique, reorganizaciones
mecánicas ya aplicadas (con commit), propuestas de mejora de skills en
`00_CENTRO_CONTROL/propuestas_mejora_skills/`, y un borrador de email si
hubo hallazgos.

## Límites

Nunca aprueba nada. Nunca ejecuta `/vcf-auditoria` ni `/vcf-normativa`
por su cuenta. Nunca toca `/vcf-diversidad`, `/vcf-analitica`, ni las
tres carpetas de datos personales. Nunca aplica un cambio a un `SKILL.md`
sin confirmación explícita — solo propone. Nunca envía correo, solo dejar
un borrador. Cada corrección automática (regeneración o reorganización)
termina en un commit de git con mensaje que la identifique como
originada por `/vcf-mantenimiento`.

## Validación humana

Obligatoria para: aprobar cualquier `BORRADOR` regenerado (vía
`/vcf-revision`), aplicar cualquier propuesta de mejora de skill, enviar
el email (el docente lo revisa y envía él mismo desde Gmail), y
cualquier hallazgo marcado como crítico (datos personales fuera de
sitio).
