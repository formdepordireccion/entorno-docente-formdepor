---
name: vcf-vigilancia
description: Comprueba si ha cambiado alguna de las normas ya verificadas de VCF (RD 653/2017, Decreto 106/2018, Instrucción 13/2024) o si se ha publicado calendario escolar de Extremadura para el curso siguiente, y avisa solo si encuentra algo nuevo. Úsalo cuando el usuario pida comprobar, vigilar o revisar si ha cambiado la normativa de VCF, y en la ejecución trimestral programada.
---

# /vcf-vigilancia — Vigilancia normativa (VCF/TSEAS)

## Rol

Comprueba periódicamente si las normas ya verificadas en
`01_NORMATIVA_CURRICULO/normativa_registro.md` siguen vigentes sin
cambios, y si se ha publicado el calendario escolar de Extremadura para
el curso siguiente al que refleja `ficha.yaml`. No cambia nada por su
cuenta: si encuentra algo, lo registra como pendiente de revisión y
avisa — nunca actualiza `ficha.yaml` ni ningún documento aprobado sin
confirmación explícita del docente.

## Entradas

- `01_NORMATIVA_CURRICULO/normativa_registro.md` (normas ya verificadas,
  con sus URLs y fechas de consulta).
- `ficha.yaml → normativa` (RD estatal, decreto autonómico, y sus datos
  de horas).
- `ficha.yaml → asignatura.curso_academico`.

## Tareas

1. Con WebSearch/WebFetch, comprueba cada norma ya registrada:
   - RD 653/2017: ¿sigue siendo el RD vigente para el título TSEAS, o hay
     un RD posterior que lo modifique o derogue (p. ej. por una reforma
     de la LOE/LOMLOE que afecte a este ciclo)?
   - Decreto 106/2018 (Extremadura): ¿sigue vigente, o hay un decreto
     autonómico posterior que lo sustituya para este título?
   - Instrucción 13/2024 (Extremadura): ¿sigue siendo la instrucción
     aplicable a la carga horaria del módulo 1136, o hay una instrucción
     posterior que la sustituya para el curso reflejado en
     `ficha.yaml → asignatura.curso_academico`?
2. Comprueba si se ha publicado en el DOE la resolución del calendario
   escolar de Extremadura para el curso siguiente al de
   `ficha.yaml → asignatura.curso_academico` (por ejemplo, si la ficha
   dice 2026-2027, busca si ya existe la resolución de calendario para
   2027-2028; suele publicarse hacia junio del año anterior).
3. Si TODO sigue igual (ninguna norma nueva, ningún calendario nuevo
   publicado todavía), no toques ningún archivo. Informa en una sola
   frase: "Sin cambios: las 3 normas siguen vigentes, sin calendario
   nuevo publicado todavía."
4. Si encuentras un cambio real (norma derogada/sustituida, o calendario
   nuevo publicado):
   - No lo apliques tú. Añade una entrada fechada en
     `01_NORMATIVA_CURRICULO/normativa_registro.md`, sección nueva
     "## Cambios detectados — pendientes de revisión", citando la fuente
     nueva encontrada (URL, fecha) y qué norma/dato de `ficha.yaml`
     podría verse afectado.
   - Avisa explícitamente al usuario, describiendo qué cambió y qué
     acción sugieres (normalmente: volver a ejecutar `/vcf-normativa` o
     `/vcf-programacion` para esa parte concreta).
5. Si esta tarea se ejecuta desde un agente programado (sin usuario
   presente en el momento), el aviso del paso 4 se entrega igualmente
   (por el canal de notificación disponible en ese contexto) — pero la
   entrada en `normativa_registro.md` y el commit de git se hacen igual,
   para que quede constancia aunque el docente lo revise más tarde.

## Salidas

Sin cambios: solo un mensaje corto, ningún archivo tocado. Con cambios:
entrada nueva en `normativa_registro.md` + commit de git + aviso
explícito al usuario.

## Límites

Nunca actualiza `ficha.yaml`, ni ningún documento `APROBADO`, ni el
calendario del curso, a partir de lo que encuentre aquí — eso requiere
volver a ejecutar `/vcf-normativa` o `/vcf-programacion` con
confirmación explícita del docente. No inventa un cambio para tener algo
que reportar: si la búsqueda no es concluyente, lo dice como tal
("no he podido confirmar si sigue vigente, revisar manualmente") en vez
de afirmar que no hay cambios.

## Validación humana

No aplica para la propia comprobación (es de solo lectura). Sí es
obligatoria antes de que cualquier cambio detectado se aplique a
`ficha.yaml` o a documentos aprobados, vía los comandos correspondientes.
