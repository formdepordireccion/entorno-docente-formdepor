# Generalización de comandos a multi-asignatura (Fase 4 — escalado)

Fecha: 2026-07-28
Estado: Aprobado por el usuario, pendiente de implementación

## Contexto y alcance

El spec original del piloto
(`docs/superpowers/specs/2026-07-23-entorno-docente-vcf-piloto-design.md`)
cubría solo VCF/TSEAS y marcaba explícitamente "otras asignaturas del centro"
como Fase 4, fuera de su alcance. Ese momento ha llegado: el docente quiere
empezar a construir una segunda asignatura real, **METODOLOGÍA** (módulo
1143, "Metodología de la Enseñanza de Actividades Físico-Deportivas"), mismo
ciclo TSEAS que VCF.

Punto de partida de METODOLOGÍA: `3. METODOLOGÍA 25_26/`, con material del
curso 25/26 (temas en PDF/DOCX/PPTX, fichas de sesión, ítems de evaluación) y
un borrador de programación 2026-2027 ya bastante completo
(`1.Modulo_Profesional_Metodologia_Mario_Curso_2026-2027_programación.md`):
mismo RD 653/2017 y Decreto 106/2018 que VCF, Instrucción 13/2024 (96 horas,
3 semanales), 6 unidades de trabajo (UT0-UT5), calendario 2026/2027 y
criterios de calificación (40 % exámenes, 10 % presencia diaria, 50 %
trabajos) ya definidos.

Este spec cubre **generalizar la capa de comandos** (`.claude/skills/vcf-*/`
→ `.claude/skills/asig-*/`, 16 skills) y `CLAUDE.md` para que sirvan a
cualquier asignatura del departamento, no solo VCF. **No cubre** auditar de
verdad el material de METODOLOGÍA ni generar su programación/unidades/
temario reales — eso es trabajo posterior, una vez la capa de comandos esté
lista (ver "Fuera de alcance").

## Decisiones de diseño (resumen de la conversación de brainstorming)

1. **Generalizar ahora, no duplicar.** Con solo VCF como ejemplo se corría el
   riesgo de generalizar mal, pero el usuario prefirió afrontar el coste
   ahora en vez de acumular una tercera familia de comandos duplicada más
   adelante. Se acepta el riesgo de tocar el flujo de VCF (ya aprobado y en
   producción) como parte de este trabajo.
2. **Prefijo de comandos: `/asig-*`.** Sustituye a `/vcf-*` por completo (no
   coexisten). Ejemplos: `/asig-estado`, `/asig-unidad`, `/asig-tema`,
   `/asig-examen`.
3. **Selección de asignatura por lenguaje natural + código corto**, no por
   argumento posicional obligatorio. Si la referencia del usuario ("MET",
   "metodología", "el módulo 1143") resuelve a una única asignatura, el
   comando sigue; si es ambigua o no hay ninguna, pregunta antes de generar
   o tocar nada. Los comandos informativos (`/asig-estado`,
   `/asig-mantenimiento`) sin asignatura especificada recorren todas por
   defecto.
4. **Normativa sin nivel compartido.** Aunque VCF y METODOLOGÍA comparten
   literalmente el mismo RD/Decreto/Instrucción, METODOLOGÍA verifica su
   propia normativa de forma independiente en su propio
   `normativa_registro.md`. No se introduce un nivel "ciclo" nuevo en el
   modelo de datos ni se toca el `normativa_registro.md` ya aprobado de VCF.
5. **Alcance: las 16 skills de una vez**, no solo el núcleo de generación de
   contenido. Se generalizan también `/asig-drive`, `/asig-calendar-sync`,
   `/asig-vigilancia`, `/asig-mantenimiento`, `/asig-diversidad`,
   `/asig-recursos` y `/asig-analitica` aunque no vayan a usarse de
   inmediato para METODOLOGÍA.
6. **Cero cambios sobre contenido ya generado/aprobado.** Nada dentro de
   `DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/` cambia — ni contenido, ni
   nombres de archivo, ni su `ficha.yaml`. El token `ASIGNATURA` de la
   nomenclatura de archivo (`ASIGNATURA_TIPO_UD_CURSO_VERSION_ESTADO.ext`)
   ya era genérico (`VCF`, y ahora también `MET`); ese formato no cambia.

