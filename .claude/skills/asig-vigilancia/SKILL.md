---
name: asig-vigilancia
description: Comprueba, para cada asignatura que tenga normativa ya verificada, si esa normativa ha cambiado, o si se ha publicado calendario escolar de Extremadura para el curso siguiente, y avisa solo si encuentra algo nuevo. Úsalo cuando el usuario pida comprobar, vigilar o revisar si ha cambiado la normativa de una asignatura (o de todas, si no especifica ninguna), y en la ejecución trimestral programada.
---

# /asig-vigilancia — Vigilancia normativa

## Rol

Comprueba periódicamente si las normas ya verificadas en
`01_NORMATIVA_CURRICULO/normativa_registro.md` de una asignatura siguen
vigentes sin cambios, y si se ha publicado el calendario escolar de
Extremadura para el curso siguiente al que refleja el `ficha.yaml` de esa
asignatura. No cambia nada por su cuenta: si encuentra algo, lo registra
como pendiente de revisión y avisa — nunca actualiza `ficha.yaml` ni
ningún documento aprobado sin confirmación explícita del docente.

Es uno de los comandos de solo lectura/informe que forman la excepción de
CLAUDE.md → "Cómo se resuelve la asignatura" (punto 4): si el usuario lo
invoca **sin mencionar ninguna asignatura**, no pregunta cuál — recorre
automáticamente **todas** las asignaturas que ya tengan
`01_NORMATIVA_CURRICULO/normativa_registro.md` (es decir, las que ya han
pasado al menos una vez por `/asig-normativa`), y omite silenciosamente
cualquier asignatura que todavía no tenga ese archivo, porque no hay nada
registrado que reverificar. Si el usuario sí menciona una asignatura
concreta, se resuelve según esa misma sección de CLAUDE.md y solo se
comprueba esa. Cada asignatura se trata de forma independiente: aunque
dos asignaturas citen hoy las mismas normas (p. ej. VCF y MET, ambas
módulos de TSEAS), cada una verifica y registra su propia normativa por
separado, sin asumir que lo que vale para una vale automáticamente para
la otra.

## Entradas

Por cada asignatura recorrida (ver "Rol"):

- `01_NORMATIVA_CURRICULO/normativa_registro.md` de esa asignatura (normas
  ya verificadas, con sus URLs y fechas de consulta).
- `ficha.yaml → normativa` de esa asignatura (RD estatal, decreto
  autonómico, y sus datos de horas).
- `ficha.yaml → asignatura.curso_academico` de esa asignatura.

## Tareas

Repite los pasos 1-4 para cada asignatura que corresponda comprobar (ver
"Rol"):

1. Lee `01_NORMATIVA_CURRICULO/normativa_registro.md` de la asignatura en
   curso de esta comprobación y, con WebSearch/WebFetch, reverifica cada
   norma que ese archivo tenga registrada (identificándola por el
   nombre/identificador exacto que conste allí — RD, decreto autonómico,
   instrucciones u otras normas que se hayan ido añadiendo, sin asumir de
   antemano cuántas ni cuáles son):
   - Para cada norma registrada: ¿sigue vigente tal cual, o hay una norma
     posterior (estatal o autonómica de Extremadura) que la modifique,
     sustituya o derogue para el título/módulo de esta asignatura?
   - Para las normas ligadas a un curso académico concreto (p. ej. una
     instrucción sobre carga horaria): ¿sigue siendo la aplicable para el
     curso reflejado en `ficha.yaml → asignatura.curso_academico` de esta
     asignatura, o hay una versión posterior que la sustituya para ese
     curso?
2. Comprueba si se ha publicado en el DOE la resolución del calendario
   escolar de Extremadura para el curso siguiente al de
   `ficha.yaml → asignatura.curso_academico` de esta asignatura (por
   ejemplo, si la ficha dice 2026-2027, busca si ya existe la resolución
   de calendario para 2027-2028; suele publicarse hacia junio del año
   anterior). El calendario escolar es común a toda Extremadura, así que
   si ya se comprobó para una asignatura en esta misma ejecución, no hace
   falta repetir la búsqueda para las siguientes — basta con reutilizar el
   resultado.
3. Si TODO sigue igual para esta asignatura (ninguna norma nueva, ningún
   calendario nuevo publicado todavía), no toques ningún archivo de esta
   asignatura. Informa en una sola frase por asignatura, por ejemplo: "VCF:
   sin cambios, las N normas registradas siguen vigentes, sin calendario
   nuevo publicado todavía."
4. Si encuentras un cambio real para esta asignatura (norma
   derogada/sustituida, o calendario nuevo publicado):
   - No lo apliques tú. Añade una entrada fechada en el
     `01_NORMATIVA_CURRICULO/normativa_registro.md` de esa asignatura,
     sección nueva "## Cambios detectados — pendientes de revisión",
     citando la fuente nueva encontrada (URL, fecha) y qué norma/dato de
     su `ficha.yaml` podría verse afectado.
   - Avisa explícitamente al usuario, identificando de qué asignatura se
     trata, describiendo qué cambió y qué acción sugieres (normalmente:
     volver a ejecutar `/asig-normativa` o `/asig-programacion` para esa
     asignatura y esa parte concreta).
5. Si se han recorrido varias asignaturas en esta ejecución, cierra con un
   resumen agregado (una línea por asignatura: sin cambios / cambios
   detectados) además de los avisos individuales del paso 4.
6. Si esta tarea se ejecuta desde un agente programado (sin usuario
   presente en el momento), el aviso del paso 4 se entrega igualmente
   (por el canal de notificación disponible en ese contexto) — pero la
   entrada en `normativa_registro.md` y el commit de git se hacen igual,
   para que quede constancia aunque el docente lo revise más tarde.

## Salidas

Por cada asignatura sin cambios: solo un mensaje corto, ningún archivo
tocado. Por cada asignatura con cambios: entrada nueva en su
`normativa_registro.md` + commit de git + aviso explícito al usuario. Si
se recorre más de una asignatura, además un resumen agregado final.

## Límites

Nunca actualiza `ficha.yaml`, ni ningún documento `APROBADO`, ni el
calendario del curso, a partir de lo que encuentre aquí — eso requiere
volver a ejecutar `/asig-normativa` o `/asig-programacion` con
confirmación explícita del docente, sobre la asignatura correspondiente.
No inventa un cambio para tener algo que reportar: si la búsqueda no es
concluyente, lo dice como tal ("no he podido confirmar si sigue vigente,
revisar manualmente") en vez de afirmar que no hay cambios. No comprueba
asignaturas que todavía no tienen `normativa_registro.md` — no hay nada
registrado que reverificar hasta que pasen por `/asig-normativa` al menos
una vez.

## Validación humana

No aplica para la propia comprobación (es de solo lectura). Sí es
obligatoria antes de que cualquier cambio detectado se aplique a
`ficha.yaml` o a documentos aprobados, vía los comandos correspondientes.
