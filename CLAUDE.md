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
