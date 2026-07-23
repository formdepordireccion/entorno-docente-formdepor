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
