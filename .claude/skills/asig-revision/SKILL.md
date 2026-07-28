---
name: asig-revision
description: Revisa rápidamente todos los documentos de la asignatura resuelta que están en BORRADOR, agrupados por tipo (documentos base, unidades didácticas, temario, evaluación), y aprueba (renombra a APROBADO o actualiza el marcador de estado) los que el docente confirme explícitamente. Úsalo cuando el usuario quiera revisar, aprobar, o pasar a APROBADO los borradores de una asignatura.
---

# /asig-revision — Revisión y aprobación de documentos

## Rol

Ayuda al docente a revisar de forma rápida todo lo que está en `BORRADOR`
en la asignatura resuelta, agrupado por tipo de documento, y aprueba
(marca como `APROBADO`) lo que el docente confirme explícitamente.

## Entradas

Todas las rutas de esta sección son relativas a la asignatura resuelta
según `CLAUDE.md → "Cómo se resuelve la asignatura"` — si el usuario no
especifica ninguna y hay más de una, pregúntale cuál.

- Archivos con `BORRADOR` en el nombre bajo `05_UNIDADES/`,
  `06_TEMARIO/VIGENTE/`, `07_ACTIVIDADES_TAREAS/VIGENTE/` (recorre sus 11
  subcarpetas por tipo de actividad — ver `/asig-tarea`) y
  `08_EVALUACION/`.
- Los 4 documentos base, que no usan `BORRADOR` en el nombre de archivo
  (para no romper las rutas fijas que otros comandos leen) sino un
  marcador `**Estado:** BORRADOR` en su cabecera:
  - `01_NORMATIVA_CURRICULO/normativa_registro.md`
  - `03_MAPA_CURRICULAR/matriz_alineacion.md`
  - `02_PROGRAMACION/programacion_26_27.md`
  - `04_TEMPORALIZACION/calendario_26_27.md`
- `ficha.yaml` (estado global y estado de cada unidad en `unidades`).

## Tareas

1. Escanea las entradas y agrupa en este orden fijo:
   1. **Documentos base** (normativa → mapa curricular → programación →
      calendario)
   2. **Unidades didácticas** (`05_UNIDADES/`)
   3. **Temario** (`06_TEMARIO/VIGENTE/`)
   4. **Actividades y tareas** (`07_ACTIVIDADES_TAREAS/VIGENTE/`, solo lo
      generado por `/asig-tarea` — no el material migrado por
      `/asig-auditoria`, que no lleva `BORRADOR`/`APROBADO`; dentro del
      grupo, agrupa además por subcarpeta/categoría de actividad para
      que la tabla sea legible)
   5. **Evaluación** (`08_EVALUACION/`, exámenes y solucionarios)
2. Para cada grupo, presenta una tabla compacta: archivo | resumen de una
   línea (de qué trata, qué RA/unidad cubre) | avisos conocidos. Los
   avisos se sacan del propio documento (marcas `[NUEVO]`, notas de "no
   confirmado", "pendiente de verificación manual", "sin respaldo
   histórico", discrepancias señaladas, etc.) — nunca se ocultan para
   agilizar la revisión, se listan siempre aunque el grupo se apruebe en
   bloque.
3. Presenta el grupo completo y espera confirmación explícita antes de
   aprobar nada. El docente puede:
   - Aprobar el grupo entero.
   - Aprobar el grupo excluyendo archivos concretos ("todo el temario
     menos el glosario de UD03a").
   - Pedir revisar un archivo concreto con más detalle antes de decidir.
   - Rechazar/posponer el grupo entero.
4. Al aprobar un archivo con nomenclatura
   `..._V01_BORRADOR.md`/`..._V01_BORRADOR_<TIPO>.md`, renómbralo a
   `..._V01_APROBADO.md`/`..._V01_APROBADO_<TIPO>.md` (conservando el
   resto del nombre) usando `git mv`, no `mv` a secas.
5. Al aprobar uno de los 4 documentos base, sustituye su marcador de
   cabecera (`**Estado: BORRADOR.**`, `**Estado:** BORRADOR` o similar,
   respeta el formato exacto de cada archivo) por
   `**Estado: APROBADO** (aprobado por el docente el <fecha de hoy>).`
6. Al aprobar una unidad didáctica, actualiza también su entrada en
   `ficha.yaml → unidades`: `estado: propuesta_pendiente_confirmacion` →
   `estado: aprobado`. No toques fechas, RA ni ningún otro campo de esa
   entrada ni de las demás.
7. Si tras esta revisión TODO queda aprobado (los 4 documentos base,
   todas las unidades y todo su temario/tareas/examen), pregunta
   explícitamente al docente si quiere marcar también
   `ficha.yaml → estado: aprobado` a nivel de asignatura. Nunca lo
   cambies sin que lo pida de forma explícita para ese campo en
   concreto.
8. Cada aprobación (de un archivo, de un grupo, o del estado global)
   termina en un commit de git con un mensaje que identifique
   exactamente qué se aprobó, siguiendo la regla ya fijada en
   `CLAUDE.md`.

## Salidas

Archivos renombrados a `APROBADO`, marcadores de estado actualizados en
los 4 documentos base, `ficha.yaml` actualizado, un commit por grupo
aprobado (o por archivo, si el docente pide ese nivel de detalle).

## Límites

Nunca aprueba nada sin confirmación explícita del docente para ese
documento o grupo — "aprueba todo" sin que el docente haya visto el
resumen del grupo no cuenta como confirmación válida; siempre hay que
presentar la tabla primero. Nunca oculta un aviso conocido para que el
grupo se apruebe más rápido. No inventa que un documento fue revisado en
detalle si el docente solo confirmó el resumen. **Nunca incluye
`10_DIVERSIDAD/INFORMES_ALUMNADO/`, `10_DIVERSIDAD/PLANES_ADAPTACION/`
ni `11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/` en ningún grupo** — esos
documentos no tienen ciclo `BORRADOR`/`APROBADO` (ver `/asig-diversidad`,
`/asig-analitica`), quedan fuera de este comando por completo.

## Validación humana

Obligatoria en cada grupo (o archivo, si se pide ese nivel). Es la puerta
de salida de todo lo que generan `/asig-unidad`, `/asig-tema`, `/asig-examen`,
`/asig-programacion` y `/asig-normativa`.
