---
name: asig-recursos
description: Genera, por trimestre completo, los recursos digitales de apoyo de todas las unidades reales de ese trimestre de la asignatura resuelta (sincronizado con ficha.yaml → unidades → trimestre). Presentación PowerPoint local es obligatoria para cada unidad; esquemas visuales, infografías, fichas interactivas, material de aula virtual y actividades gamificadas se generan cuando aportan valor real. Todo queda en BORRADOR, pendiente de aprobación vía /asig-revision — forma parte de "la fábrica" de generación de contenido junto a /asig-tema, /asig-tarea, /asig-unidad y /asig-examen. Úsalo cuando el usuario pida generar los recursos digitales de un trimestre o de una unidad concreta de la asignatura resuelta.
---

# /asig-recursos — Recursos digitales

## Rol

Parte de **"la fábrica"**: como `/asig-tema`, `/asig-tarea`, `/asig-unidad`
y `/asig-examen`, toma contenido ya generado/aprobado y produce material
nuevo, siempre en `BORRADOR`, siempre con `/asig-revision` como puerta de
salida antes de usarse con alumnado. La diferencia con las demás skills
de la fábrica (que se invocan unidad por unidad) es que esta **se
invoca por trimestre completo**: genera los recursos de todas las
unidades reales de ese trimestre en una sola pasada, resuelto contra
`ficha.yaml → unidades → trimestre`.

**El trimestre es un criterio de alcance y organización, no una
restricción temporal respecto a la fecha de hoy.** Es normal y esperado
generar los recursos de un trimestre antes de que empiece (p. ej.
preparar los recursos de UD00 en julio, antes de que el curso arranque
en septiembre) — nunca se bloquea la generación comparando con la fecha
actual.

## Entradas

- **Trimestre** (`1`, `2` o `3`), obligatorio. Si no se especifica,
  pregúntalo. También puede pedirse una única unidad ya identificada
  (p. ej. para regenerar sus recursos tras editar su contenido) sin
  repetir todo el trimestre — el trimestre sigue siendo el criterio de
  alcance, solo se reduce a una unidad concreta dentro de él.
- `ficha.yaml → unidades` de la asignatura resuelta (ver CLAUDE.md →
  "Cómo se resuelve la asignatura"), para resolver qué unidades reales
  pertenecen a ese trimestre.
- Por unidad: preferiblemente `05_UNIDADES/*APROBADO*.md` y/o
  `06_TEMARIO/VIGENTE/*APROBADO_DOCENTE.md`. Si solo existe en
  `BORRADOR`, se puede generar igualmente si el usuario lo pide
  explícitamente, avisando de que la fuente aún no está aprobada.

## Resolución de unidades por trimestre

1. Lee `ficha.yaml → unidades` y filtra las entradas con
   `trimestre == N`.
2. Excluye los bloques puros de evaluación/repaso/recuperación (no
   reciben `UD` numerada — mismo criterio que la regla 4 de
   `CLAUDE.md`).
3. Para cada unidad restante, calcula su `UD<NN>` según esa misma
   regla (posición entre las unidades docentes reales, con sufijo
   `a`/`b`/`c` para subdivisiones).
4. Si alguna unidad del trimestre no tiene fuente aprobada, avísalo
   explícitamente y pregunta si continuar con lo que haya en
   `BORRADOR` o esperar a que se apruebe primero.
5. **Presenta la lista de unidades resueltas y espera confirmación
   antes de generar nada** — es el alcance real de la ejecución.

## Tareas (por cada unidad del trimestre)

