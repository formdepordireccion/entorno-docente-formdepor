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
- Programación docente real, si existe: `02_PROGRAMACION/programacion_26_27.md`
  y cualquier borrador migrado a `02_PROGRAMACION/REFERENCIA_HISTORICA/`
  (por `/vcf-auditoria`) — ver "Orden de prioridad de fuentes" más abajo.

## Orden de prioridad de fuentes

La normativa oficial (RD estatal, decreto/instrucciones autonómicas) es la
referencia legal, pero no siempre es la fuente más completa o actualizada
para datos operativos concretos (horario real, horas totales asignadas,
organización específica de contenidos): esos datos a menudo solo constan
en instrucciones administrativas posteriores o en la propia programación
aprobada por el centro, que el RD/decreto no siempre reflejan (p. ej. el
RD marca solo un mínimo de horas).

Por eso, para **horario, horas totales/semanales, y el desarrollo/detalle
de contenidos**, esta tarea da prioridad a lo que diga la programación
docente real (`02_PROGRAMACION/programacion_26_27.md` o su borrador en
`02_PROGRAMACION/REFERENCIA_HISTORICA/`) sobre lo que diga la normativa
"vigente" que esta tarea localiza por su cuenta — **salvo que el dato de
la programación sea un error demasiado notorio**, entendiendo por tal
cualquiera de estos casos:

- Horas por debajo del mínimo legal que fija el RD estatal para el módulo.
- Un resultado de aprendizaje (RA) que la programación omite por completo
  respecto a los que fija el RD, o uno que no existe en el RD.
- Un bloque de contenidos obligatorio del RD ausente por completo en la
  programación (no basta con que esté reorganizado o más detallado).

Si la programación cita ella misma una fuente oficial adicional (p. ej.
una instrucción autonómica posterior al decreto, como una instrucción
sobre aspectos organizativos del currículo) que confirma su dato, verifica
esa fuente con WebSearch igual que el RD/decreto — si se confirma, es la
mejor fuente disponible y así se registra en `normativa_registro.md`,
citada igual que el RD/decreto, no como "según la programación" a secas.

En caso de error notorio, no se adopta el dato de la programación
silenciosamente: se registra la discrepancia en `ficha.yaml` (con el
mismo patrón `confirmado_*: false` + `nota` ya usado) y se avisa al
usuario explícitamente, en vez de decidir por él.

Los resultados de aprendizaje y sus criterios de evaluación, al ser texto
legal fijado por el RD, se registran siempre con el texto del RD como
base — si la programación los redacta de otra forma sin cambiar el
contenido legal, se puede anotar la redacción de la programación como
referencia adicional, pero el texto que queda en `ficha.yaml` es el del
RD.

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
4. Si existe una programación docente real (ver Entradas), léela y
   aplica el "Orden de prioridad de fuentes" de arriba para horario,
   horas totales/semanales y desarrollo de contenidos: verifica con
   WebSearch cualquier fuente adicional que la programación cite, y usa
   el resultado (programación+fuente verificada, o el aviso de
   discrepancia si hay error notorio) en vez de quedarte solo con el
   mínimo del RD/decreto.
5. Escribe `01_NORMATIVA_CURRICULO/normativa_registro.md` con, para cada
   norma encontrada: título de la norma, URL fuente, fecha de publicación,
   fecha de consulta de hoy, y artículos/anexos relevantes citados
   literalmente.
6. Actualiza `ficha.yaml`:
   - `normativa.rd_estatal`: identificador y URL del RD.
   - `normativa.decreto_curriculo_autonomico`: identificador y URL del
     decreto de Extremadura.
   - `resultados_aprendizaje`, `criterios_evaluacion`, `contenidos`: listas
     extraídas de la norma (texto literal o resumen fiel, citando el
     artículo de origen).
   - `asignatura.horas_totales`, `asignatura.horas_semanales`: según el
     orden de prioridad de fuentes de arriba.
   - `estado` permanece en `borrador`.
7. Genera `03_MAPA_CURRICULAR/matriz_alineacion.md`: una tabla que cruza
   cada resultado de aprendizaje con sus criterios de evaluación y
   contenidos asociados.
8. Presenta un resumen al usuario y pide confirmación explícita antes de
   que cualquier otro comando trate estos datos como definitivos.

## Salidas

`normativa_registro.md`, `matriz_alineacion.md`, `ficha.yaml` actualizado.

## Límites

No marca `ficha.yaml.estado` como `aprobado`. Si no encuentra la norma
exacta o algún dato no puede verificarse, lo dice explícitamente ("no he
podido confirmar X, pendiente de verificación manual") en vez de inventar
artículos, fechas u horas. Dar prioridad a la programación real no exime
de verificar sus fuentes citadas ni de avisar de errores notorios — nunca
se adopta un dato de la programación sin más si contradice claramente el
mínimo legal.

## Validación humana

Obligatoria: el docente debe confirmar que el RD y el decreto localizados
son los correctos antes de que `/vcf-programacion`, `/vcf-unidad`, `/vcf-tema`
o `/vcf-examen` usen estos datos.