## Arquitectura

### Estructura de carpetas

```text
DEPARTAMENTO_DOCENTE/
├── CLAUDE.md                    # generalizado, ya no habla solo de VCF
├── 00_CENTRO_CONTROL/
└── ASIGNATURAS/
    ├── VCF_TSEAS/                # sin cambios de ningún tipo
    └── MET_TSEAS/                # nueva, mismas 15 carpetas que VCF_TSEAS
        ├── 00_FICHA/ficha.yaml
        ├── 01_NORMATIVA_CURRICULO/
        ├── 02_PROGRAMACION/
        ├── 03_MAPA_CURRICULAR/
        ├── 04_TEMPORALIZACION/
        ├── 05_UNIDADES/
        ├── 06_TEMARIO/{VIGENTE,REFERENCIA_HISTORICA}/
        ├── 07_ACTIVIDADES_TAREAS/{VIGENTE,REFERENCIA_HISTORICA}/
        ├── 08_EVALUACION/
        ├── 09_RECURSOS_DIGITALES/
        ├── 10_DIVERSIDAD/
        ├── 11_SEGUIMIENTO_RESULTADOS/
        ├── 12_RECUPERACION/
        ├── 13_MEMORIA_FINAL/
        └── 14_HISTORICO_CAMBIOS/
```

Código corto de METODOLOGÍA: **`MET`**. Carpeta: **`MET_TSEAS`** (mismo
patrón `<CODIGO>_<CICLO>` que VCF_TSEAS). La creación real de `MET_TSEAS/`
con sus 15 carpetas y `ficha.yaml` inicial (campos a `null`/`[]`, igual que
arrancó VCF) es parte del plan de implementación, no de este documento.

### Mecanismo de resolución de asignatura

