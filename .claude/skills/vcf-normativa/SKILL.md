---
name: vcf-normativa
description: Localiza y registra la normativa oficial (RD estatal del título TSEAS y normativa autonómica de Extremadura) del módulo Valoración de la Condición Física, extrae resultados de aprendizaje/criterios/contenidos/horas, y genera la matriz de alineación curricular. Úsalo cuando el usuario pida buscar, actualizar o verificar la normativa/currículo de VCF.
---

# /vcf-normativa — Normativa y currículo (VCF/TSEAS)

## Rol

Localiza normas oficiales en BOE y en el Diario Oficial de Extremadura
(DOE), registra fuente/fecha/norma, y extrae competencias, resultados de
aprendizaje, criterios, contenidos y horas del módulo VCF dentro del
título TSEAS.

## Entradas

- `ficha.yaml` (para saber qué campos de normativa ya están rellenos)
- Título: Técnico Superior en Enseñanza y Animación Sociodeportiva (TSEAS)
- Módulo: Valoración de la Condición Física (VCF)
- Comunidad autónoma: Extremadura

## Tareas

1. Con WebSearch, busca en boe.es el Real Decreto que regula el título
   TSEAS y localiza dentro de él el módulo profesional correspondiente a
   "Valoración de la Condición Física" (comprueba el nombre oficial exacto
   del módulo, puede diferir ligeramente).
2. Extrae del RD: resultados de aprendizaje, criterios de evaluación,
   contenidos y horas mínimas del módulo.
3. Con WebSearch, busca en el Diario Oficial de Extremadura (DOE) el
   decreto autonómico que desarrolla el currículo de TSEAS en Extremadura,
   y localiza las horas/contenidos específicos de VCF si los hay.
4. Escribe `01_NORMATIVA_CURRICULO/normativa_registro.md` con, para cada
   norma encontrada: título de la norma, URL fuente, fecha de publicación,
   fecha de consulta de hoy, y artículos/anexos relevantes citados
   literalmente.
5. Actualiza `ficha.yaml`:
   - `normativa.rd_estatal`: identificador y URL del RD.
   - `normativa.decreto_curriculo_autonomico`: identificador y URL del
     decreto de Extremadura.
   - `resultados_aprendizaje`, `criterios_evaluacion`, `contenidos`: listas
     extraídas de la norma (texto literal o resumen fiel, citando el
     artículo de origen).
   - `asignatura.horas_totales`, `asignatura.horas_semanales`.
   - `estado` permanece en `borrador`.
6. Genera `03_MAPA_CURRICULAR/matriz_alineacion.md`: una tabla que cruza
   cada resultado de aprendizaje con sus criterios de evaluación y
   contenidos asociados.
7. Presenta un resumen al usuario y pide confirmación explícita antes de
   que cualquier otro comando trate estos datos como definitivos.

## Salidas

`normativa_registro.md`, `matriz_alineacion.md`, `ficha.yaml` actualizado.

## Límites

No marca `ficha.yaml.estado` como `aprobado`. Si no encuentra la norma
exacta o algún dato no puede verificarse, lo dice explícitamente ("no he
podido confirmar X, pendiente de verificación manual") en vez de inventar
artículos, fechas u horas.

## Validación humana

Obligatoria: el docente debe confirmar que el RD y el decreto localizados
son los correctos antes de que `/vcf-programacion`, `/vcf-unidad`, `/vcf-tema`
o `/vcf-examen` usen estos datos.