1. Genera la **presentación** (obligatoria — ver subsección propia).
2. Para cada uno de los otros cinco tipos, decide si aporta valor real
   para el contenido concreto de esa unidad (ver "Criterio de
   selección" abajo) y, si sí, genéralo; si no, dilo explícitamente y
   por qué, no lo generes por generar.
3. Guarda cada recurso en `BORRADOR`, en la subcarpeta de
   `09_RECURSOS_DIGITALES/` que corresponda a su tipo — nunca se
   mezcla contenido de distintos tipos en la misma carpeta.

## Criterio de selección de recursos opcionales

- **Esquemas** (mapa conceptual visual): si el contenido tiene una
  jerarquía clara (RA → bloques → conceptos) que se beneficia de una
  vista visual más allá del árbol de texto que ya genera `/asig-tema`.
- **Infografías**: si hay datos, cifras, protocolos o clasificaciones
  "citables" que resumen bien en una sola página.
- **Fichas interactivas**: si el contenido se presta a preguntas de
  repaso autoevaluables (definiciones, protocolos, clasificaciones).
- **Material de aula virtual**: casi siempre aporta valor (es el texto
  de presentación del tema para el LMS) — genéralo salvo indicación
  contraria explícita del docente.
- **Actividades gamificadas**: si hay suficientes hechos o protocolos
  discretos como para sostener un juego de preguntas con sentido.

## Nomenclatura

Sigue la regla general de `CLAUDE.md`
(`ASIGNATURA_TIPO_UD_CURSO_VERSION_ESTADO.ext`), donde `ASIGNATURA` es
el `<CODIGO>` de la asignatura resuelta (ver CLAUDE.md → "Cómo se
resuelve la asignatura"):

| Tipo de recurso | `TIPO` en el nombre | Carpeta |
|---|---|---|
| Presentación | `PRESENTACION` | `PRESENTACIONES/` |
| Esquema visual | `ESQUEMA_VISUAL` | `ESQUEMAS/` |
| Infografía | `INFOGRAFIA` | `INFOGRAFIAS/` |
| Ficha interactiva | `FICHA_INTERACTIVA` | `FICHAS_INTERACTIVAS/` |
| Material de aula virtual | `MATERIAL_AULA` | `MATERIAL_AULA_VIRTUAL/` |
| Actividad gamificada | `GAMIFICACION` | `ACTIVIDADES_GAMIFICADAS/` |

Ejemplo: `<CODIGO>_PRESENTACION_UD00_2026-2027_V01_BORRADOR.pptx` (p.
ej. `VCF_PRESENTACION_UD00_2026-2027_V01_BORRADOR.pptx` para VCF,
`MET_PRESENTACION_UD00_2026-2027_V01_BORRADOR.pptx` para MET).

**Nunca lee ni incluye nada de `10_DIVERSIDAD/INFORMES_ALUMNADO/`,
`10_DIVERSIDAD/PLANES_ADAPTACION/` ni
`11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/`** — los recursos digitales
son material curricular genérico, nunca datos reales de alumnado.

---

## Tipo de recurso: Presentación (obligatorio)

`.pptx` real generado localmente con `python-pptx` (entorno virtual
propio del proyecto, `.venv-recursos/`, fuera de git — ver
`.gitignore`; si no existe todavía: `python3 -m venv .venv-recursos &&
.venv-recursos/bin/pip install python-pptx`). No depende de ningún
servicio en la nube ni de ninguna suscripción.

**Toda presentación sigue el sistema de diseño "UD00 style"**, descrito
completo en
`.claude/skills/asig-recursos/reference/formdepor-pptx-ud00-style.md`:
naranja `#FF6A00` como acento dominante, fondo oscuro `#14161A` en
portada/separadores/cierre, fondo claro `#F2F3F5` en contenido,
tipografía Arial, formato 16:9 a 13,333×7,5 in. **Este sistema
sustituye, para las presentaciones de `/asig-recursos`, la guía de marca
FORMDEPOR azul/Aptos** (`reference/FORMDEPOR_especificaciones_tecnicas_powerpoint.md`)
— esa guía sigue siendo válida como referencia corporativa general para
otros documentos (es el contenido curricular del departamento en
general el que se trata como contenido de FORMDEPOR Formación, no algo
específico de una asignatura concreta), pero no es la que aplica aquí.

**El contenido fuente (DOCENTE, unidad) está escrito para leer, no como
guión de diapositivas** — convertirlo línea a línea produce
diapositivas fragmentadas e inútiles. Pero **no hay límite de
diapositivas**: el objetivo del esquema NO es resumir al mínimo, es
transformar el temario completo en formato proyectable. Apóyate en el
`DOCENTE` completo (no solo en el `RESUMEN`), y si un bloque tiene
mucho contenido real, repártelo en 2-3 diapositivas en vez de forzarlo
en una — más diapositivas con contenido genuino es preferible a menos
diapositivas demasiado densas o vacías de sustancia. El proceso tiene
dos pasos:

1. **Transforma tú mismo** el contenido de la unidad (partiendo del
   `DOCENTE`, no del `RESUMEN`) en un esquema nuevo: un Markdown con un
   `#` (título de portada) y varios `##` (uno por diapositiva). Es una
   transformación real de formato — de prosa para leer a guión visual
   para proyectar — no una poda agresiva: la meta es cubrir el temario
   con detalle, igual que harías tú si prepararas la presentación a
   mano. El script reconoce estas convenciones en el esquema (detalle
   completo y actualizado siempre en el docstring de
   `scripts/generar_pptx.py`, que es la fuente de verdad técnica):
   - `## RA<n> — Título` (o `## Separador: Título`) → separador oscuro
     con macroidentificador, numerado "BLOQUE X DE Y".
   - `## Cierre ...` → cierre oscuro con próximos pasos.
   - Sección con exactamente 3 viñetas `LETRA/Nº: texto` → protocolo de
     tres pasos con círculos (automático, colores naranja/rojo/negro).
   - Etiqueta `{recorrido}` / `{clasificacion}` / `{comparativa}` /
     `{reglaexcepciones}` al final del título de sección → patrones C,
     G/K, H y L respectivamente. **Elige la etiqueta a propósito según
     el contenido real de esa diapositiva** (una secuencia de pasos no
     es lo mismo que una taxonomía, y ambas son distintas de una
     comparación de dos conceptos) — sin etiqueta, cae en tarjetas
     genéricas, que es el patrón por defecto pero no siempre el más
     expresivo.
   - Línea `> texto` justo tras el título de sección → subtítulo/frase
     de contexto bajo la línea de acento.
   - Viñeta `- ! texto` → caja de cierre de diapositiva ("Idea clave",
     "Ojo"...) en vez de tarjeta.
   - Cada diapositiva de contenido lleva además un icono automático
     (formas nativas de PowerPoint, elegido por palabra clave del
     título — ver `ICONOS_POR_PALABRA_CLAVE` en el script).
   Guarda este esquema como
   `09_RECURSOS_DIGITALES/PRESENTACIONES/<CODIGO>_PRESENTACION_<UD>_<curso>_V01_BORRADOR_ESQUEMA.md`.
2. Conviértelo a `.pptx`:
   ```
   .venv-recursos/bin/python .claude/skills/asig-recursos/scripts/generar_pptx.py \
     --input "09_RECURSOS_DIGITALES/PRESENTACIONES/<CODIGO>_PRESENTACION_<UD>_<curso>_V01_BORRADOR_ESQUEMA.md" \
     --output "09_RECURSOS_DIGITALES/PRESENTACIONES/<CODIGO>_PRESENTACION_<UD>_<curso>_V01_BORRADOR.pptx" \
     --titulo "<título de portada, máx. 12 palabras>" \
     --etiqueta "<CODIGO> · <CICLO>" \
     --subtitulo "<curso o edición>" \
     --pie "<CODIGO> · <CICLO> · FORMDEPOR"
   ```
   `<CODIGO>` y `<CICLO>` son los de la asignatura resuelta (ver
   CLAUDE.md → "Cómo se resuelve la asignatura"). `--etiqueta`,
   `--subtitulo` y `--pie` son opcionales (el script cae en valores
   genéricos si se omiten), pero conviene pasarlos explícitos para que
   portada y pie de página identifiquen la asignatura correcta (p. ej.
   `--etiqueta "VCF · TSEAS"` y `--pie "VCF · TSEAS · FORMDEPOR"` para
   VCF; `--etiqueta "MET · TSEAS"` y `--pie "MET · TSEAS · FORMDEPOR"`
   para MET).
3. Informa de la ruta del `.pptx` y de cualquier aviso de estilo que
   imprima el script (título largo, cuerpo fuera del rango de
   palabras recomendado) — revísalos antes de dar la presentación por
   buena.

**Patrones del documento de diseño que el script NO implementa** (guía,
patrones B, E, I, M — cuadrícula 2×2 de cuatro bloques fijos,
bifurcación de decisión con resultados coloreados...): quedan para
maquetación manual en PowerPoint después, o para cuando exista una
plantilla maestra real. Los iconos son una aproximación con formas
nativas de PowerPoint, no un set de iconos real (no hay assets
disponibles); las fotografías reales tampoco se generan.

**Gamma** sigue disponible como mecanismo alternativo, solo si el
docente lo pide explícitamente para un concepto puntual (su suscripción
limita cuántas Gamma se pueden generar): usa `format: presentation`,
`textMode: preserve`, `language: es`, y guarda un registro en
`09_RECURSOS_DIGITALES/PRESENTACIONES/<CODIGO>_PRESENTACION_<UD>_<curso>_V01_BORRADOR_GAMMA.md`
con la URL generada (el contenido real vive en la cuenta de Gamma del
docente, no aquí — no se puede editar una Gamma existente desde este
comando).

---

## Tipo de recurso: Esquemas

Página HTML autocontenida (CSS embebido, sin dependencias externas ni
CDN) con el mapa conceptual visual de la unidad: jerarquía RA → bloques
→ conceptos, pensada para imprimir o proyectar como repaso rápido. Tú
(Claude) la autoras directamente como harías con un Artifact — no hay
script, porque cada mapa conceptual tiene una forma distinta y
generalizarlo mecánicamente perdería claridad. Aplica la paleta y
tipografía de `formdepor-pptx-ud00-style.md` (naranja de acento, fondo
claro, Arial), con buen contraste y diseño responsivo. Guarda como
`09_RECURSOS_DIGITALES/ESQUEMAS/<CODIGO>_ESQUEMA_VISUAL_<UD>_<curso>_V01_BORRADOR.html`.

## Tipo de recurso: Infografías

Página HTML autocontenida, formato póster de una sola pantalla/página
(pensada para imprimir en A4/A3), con los datos, cifras y puntos clave
más citables de la unidad. Mismo criterio de autoría directa y de
diseño que los esquemas. Guarda como
`09_RECURSOS_DIGITALES/INFOGRAFIAS/<CODIGO>_INFOGRAFIA_<UD>_<curso>_V01_BORRADOR.html`.

## Tipo de recurso: Fichas interactivas

Página HTML con JavaScript embebido (sin dependencias externas): tarjetas
que se giran para revelar la respuesta, autoevaluación de opción
múltiple con corrección inmediata, o similar, para que el alumnado
repase por su cuenta. Autoría directa, mismo sistema visual. Guarda
como
`09_RECURSOS_DIGITALES/FICHAS_INTERACTIVAS/<CODIGO>_FICHA_INTERACTIVA_<UD>_<curso>_V01_BORRADOR.html`.

## Tipo de recurso: Material de aula virtual

Markdown con el contenido de la unidad adaptado para copiar-pegar
directamente en una página/tema de Moodle o Google Classroom
(introducción, enlaces internos a los demás recursos ya generados de
esa unidad, estructura clara por sesión). Guarda como
`09_RECURSOS_DIGITALES/MATERIAL_AULA_VIRTUAL/<CODIGO>_MATERIAL_AULA_<UD>_<curso>_V01_BORRADOR.md`.

Si el docente pide explícitamente preparar fuentes para **NotebookLM**
(sin API/conector propio), genera además
`09_RECURSOS_DIGITALES/MATERIAL_AULA_VIRTUAL/<UD>/NOTEBOOKLM/`:

1. Copia ahí el temario `DOCENTE` y la unidad didáctica (Markdown).
   **No copies binarios de `06_TEMARIO/REFERENCIA_HISTORICA/`** (PDF,
   escaneos...) — ya están versionados en git y duplicarlos hace crecer
   el repositorio sin necesidad (pueden pesar decenas de MB).
2. Genera `INSTRUCCIONES.md` con: la lista exacta de archivos a subir
   a un notebook nuevo (los Markdown copiados + la ruta original de
   cada PDF histórico relevante), 2-3 sugerencias concretas de qué
   pedirle a NotebookLM que genere, y un checklist simple (crear
   notebook → subir fuentes → generar → revisar antes de compartir).

## Tipo de recurso: Actividades gamificadas

Markdown con un banco de preguntas o guion de juego (estilo
Kahoot/Quizizz: opción múltiple con respuesta correcta marcada; o un
guion de escape-room/gymkana con pistas ligadas a contenidos de la
unidad), listo para que el docente lo cargue a mano en la herramienta
de gamificación que use. Guarda como
`09_RECURSOS_DIGITALES/ACTIVIDADES_GAMIFICADAS/<CODIGO>_GAMIFICACION_<UD>_<curso>_V01_BORRADOR.md`.

---

## Cómo añadir un tipo de recurso nuevo

Añade una subsección nueva con este mismo patrón: nombre del tipo,
mecanismo de generación (script o autoría directa), nomenclatura,
carpeta de salida (`09_RECURSOS_DIGITALES/<NOMBRE>/`) y sus límites
propios. Añádelo también a la tabla de nomenclatura y al criterio de
selección. No hace falta tocar las demás subsecciones.

## Límites generales

No inventa contenido nuevo — parte siempre de una unidad ya generada,
nunca "desde cero" sin fuente. Nunca cruza datos de `10_DIVERSIDAD/` ni
de `CALIFICACIONES/`. Avisa explícitamente si la fuente usada está en
`BORRADOR` en vez de `APROBADO`. No genera un tipo de recurso opcional
solo por completar la lista — cada uno debe tener una justificación
real ligada al contenido de esa unidad concreta. El trimestre nunca se
usa como restricción temporal respecto a la fecha de hoy, solo como
criterio de alcance/organización via `ficha.yaml`.

## Validación humana

Todo lo generado queda en `BORRADOR`. `/asig-revision` es la puerta de
salida antes de que cualquier recurso se use con alumnado o se suba a
Drive/aula virtual — igual que con el resto de "la fábrica".
