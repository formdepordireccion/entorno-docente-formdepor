---
name: vcf-calendar-sync
description: Crea eventos en Google Calendar (calendario principal del usuario) a partir de 04_TEMPORALIZACION/calendario_26_27.md y de ficha.yaml → unidades — inicio/fin de cada unidad, evaluaciones y recuperaciones. Úsalo cuando el usuario pida sincronizar, subir o crear en Calendar el calendario del curso de VCF.
---

# /vcf-calendar-sync — Integración con Google Calendar (VCF/TSEAS)

## Rol

Crea eventos en el calendario principal de Google del usuario a partir
del calendario de temporalización real de VCF, bajo petición explícita
en cada ejecución. Nunca corre en segundo plano.

## Entradas

- `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/04_TEMPORALIZACION/calendario_26_27.md`
- `ficha.yaml → unidades` (nombre, fechas de inicio/fin, estado —
  `aprobado`, `propuesta_pendiente_confirmacion` o
  `confirmado_calendario_oficial`)
- El calendario principal de Google del usuario (no se crea ni se pide
  elegir un calendario distinto salvo que el usuario lo pida
  explícitamente).

## Tareas

1. Lee `ficha.yaml → unidades` y agrupa las entradas en tres bloques por
   fiabilidad de la fecha: **confirmado_calendario_oficial** (fechas de
   una fuente oficial verificada), **aprobado** (unidad con documento ya
   aprobado por el docente, fechas propuestas por `/vcf-programacion` no
   verificadas más allá de eso), y **propuesta_pendiente_confirmacion**
   (ni la unidad ni las fechas están confirmadas todavía).
2. Antes de crear nada, comprueba en el calendario de Google si ya existe
   un evento con un título equivalente en fechas similares, para no
   duplicar si se ejecuta este comando más de una vez.
3. Presenta al usuario la lista de eventos que se van a crear, agrupada
   por los tres bloques del punto 1, dejando claro en el propio título o
   descripción del evento qué fiabilidad tiene cada fecha (p. ej.
   añadiendo "(fecha propuesta, pendiente de confirmar)" en el título o
   la descripción de los eventos que no sean `confirmado_calendario_oficial`).
4. Espera confirmación explícita. El usuario puede aprobar todos los
   bloques, o solo el de `confirmado_calendario_oficial` +
   `aprobado`, dejando fuera lo que aún es pura propuesta.
5. Tras confirmación, crea un evento por unidad/entrada confirmada:
   - Título: nombre de la unidad tal cual está en `ficha.yaml`.
   - Fechas: `fechas.inicio` a `fechas.fin` (evento de varios días si
     aplica).
   - Descripción: RA que cubre, fiabilidad de la fecha, y enlace/ruta al
     archivo de la unidad si existe (`archivo` en `ficha.yaml`).
6. Informa con el número de eventos creados y con qué fiabilidad cada
   uno, y qué quedó fuera por no estar confirmado.

## Salidas

Eventos creados en el calendario principal de Google del usuario; resumen
en el chat.

## Límites

Nunca crea eventos a partir de fechas `propuesta_pendiente_confirmacion`
sin que el usuario lo pida explícitamente sabiendo que son provisionales.
No modifica ni borra eventos existentes que no haya creado este mismo
comando. No inventa horas concretas (día/hora/aula) si `ficha.yaml` no las
tiene confirmadas — usa eventos de día completo en ese caso, en vez de
inventar un horario.

## Validación humana

Obligatoria antes de crear cualquier evento (puede darse en bloque por
grupo de fiabilidad).
