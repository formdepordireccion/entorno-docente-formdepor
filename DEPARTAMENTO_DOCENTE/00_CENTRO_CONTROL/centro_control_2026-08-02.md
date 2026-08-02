# Centro de control docente — 2026-08-02

Primera ejecución real del "Modo registro" de `/asig-estado`
(`.claude/skills/asig-estado/SKILL.md → ## Modo registro (Centro de
Control Docente)`), hecha a mano como verificación de que las
instrucciones son seguibles sin ambigüedad (Tarea 4 del plan de
implementación del modo registro).

**Alcance de esta ejecución (nota de verificación, no aplica a ejecuciones
futuras del modo):** por diseño de la verificación, la tabla "Documentos"
solo cubre el universo completo de dos subcarpetas de VCF_TSEAS
(`05_UNIDADES/` y `08_EVALUACION/`, 27 documentos), no las 250+ que
cubriría una ejecución real del modo registro sobre todo el
departamento. La fila de MET_TSEAS en "Panel general" se calculó con un
barrido agregado (recuentos de archivos, sin abrir cada documento ni
resolver su enlace de Drive) — ver nota bajo esa tabla. Una ejecución real
de `/asig-estado` en modo registro no tiene este recorte.

## Panel general

| Asignatura | % Preparación | Unidad actual | Próxima evaluación | Pendientes | Riesgo |
|---|---|---|---|---|---|
| VCF | 100% | — | 2026-09-29 | 0 | Bajo |
| MET | 100% | — | 2026-09-27 | 0 | Bajo |

Notas de cálculo:

- **VCF** — % Preparación, Pendientes y Riesgo se calculan sobre las 27
  filas de la tabla "Documentos" de abajo (únicamente
  `05_UNIDADES/`+`08_EVALUACION/`, ver nota de alcance arriba), no sobre
  el universo completo de VCF. Unidad actual: ninguna unidad de
  `ficha.yaml → unidades` tiene hoy (2026-08-02) dentro de su rango
  `fechas.inicio`-`fechas.fin` (la primera, UT0, empieza el 2026-09-10) →
  `—`. Próxima evaluación: de las unidades con examen en
  `08_EVALUACION/` cuyo `fechas.fin` todavía no ha llegado, la más
  próxima es UT0 (`fechas.fin = 2026-09-29`) — ver corrección aplicada al
  `SKILL.md` sobre cómo se define "la fecha del examen" para este campo.
- **MET** — calculado con el barrido agregado del Step 4 (recuento de
  archivos `APROBADO`/`BORRADOR` en `05_UNIDADES/`, `06_TEMARIO/VIGENTE/`,
  `07_ACTIVIDADES_TAREAS/VIGENTE/`, `08_EVALUACION/` y
  `09_RECURSOS_DIGITALES/`): 126 documentos totales, 126 `APROBADO`, 0
  `BORRADOR` → 100% preparación. "Pendientes" aquí solo refleja el
  recuento de `BORRADOR` (0) — **no se ha resuelto el enlace de Drive de
  ningún documento de MET en esta ejecución** (fuera del alcance del Step
  4 del plan, que pide expresamente no repetir el detalle fila por fila),
  así que no se puede afirmar si algún `APROBADO` de MET tiene
  "Subir a Drive" pendiente; ese posible pendiente no está contado
  arriba. Unidad actual: ninguna unidad de MET contiene hoy en su rango
  (UT0 empieza el 2026-09-10) → `—`. Próxima evaluación: unidad con
  examen en `08_EVALUACION/` (las 6 existen, UD00-UD05) cuyo `fechas.fin`
  más próximo aún no ha pasado: UT0, `fechas.fin = 2026-09-27`.

## Documentos

Universo: `VCF_TSEAS/05_UNIDADES/` (7 documentos, todos `Tipo = Unidad`) y
`VCF_TSEAS/08_EVALUACION/` (20 documentos: 10 exámenes + 10
solucionarios, todos `Tipo = Examen`). Se excluyen los `README.md` de
ambas carpetas (no tienen ciclo `BORRADOR`/`APROBADO`). Todos los
documentos de este universo están en estado `APROBADO`, versión `V01`,
curso `2026-2027`, con último commit `2026-07-24`
(`git log -1 --format=%as`). Ninguno tiene marcas `[NUEVO]`, "pendiente
de verificación manual" ni "sin respaldo histórico" (comprobado con
`grep` sobre los 27 archivos).

