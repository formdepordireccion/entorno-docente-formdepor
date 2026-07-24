---
name: vcf-estado
description: Genera una foto de estado del proyecto VCF/TSEAS (rol de Coordinador / Centro de control) — qué falta en ficha.yaml, qué carpetas están vacías, próximos hitos del calendario, incoherencias detectadas, y qué unidades próximas en el calendario necesitan material todavía. Úsalo cuando el usuario pida el estado, resumen, panel de control, "qué falta", o qué preparar la semana que viene de la asignatura VCF.
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
   vacía. **Excepción:** `10_DIVERSIDAD/INFORMES_ALUMNADO/`,
   `10_DIVERSIDAD/PLANES_ADAPTACION/` y
   `11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/` contienen datos
   personales de alumnado — indica solo si tienen contenido o no
   (vacía/con documentos), nunca nombres de archivo ni ningún detalle de
   su contenido.
3. Si existe `calendario_26_27.md`, compáralo con la fecha actual y señala
   los hitos (unidades, evaluaciones, entregas) previstos en los próximos
   30 días.
4. Detecta incoherencias simples:
   - Unidades listadas en `ficha.yaml → unidades` sin archivo
     correspondiente en `05_UNIDADES/`.
   - Archivos con `BORRADOR` en el nombre que llevan más de 30 días sin
     modificarse (usa la fecha de última modificación del archivo).
5. **Próxima preparación (propuesta semanal):** ordena
   `ficha.yaml → unidades` por `fechas.inicio` y localiza las 2-3
   unidades reales (con `archivo`, no bloques de evaluación) cuyo inicio
   caiga dentro de los próximos 45 días. Para cada una, comprueba qué
   material ya existe y cuál falta:
   - Unidad (`05_UNIDADES/`) → si falta, sugiere `/vcf-unidad`.
   - Temario (`06_TEMARIO/VIGENTE/`, 6 archivos por unidad) → si falta o
     está incompleto, sugiere `/vcf-tema`.
   - Actividades/tareas propias de esa unidad
     (`07_ACTIVIDADES_TAREAS/VIGENTE/`) → si no hay ninguna, sugiere
     `/vcf-tarea` (aviso, no obligatorio).
   - Examen (`08_EVALUACION/`) → si falta, sugiere `/vcf-examen`.
   - Recursos digitales (`09_RECURSOS_DIGITALES/`, cualquier
     subcarpeta) → si no hay ninguno, sugiere `/vcf-recursos` (aviso, no
     obligatorio — a diferencia de unidad/temario/examen, no es
     obligatorio que exista).
   Ordena la lista por cercanía de fecha (lo más próximo primero), no
   por tipo de unidad.
6. Presenta un resumen con cinco bloques: **Pendiente de revisión**,
   **Huecos de contenido**, **Próximos hitos**, **Incoherencias**,
   **Próxima preparación**.
7. Si el usuario pide guardar el resumen, escríbelo en
   `DEPARTAMENTO_DOCENTE/00_CENTRO_CONTROL/estado_<YYYY-MM-DD>.md` con la
   fecha de hoy.

## Salidas

Resumen en el chat con los cinco bloques anteriores. Opcionalmente, un
archivo en `00_CENTRO_CONTROL/`.

## Límites

No modifica ni crea ningún documento de las carpetas 01-14 salvo el propio
informe en `00_CENTRO_CONTROL/`. No aprueba ni rechaza nada, solo informa.

## Validación humana

Ninguna: es puramente informativo. El usuario decide qué hacer con lo que
reporta.