Cada `ASIGNATURAS/*/00_FICHA/ficha.yaml` debe tener `asignatura.codigo`
(p. ej. `MET`) y `asignatura.nombre` (p. ej. "Metodología de la Enseñanza de
Actividades Físico-Deportivas"). Regla común a todas las `/asig-*`:

1. Recorre `ASIGNATURAS/*/00_FICHA/ficha.yaml` y compara la referencia en
   lenguaje natural del usuario contra `codigo` (coincidencia exacta o de
   prefijo, insensible a mayúsculas) y `nombre` (coincidencia de
   subcadena, insensible a mayúsculas/acentos).
2. Si resuelve a exactamente una asignatura → sigue con esa.
3. Si resuelve a cero o a más de una → pregunta explícitamente antes de
   generar, modificar o aprobar nada. Nunca asume "la primera" ni "la más
   reciente".
4. Excepción: comandos de solo lectura/informe (`/asig-estado`,
   `/asig-mantenimiento`, `/asig-vigilancia` en su verificación normativa)
   sin ninguna asignatura mencionada recorren **todas** las que existan,
   igual que ya hace hoy el modo resumen semanal de `/vcf-estado`.

### `CLAUDE.md` generalizado

Dos bloques, sustituyendo al `CLAUDE.md` actual (centrado en VCF):

- **Reglas fijas** (las 8 actuales): se reescriben como reglas de
  departamento, sin mención a VCF salvo como ejemplo puntual entre
  paréntesis donde aporte claridad.
- **"Dónde está todo"**: describe el patrón `ASIGNATURAS/<CODIGO>_<CICLO>/`
  en vez de apuntar solo a VCF_TSEAS, y mantiene una lista corta de las
  asignaturas activas (hoy: VCF, MET) con una frase cada una — se actualiza
  cada vez que se añade una asignatura nueva.
- El título del documento y su primer párrafo dejan de decir "... / VCF" y
  pasan a describir el departamento en general.

### Las 16 skills a generalizar

`.claude/skills/vcf-<nombre>/` → `.claude/skills/asig-<nombre>/` para las
16: `estado`, `normativa`, `auditoria`, `programacion`, `unidad`, `tema`,
`tarea`, `examen`, `revision`, `drive`, `calendar-sync`, `vigilancia`,
`diversidad`, `recursos`, `analitica`, `mantenimiento`.

En cada una, el rol y la lógica interna no cambian — solo la resolución de
ruta: cualquier mención literal a `VCF_TSEAS` o a una ruta fija se sustituye
por "la carpeta de la asignatura resuelta según el mecanismo de arriba".
Casos concretos a vigilar durante la migración:

- `vcf-estado` ya quedó parcialmente generalizado hoy mismo (su modo
  resumen semanal ya recorre `ASIGNATURAS/*/`) — al pasar a `asig-estado`
  hay que generalizar también su modo de informe completo bajo demanda, que
  todavía asume una sola asignatura en algunos puntos.
- `vcf-recursos/reference/FORMDEPOR_especificaciones_tecnicas_powerpoint.md`
  y `vcf-recursos/scripts/generar_pptx.py` no son específicos de VCF (son
  el sistema de marca FORMDEPOR y el motor de generación, ya genéricos) —
  solo cambian de carpeta contenedora.
- `vcf-revision` lista otras skills por nombre en su propio texto (menciona
  `/vcf-unidad`, `/vcf-tema`, etc.) — esas referencias cruzadas hay que
  actualizarlas también.
- `vcf-mantenimiento` dispara otras skills por nombre — mismo caso.

### Normativa: sin nivel compartido

METODOLOGÍA verifica su propio RD 653/2017 + Decreto 106/2018 + Instrucción
13/2024 de forma independiente, en su propio `normativa_registro.md`, sin
referenciar ni depender del de VCF. Es trabajo duplicado a sabiendas (barato:
un par de verificaciones con WebSearch/WebFetch), a cambio de no introducir
una entidad "ciclo" nueva en el modelo de datos ni tocar el
`normativa_registro.md` ya aprobado de VCF.

## Efectos secundarios a corregir

Dos eventos recurrentes de Google Calendar creados en esta misma sesión
mencionan los nombres de comando antiguos en su descripción:

- "VCF · Mantenimiento quincenal (/vcf-mantenimiento)"
- "VCF · Resumen semanal (/vcf-estado)"

Como parte del plan, hay que actualizar la descripción (no necesariamente el
título, que ya es específico de VCF por diseño — el mantenimiento y el
resumen semanal seguirán siendo por asignatura o multi-asignatura según el
caso) de ambos eventos para que citen `/asig-mantenimiento` y
`/asig-estado`.

## Riesgos y mitigación

- **Riesgo principal: romper el flujo de VCF, ya aprobado y en producción.**
  Mitigación: ningún archivo dentro de `ASIGNATURAS/VCF_TSEAS/` se toca; solo
  se renombran/reescriben las skills y `CLAUDE.md`. Tras la migración, hay
  que ejecutar `/asig-estado` sobre VCF (equivalente al `/vcf-estado`
  completo de hoy) y comparar que el resultado es coherente con el estado
  real del proyecto, como prueba de humo mínima antes de dar la migración
  por buena.
- **Riesgo: referencias cruzadas rotas** (una skill que menciona a otra por
  su nombre antiguo `/vcf-*`). Mitigación: grep de `vcf-` sobre
  `.claude/skills/asig-*/` y `CLAUDE.md` al final de la migración; cero
  resultados esperados salvo menciones históricas explícitas (p. ej. "esto
  sustituye a `/vcf-estado`").

## Fuera de alcance (siguiente paso, no parte de este plan)

- **Poblar `MET_TSEAS/` con contenido real.** El plan sí crea el esqueleto
  vacío (15 carpetas + `ficha.yaml` inicial con campos a `null`/`[]`, igual
  que arrancó VCF) porque hace falta para probar que las skills
  generalizadas funcionan de verdad sobre una segunda asignatura. Lo que
  queda fuera es todo lo que llenaría ese esqueleto: auditar
  `3. METODOLOGÍA 25_26/` con `/asig-auditoria`, verificar su normativa con
  `/asig-normativa`, generar programación/calendario/unidades/temario
  reales — cada uno de esos pasos requiere su propia revisión con el
  docente y no tiene sentido meterlo en el mismo plan que la migración de
  las skills.
- Cualquier generalización de nivel "ciclo" compartido (normativa u otro
  dato común entre asignaturas del mismo ciclo) — descartada explícitamente
  en la decisión 4.
- Añadir asignaturas más allá de VCF y METODOLOGÍA.

## Siguiente paso

Invocar la skill `writing-plans` para convertir este diseño en un plan de
implementación paso a paso.