Enlace de Drive resuelto siguiendo el algoritmo de tres pasos del
`SKILL.md`: carpeta raíz `VCF_TSEAS 2026-2027` → subcarpeta
(`05_UNIDADES` u `08_EVALUACION`) → listado de archivos por `parentId`,
cruzando título (sin extensión) contra el nombre de archivo local. Los 27
documentos se encontraron subidos con ese algoritmo — ningún caso de "no
subido a Drive" en este universo, por lo que "Acción pendiente" queda
vacía en las 27 filas.

### Tipo: Unidad

| Asignatura | Unidad | Tipo | Curso | Estado | Versión | Última revisión | Próxima revisión | RA/Criterios | Enlace | Observaciones | Acción pendiente |
|---|---|---|---|---|---|---|---|---|---|---|---|
| VCF | UD00 | Unidad | 2026-2027 | APROBADO | V01 | 2026-07-24 | 2026-09-10 | RA2, RA7, RA7.a, RA7.b, RA7.c, RA7.d, RA7.e, RA7.f, RA7.g, RA7.h, RA8, RA8.a, RA8.b, RA8.c, RA8.d, RA8.e, RA8.f, RA8.g, RA9, RA9.a, RA9.b, RA9.c, RA9.d, RA9.e | [Drive](https://docs.google.com/document/d/1zhcWNJkHBy-BXnfyjaeQEkPjXRNIcmpS3sx1lKfpKgs/edit?usp=drivesdk) | | |
| VCF | UD01 | Unidad | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA1, RA2, RA2.a, RA2.b, RA2.c, RA2.d, RA2.e, RA2.f, RA3, RA4, RA7 | [Drive](https://docs.google.com/document/d/1U8xbmTIQ92y_arWADLiYutU9eiAUsbh54lJfBhEg5UI/edit?usp=drivesdk) | | |
| VCF | UD02 | Unidad | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA1, RA1.a, RA1.b, RA1.c, RA1.d, RA1.e, RA1.f, RA1.g, RA2, RA4, RA5, RA7 | [Drive](https://docs.google.com/document/d/1xjwRuCry3aXGwVoKGjNlx2GTkMvLGS_4HC6yIuyB3DA/edit?usp=drivesdk) | | |
| VCF | UD03a | Unidad | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA1, RA2, RA3, RA4, RA4.a, RA4.b, RA4.c, RA4.d, RA4.e, RA4.f, RA5, RA5.a, RA5.b, RA5.c, RA5.d, RA5.e, RA6, RA7 | [Drive](https://docs.google.com/document/d/103QCH5pcD_tNF3TSIh0rS_EUtSzXVT-Kh68yNhW-QK0/edit?usp=drivesdk) | | |
| VCF | UD03b | Unidad | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA1, RA2, RA3, RA3.a, RA3.b, RA3.c, RA3.d, RA3.e, RA3.f, RA3.g, RA4, RA5, RA6 | [Drive](https://docs.google.com/document/d/1-FAk2iodGT8FtzGZigieZ1rNupnDrzGMc2i8VrRBM9k/edit?usp=drivesdk) | | |
| VCF | UD03c | Unidad | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA3, RA4, RA5, RA6, RA6.a, RA6.b, RA6.c, RA6.d, RA6.e, RA6.f, RA7, RA8, RA9 | [Drive](https://docs.google.com/document/d/1_LjH1tuF3B5rWENLGiA1vfAltmFZe1JMlj3C_y8DM88/edit?usp=drivesdk) | | |
| VCF | UD04 | Unidad | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA6, RA7, RA7.a, RA7.b, RA7.c, RA7.d, RA7.e, RA7.f, RA7.g, RA7.h, RA8, RA8.a, RA8.b, RA8.c, RA8.d, RA8.e, RA8.f, RA8.g, RA9, RA9.a, RA9.b, RA9.c, RA9.d, RA9.e | [Drive](https://docs.google.com/document/d/1Ak3VaDiCSRuuxN28PlhhZipzf9OMP-3g3dt7myLBSgs/edit?usp=drivesdk) | | |

### Tipo: Examen

| Asignatura | Unidad | Tipo | Curso | Estado | Versión | Última revisión | Próxima revisión | RA/Criterios | Enlace | Observaciones | Acción pendiente |
|---|---|---|---|---|---|---|---|---|---|---|---|
| VCF | UD00 | Examen | 2026-2027 | APROBADO | V01 | 2026-07-24 | 2026-09-10 | RA7, RA7.a, RA7.b, RA7.c, RA7.d, RA7.e, RA7.f, RA7.g, RA7.h, RA8, RA8.a, RA8.b, RA8.c, RA8.d, RA8.e, RA8.f, RA8.g, RA9, RA9.a, RA9.b, RA9.c, RA9.d, RA9.e | [Drive](https://docs.google.com/document/d/1RoxpAUo1wn_z6Hwe230In8IAJYtWaAptWDBlE5OhJHA/edit?usp=drivesdk) | | |
| VCF | UD00 | Examen (solucionario) | 2026-2027 | APROBADO | V01 | 2026-07-24 | 2026-09-10 | RA7.a, RA7.b, RA7.c, RA7.d, RA7.e, RA7.f, RA7.g, RA7.h, RA8.a, RA8.b, RA8.c, RA8.d, RA8.e, RA8.f, RA8.g, RA9.a, RA9.b, RA9.c, RA9.d, RA9.e | [Drive](https://docs.google.com/document/d/1BfavaBrqF70ECNzzN_ZUGwr773AeQii8a_XjFFBhx5s/edit?usp=drivesdk) | | |
| VCF | UD01 | Examen | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA2, RA2.a, RA2.b, RA2.c, RA2.d, RA2.e, RA2.f | [Drive](https://docs.google.com/document/d/1Uz3J3bpyLEWfXI7DHfSyRJ_440hHygZNqrk5pBoF8mc/edit?usp=drivesdk) | | |
| VCF | UD01 | Examen (solucionario) | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA2.a, RA2.b, RA2.c, RA2.d, RA2.e, RA2.f | [Drive](https://docs.google.com/document/d/1TepFHvEcC5Sqxb9DF3eRhDKGi01-pUn2VdQGizf4mig/edit?usp=drivesdk) | | |
| VCF | UD02 | Examen | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA1, RA1.a, RA1.b, RA1.c, RA1.d, RA1.e, RA1.f, RA1.g | [Drive](https://docs.google.com/document/d/1R6WkyDwwogD0UIJyNWdZzWU7H68W4VjBR3ehMGKyA7s/edit?usp=drivesdk) | | |
| VCF | UD02 | Examen (solucionario) | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA1.a, RA1.b, RA1.c, RA1.d, RA1.e, RA1.f, RA1.g | [Drive](https://docs.google.com/document/d/1CP4xiJsGHdhwJplJ2GuMGOsZMP2ECUFafuEDpnbxGLY/edit?usp=drivesdk) | | |
| VCF | UD03a | Examen | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA4, RA4.a, RA4.b, RA4.c, RA4.d, RA4.e, RA4.f, RA5, RA5.a, RA5.b, RA5.c, RA5.d, RA5.e | [Drive](https://docs.google.com/document/d/1Y6_ZSFPfMtAy-utVpM1p943yY00dBoC9FtYAP1_rxCA/edit?usp=drivesdk) | | |
| VCF | UD03a | Examen (solucionario) | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA1, RA4.a, RA4.b, RA4.c, RA4.d, RA4.e, RA4.f, RA5.a, RA5.b, RA5.c, RA5.d, RA5.e | [Drive](https://docs.google.com/document/d/1jEJjgO6rNNpmOZTTQi7GGIT1JQHp3NrlXfkc2OuNIcQ/edit?usp=drivesdk) | | |
| VCF | UD03b | Examen | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA3, RA3.a, RA3.b, RA3.c, RA3.d, RA3.e, RA3.f, RA3.g | [Drive](https://docs.google.com/document/d/1biy_vHspSZfJVP1QC0BI2XuXt7N0KGegon5vBhDPeag/edit?usp=drivesdk) | | |
| VCF | UD03b | Examen (solucionario) | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA3.a, RA3.b, RA3.c, RA3.d, RA3.e, RA3.f, RA3.g | [Drive](https://docs.google.com/document/d/12hngPKg6dHM21nRdrdMVHwaVw_AUHBPWsUCO-ZWUypk/edit?usp=drivesdk) | | |
| VCF | UD03c | Examen | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA6, RA6.a, RA6.b, RA6.c, RA6.d, RA6.e, RA6.f | [Drive](https://docs.google.com/document/d/1A-LzxV42g5DHwVcf1khG-8t6fCnjwXxHu1hhvouO6Ik/edit?usp=drivesdk) | | |
| VCF | UD03c | Examen (solucionario) | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA6.a, RA6.b, RA6.c, RA6.d, RA6.e, RA6.f | [Drive](https://docs.google.com/document/d/1s0-TE6fgeg8dO_a3mubhmePMz0ukowURtUUjcs9Yhwg/edit?usp=drivesdk) | | |
| VCF | UD04 | Examen | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA7, RA7.a, RA7.b, RA7.c, RA7.d, RA7.e, RA7.f, RA7.g, RA7.h, RA8, RA8.a, RA8.b, RA8.c, RA8.d, RA8.e, RA8.f, RA8.g, RA9, RA9.a, RA9.b, RA9.c, RA9.d, RA9.e | [Drive](https://docs.google.com/document/d/1f7BrI_MNeFvMF7R70Y9fPFGFCFYjarq_aOZ9Lq206vU/edit?usp=drivesdk) | | |
| VCF | UD04 | Examen (solucionario) | 2026-2027 | APROBADO | V01 | 2026-07-24 | | RA7.a, RA7.b, RA7.c, RA7.d, RA7.e, RA7.f, RA7.g, RA7.h, RA8.a, RA8.b, RA8.c, RA8.d, RA8.e, RA8.f, RA8.g, RA9.a, RA9.b, RA9.c, RA9.d, RA9.e | [Drive](https://docs.google.com/document/d/1RsqlpXuNoFIS0-XsZkB52XPEkQ7dZBKzFhNoQ7c_DQo/edit?usp=drivesdk) | | |

## Correcciones aplicadas a `SKILL.md` durante esta verificación

Al ejecutar el algoritmo de "Enlace" (punto 4 de "Modo registro") contra
Drive real, aparecieron dos casos donde el texto tal como estaba escrito
no era seguible sin ambigüedad o sin fallo silencioso. Se corrigieron en
`.claude/skills/asig-estado/SKILL.md` en el momento (detalle en el propio
diff):

1. **Paginación del listado de una subcarpeta.** El texto decía "una
   única llamada `search_files` con `parentId = '<id>'` devuelve todos
   sus archivos". Al ejecutarlo contra `08_EVALUACION` (20 documentos)
   la llamada devolvió solo 10 y un `nextPageToken` — sin seguir
   paginando, la mitad de los documentos habría quedado marcada
   incorrectamente como "no subida a Drive". Se corrigió el texto para
   indicar que hay que seguir paginando con `nextPageToken` hasta
   agotarlo.
2. **Límite de tokens con documentos grandes.** La primera llamada sin
   `excludeContentSnippets` sobre `08_EVALUACION` superó el límite de
   tokens de salida de la herramienta (los exámenes+solucionarios son más
   grandes que las unidades) y no devolvió nada utilizable. Se añadió al
   texto la indicación de pasar `excludeContentSnippets: true` en las
   llamadas de este algoritmo, ya que el algoritmo solo necesita título y
   `viewUrl`, no el contenido.
3. **Definición de "la fecha del examen" en Panel general.** El punto 5
   decía "la fecha del examen más próximo en `08_EVALUACION/` cuya
   unidad todavía no ha llegado a su `fechas.fin`" sin decir de dónde
   sale esa fecha — no existe ningún campo de fecha propio por examen ni
   en `ficha.yaml` ni en el documento del examen. Se corrigió el texto
   para aclarar explícitamente que esa fecha es `fechas.fin` de la unidad
   correspondiente (el examen se sitúa convencionalmente al final de la
   unidad; confirmado además por el calendario real de VCF, donde los
   bloques "EVAL-Tn" caen justo tras el `fechas.fin` de la última unidad
   de cada trimestre).

Ningún otro punto del "Modo registro" necesitó corrección: el resto de
reglas (extracción de Estado/Versión/Unidad del nombre de archivo, fecha
de último commit, patrón `grep` de RA/Criterios, marcas de Observaciones,
regla de Acción pendiente) se siguieron literalmente y produjeron un
valor concreto en las 27 filas, sin ningún caso ambiguo.
