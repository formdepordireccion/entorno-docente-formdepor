---
name: vcf-recursos
description: Genera recursos digitales (presentaciones vía Gamma, paquetes de fuentes preparados para NotebookLM) a partir de las unidades y temario ya generados de VCF. Diseñado para añadir más plataformas en el futuro sin rediseñar nada. Úsalo cuando el usuario pida una presentación, un recurso de NotebookLM, o cualquier material digital derivado de una unidad de VCF.
---

# /vcf-recursos — Recursos digitales (VCF/TSEAS)

## Rol

Genera recursos digitales a partir del contenido ya producido (unidades,
temario) para una o varias plataformas externas. Cada plataforma es una
subsección independiente de este documento — añadir una plataforma nueva
no debe requerir tocar las demás.

## Entradas

- La unidad o tema para el que se pide el recurso: preferiblemente
  `05_UNIDADES/*APROBADO*.md` y/o
  `06_TEMARIO/VIGENTE/*APROBADO_DOCENTE.md`. Si solo existe en
  `BORRADOR`, se puede generar igualmente si el usuario lo pide
  explícitamente, pero avisando de que la fuente aún no está aprobada.
- `ficha.yaml` (para RA/criterios de contexto si hace falta).

## Salida y organización de carpetas

`09_RECURSOS_DIGITALES/<PLATAFORMA>/` — una subcarpeta por plataforma,
con un archivo de registro por unidad dentro. Nunca se mezcla contenido
de distintas plataformas en la misma carpeta.

**Nunca lee ni incluye nada de `10_DIVERSIDAD/INFORMES_ALUMNADO/` ni
`10_DIVERSIDAD/PLANES_ADAPTACION/`** — los recursos digitales son
material curricular, no deben cruzarse con datos de alumnado real.

---

## Plataforma: Gamma (automatizada)

Conector MCP disponible — se puede generar directamente.

1. Toma el contenido de la unidad/tema fuente (texto completo, no
   resumido salvo que el usuario pida un resumen).
2. Llama a la generación de Gamma con `format: presentation`,
   `textMode: preserve` si el contenido fuente ya está bien
   estructurado en secciones (lo habitual viniendo de `/vcf-unidad` o
   `/vcf-tema`), `language: es`, y `textOptions.audience`: "alumnado de
   Formación Profesional, Grado Superior" salvo que el usuario indique
   otra cosa.
3. No elijas tema visual (`themeId`) salvo que el usuario pida un estilo
   concreto — deja el valor por defecto.
4. Guarda un archivo de registro en
   `09_RECURSOS_DIGITALES/GAMMA/<UD>_presentacion.md` con: la URL de la
   Gamma generada (`gammaUrl`), fecha, unidad/fuente usada, y una nota de
   que las ediciones posteriores se hacen en el propio editor de Gamma
   (esta herramienta no puede editar una Gamma ya creada).
5. Comparte la URL con el usuario.

**Límites de esta plataforma:** el contenido real de la presentación vive
en la cuenta de Gamma del usuario, no en este repositorio — el archivo de
registro es solo un puntero. No se puede regenerar/editar una Gamma
existente desde aquí, solo crear una nueva.

---

## Plataforma: NotebookLM (preparación manual, sin API)

NotebookLM no tiene conector MCP ni API pública disponible — este comando
no puede subir nada automáticamente. En su lugar, prepara todo lo
necesario para que el docente lo suba él mismo en un par de clics.

1. Identifica las fuentes relevantes para la unidad/tema pedido: el
   documento `DOCENTE` del temario, la unidad didáctica, y (si existe y
   aporta valor) el material de `06_TEMARIO/REFERENCIA_HISTORICA/`
   relacionado.
2. Copia esas fuentes (no las muevas) a
   `09_RECURSOS_DIGITALES/NOTEBOOKLM/<UD>/`.
3. Genera `09_RECURSOS_DIGITALES/NOTEBOOKLM/<UD>/INSTRUCCIONES.md` con:
   - Lista exacta de archivos a subir a un notebook nuevo en
     notebooklm.google.com.
   - 2-3 sugerencias concretas de qué pedirle a NotebookLM que genere
     (p. ej. "guía de estudio", "resumen de audio", "preguntas
     frecuentes para repaso de examen"), adaptadas al contenido de esa
     unidad.
   - Un checklist simple para el docente (crear notebook → subir fuentes
     → generar → revisar antes de compartir con alumnado).

**Límites de esta plataforma:** nada se sube automáticamente; el docente
completa el último paso a mano. Si en el futuro NotebookLM publica una
API/MCP, esta subsección es la que habría que actualizar para
automatizarla — el resto del comando no cambiaría.

---

## Cómo añadir una plataforma nueva

Añade aquí una subsección nueva con este mismo patrón: nombre de la
plataforma, si es automatizada o manual, pasos concretos, dónde vive la
salida (`09_RECURSOS_DIGITALES/<NOMBRE_PLATAFORMA>/`), y sus límites
propios. No hace falta tocar las demás subsecciones ni el resto del
comando.

## Límites generales

No inventa contenido nuevo — parte siempre de una unidad/tema ya
generado, nunca genera un recurso "desde cero" sin fuente. Nunca cruza
datos de `10_DIVERSIDAD/`. Avisa explícitamente si la fuente usada está
en `BORRADOR` en vez de `APROBADO`.

## Validación humana

El docente elige la unidad y la plataforma antes de generar; revisa el
resultado (URL de Gamma, o el paquete de NotebookLM) después.
