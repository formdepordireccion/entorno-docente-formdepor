---
name: formdepor-pptx-ud00-style
description: >
  Sistema de diseño para generar presentaciones PowerPoint educativas con la
  estética visual de la presentación UD00: alto contraste, estructura modular,
  jerarquía tipográfica clara, color naranja como acento y alternancia de
  diapositivas claras y oscuras.
version: "1.0"
language: es
output_format: pptx
aspect_ratio: "16:9"
reference_deck: "UD00_presentacion.pptx"
---

# Skill de diseño PowerPoint — Sistema visual UD00

## 1. Finalidad

Esta skill define las reglas técnicas necesarias para reproducir, extender y
sistematizar el lenguaje visual de la presentación de referencia
`UD00_presentacion.pptx`.

Debe utilizarse para:

- unidades didácticas;
- presentaciones de aula;
- introducciones de módulos;
- secuencias formativas;
- presentaciones institucionales de carácter educativo;
- resúmenes, itinerarios, protocolos, procesos y cierres de unidad.

El objetivo no es copiar cada diapositiva literalmente, sino conservar un
**sistema visual coherente, modular y reconocible**.

---

# 2. Parámetros del documento

## 2.1. Formato

| Propiedad | Valor |
|---|---:|
| Proporción | 16:9 panorámica |
| Anchura PowerPoint | 13,333 in |
| Altura PowerPoint | 7,500 in |
| Anchura EMU | 12.192.000 |
| Altura EMU | 6.858.000 |
| Orientación | Horizontal |
| Área segura exterior | 0,50–0,75 in |
| Retícula principal | 12 columnas conceptuales |
| Unidad de separación horizontal | 0,15–0,25 in |
| Separación entre módulos | 0,15–0,30 in |

## 2.2. Resolución recomendada de recursos

- Fotografías de fondo: mínimo 1920 × 1080 px.
- Iconos: preferentemente SVG.
- Logos: SVG o PNG transparente de mínimo 1000 px de anchura.
- Capturas o diagramas: mínimo 1600 px de anchura.
- Exportación final: PDF de alta calidad y PPTX editable.

## 2.3. Márgenes estructurales

Usar como referencias:

- margen izquierdo habitual: **0,50–0,75 in**;
- margen derecho habitual: **0,50–0,75 in**;
- margen superior de contenido: **0,30 in**;
- inicio de bloques principales: **2,58–3,05 in**;
- pie de página: entre **6,95 y 7,25 in**;
- ancho útil máximo de contenido: **11,83 in**.

No situar texto esencial a menos de 0,40 in de los bordes.

---

# 3. Paleta cromática

## 3.1. Colores principales

| Token | Hex | Uso |
|---|---|---|
| `brand-orange` | `#FF6A00` | Acento principal, números, títulos secundarios, líneas y tarjetas |
| `ink-black` | `#14161A` | Fondos oscuros, tarjetas de alto contraste, texto muy oscuro |
| `ink-raised` | `#1E2229` | Tarjetas oscuras secundarias |
| `paper-light` | `#F2F3F5` | Fondo general de diapositivas claras |
| `white` | `#FFFFFF` | Texto sobre fondo oscuro |
| `charcoal` | `#2B2F36` | Texto principal sobre fondo claro |
| `slate` | `#4A5058` | Texto secundario |
| `muted-gray` | `#6C757D` | Tercer color estructural |
| `soft-gray` | `#B9BEC6` | Etiquetas y metadatos |
| `line-gray` | `#D8DBDF` | Separadores suaves |
| `alert-red` | `#E63946` | Riesgo, alerta, respuesta negativa |
| `cyan` | `#00A8B5` | Estado positivo o bloque complementario |
| `warning-yellow` | `#FFB300` | Advertencia o tercera categoría |
| `orange-pale` | `#FFF1E6` | Fondo suave asociado al naranja |
| `red-pale` | `#FFE9EB` | Fondo suave asociado al rojo |
| `cyan-pale` | `#E8FBFD` | Fondo suave asociado al cian |

## 3.2. Proporción de uso

Aplicar aproximadamente:

- 60–70 %: fondos neutros claros u oscuros;
- 15–20 %: negro, gris o blanco para estructura;
- 8–12 %: naranja corporativo;
- máximo 5–8 %: colores semánticos secundarios.

El naranja debe ser el color de identidad dominante. El rojo, cian y amarillo
solo deben emplearse cuando exista una codificación semántica real.

## 3.3. Contraste

- Texto blanco sobre `#14161A`: permitido.
- Texto blanco sobre `#FF6A00`: permitido para texto breve y en negrita.
- Texto oscuro sobre `#F2F3F5`: recomendado.
- No usar texto gris claro sobre blanco.
- Mantener contraste mínimo WCAG AA siempre que sea posible.
- En proyección, evitar cuerpos inferiores a 14 pt.

---

# 4. Tipografía

## 4.1. Familia

La presentación combina tipografía de sistema con predominio de **Arial** y
elementos heredados del tema Office.

Para replicar el resultado con estabilidad:

```text
Tipografía principal: Arial
Alternativa compatible: Aptos
Fallback: Calibri, Helvetica, sans-serif
```

No mezclar más de una familia tipográfica visible en la misma presentación.

## 4.2. Jerarquía tipográfica

| Nivel | Tamaño orientativo | Peso | Uso |
|---|---:|---|---|
| Macroidentificador | 120 pt | Bold | RA7, RA8, RA9 |
| Título de portada | 34–44 pt | Bold | Título principal |
| Título de diapositiva | 32–36 pt | Bold | Encabezado superior |
| Título de sección | 28–34 pt | Bold | Separadores de bloque |
| Título de tarjeta | 17–22 pt | Bold | Categoría o concepto |
| Subtítulo | 16–19 pt | Regular/Bold | Explicación inmediata |
| Cuerpo | 14–16 pt | Regular | Texto general |
| Cuerpo compacto | 13–14 pt | Regular | Listas breves |
| Etiqueta | 12–14 pt | Bold, mayúsculas | Bloque, recorrido, próxima sesión |
| Pie y metadatos | 8–10 pt | Regular/Bold | Marca, módulo, número |

## 4.3. Reglas de composición textual

- Interlineado: 0,95–1,10.
- Espacio posterior entre párrafos: 4–8 pt.
- Evitar párrafos superiores a 3 líneas.
- Máximo recomendado: 35–45 palabras por módulo.
- Títulos: alineación izquierda.
- Números dentro de círculos: alineación centrada.
- Etiquetas: mayúsculas, tracking visual amplio.
- Evitar justificación completa.
- No usar subrayado.
- Usar negrita para conceptos, no para párrafos completos.
- Las frases clave pueden resaltarse en naranja dentro de una línea de texto.

---

# 5. Retícula y geometría

## 5.1. Estructura base de diapositiva clara

```text
+-------------------------------------------------------------+
| título                                    icono contextual  |
| — línea naranja                                              |
| subtítulo                                                    |
|                                                               |
|                 área modular de contenido                    |
|                                                               |
| — línea inferior                                             |
| marca / programa                                    número   |
+-------------------------------------------------------------+
```

Medidas orientativas:

- título: x 0,50; y 0,30; ancho 9,00 in;
- icono: x 11,47–11,75; y 0,67–0,78; tamaño 0,75–1,11 in;
- subtítulo: inicio aproximado y 1,50–1,75 in;
- línea de acento superior: x 0,75; y 1,45–1,65; ancho 0,65–0,95 in;
- área principal: y 2,58–6,30 in;
- pie: y 7,00 in;
- número: esquina inferior derecha.

## 5.2. Estructura base de diapositiva oscura

```text
+-------------------------------------------------------------+
|                                                               |
| etiqueta de bloque                                           |
|                                                               |
| RA#                  | título de sección                    |
|                      | subtítulo / alcance                   |
|                                                               |
| — línea inferior                                             |
| marca / programa                                    número   |
+-------------------------------------------------------------+
```

Medidas orientativas:

- fondo: `#14161A`;
- macroidentificador: x 0,75; y 2,72; ancho 4,44 in;
- etiqueta: x 0,75; y 2,19; ancho 5,56 in;
- divisor vertical: x aproximada 5,50–5,75 in;
- título de sección: x 5,97; y 2,78; ancho 6,61 in;
- línea inferior naranja: x 0,75; y 6,85–7,00; ancho 4,00 in;
- texto principal blanco;
- texto auxiliar gris claro;
- acento naranja.

## 5.3. Sistema de columnas

Patrones recurrentes:

- 2 columnas: 5,0–5,8 in por columna;
- 3 columnas: 3,83 in por columna;
- 4 columnas: 2,83 in por columna;
- separación nominal: 0,17 in;
- inicio de columnas frecuentes: 0,75 / 4,75 / 8,75 in;
- para cuatro columnas: 0,75 / 3,75 / 6,75 / 9,75 in.

## 5.4. Alineación

- Los módulos deben compartir bordes superiores e inferiores.
- Los títulos de tarjetas deben partir de la misma coordenada vertical.
- Los círculos numerados se alinean con el comienzo del texto asociado.
- Las líneas de color superior funcionan como anclaje de columna.
- La línea inferior y el pie deben mantenerse constantes en toda la serie.

---

# 6. Fondos

## 6.1. Fondo claro

Color base:

```text
#F2F3F5
```

Características:

- apariencia ligeramente fría;
- mejor que blanco puro para proyección;
- permite tarjetas blancas o gris muy claro;
- mantiene contraste con naranja y negro.

## 6.2. Fondo oscuro

Color base:

```text
#14161A
```

Usar en:

- portada;
- separadores de bloque;
- cierre;
- diapositivas de impacto;
- mensajes que necesiten transición visual.

No usar más de dos o tres diapositivas oscuras consecutivas salvo en una
sección deliberadamente narrativa.

## 6.3. Alternancia recomendada

Secuencia orientativa:

1. portada oscura;
2. índice o bienvenida clara;
3. contextualización clara;
4. separador oscuro;
5. 3–5 diapositivas claras;
6. separador oscuro;
7. nuevo bloque claro;
8. cierre oscuro.

---

# 7. Componentes visuales

## 7.1. Línea de acento

- color: `#FF6A00`;
- grosor visual: 2–4 pt;
- anchura habitual: 0,65–0,95 in en cabecera;
- anchura: 4,0–5,5 in en pie o portada;
- extremos rectos;
- no usar degradado.

## 7.2. Tarjetas

### Tarjeta clara

- fondo: blanco o `#F2F3F5`;
- radio de esquina: 0,12–0,20 in;
- sin sombra o sombra extremadamente sutil;
- padding interior: 0,22–0,35 in.

### Tarjeta de color

- fondo: naranja, negro, gris, rojo o cian;
- texto: blanco;
- radio: 0,18–0,25 in;
- usar para clasificar, no solo para decorar.

### Banda horizontal

- altura: 0,61–1,11 in;
- ancho habitual: 11,83 in;
- color oscuro o semántico;
- texto centrado o alineado a la izquierda;
- radio suave.

## 7.3. Círculos numerados

- diámetro: 0,53–0,61 in;
- color principal: naranja;
- número: blanco;
- peso: Bold;
- tamaño: 14–18 pt;
- alineación perfecta vertical y horizontal.

## 7.4. Macroidentificador RA

- texto: RA7, RA8, RA9 o equivalente;
- tamaño: 100–120 pt;
- peso: Bold;
- color: naranja;
- no incluir contorno;
- ubicar a la izquierda del separador vertical.

## 7.5. Flechas de proceso

- tres bloques consecutivos;
- misma altura;
- colores: naranja — negro — gris;
- título blanco en negrita;
- descripción breve;
- usar solo para procesos ordenados o recorridos.

## 7.6. Iconografía

Características:

- estilo lineal;
- trazo simple y uniforme;
- sin relleno complejo;
- color naranja, rojo o cian;
- iconos pequeños en la esquina superior derecha;
- tamaño habitual: 0,75 in;
- tamaño máximo para icono protagonista: 1,94 in;
- usar un solo icono contextual por diapositiva.

Ejemplos del sistema:

- salud;
- emergencia;
- teléfono;
- botiquín;
- balanza;
- estetoscopio;
- pulso;
- riesgo;
- movilidad;
- checklist.

## 7.7. Pie de página

Contenido:

```text
[PROGRAMA / MÓDULO] · [CICLO] · FORMDEPOR                     [N.º]
```

Especificaciones:

- tamaño: 8–9 pt;
- mayúsculas;
- color gris sobre fondo claro;
- color gris claro sobre fondo oscuro;
- número en naranja;
- mantener exactamente la misma posición;
- no introducir logos grandes en el pie.

---

# 8. Patrones de diapositiva

## Patrón A — Portada

### Objetivo
Presentar unidad, materia y periodo.

### Composición
- fondo oscuro;
- título grande a la izquierda;
- etiqueta superior en naranja;
- subtítulo institucional en naranja;
- icono protagonista dentro de tarjeta oscura;
- líneas naranjas decorativas;
- pie mínimo.

### Restricciones
- máximo 12 palabras en el título;
- máximo 2 líneas en subtítulo;
- no usar más de un icono;
- no incluir listas.

---

## Patrón B — Bienvenida / resumen 2 × 2

### Objetivo
Introducir resultados, objetivo, calendario y cierre.

### Composición
- fondo claro;
- cuatro tarjetas;
- dos columnas y dos filas;
- círculo naranja numerado;
- título corto y explicación;
- icono contextual en cabecera.

### Medidas orientativas
- círculos: 0,58 in;
- tarjetas: aproximadamente 5,0 × 1,3 in;
- primera columna: x 1,05–6,00 in;
- segunda columna: x 7,05–12,00 in.

---

## Patrón C — Recorrido de unidad

### Objetivo
Representar secuencia o mapa del contenido.

### Composición
- título superior;
- texto contextual;
- etiqueta pequeña;
- tres flechas;
- naranja para el bloque activo o inicial;
- negro para el bloque central;
- gris para el bloque final.

### Restricciones
- máximo tres o cuatro etapas;
- máximo 8 palabras por etapa;
- mantener orden visual inequívoco.

---

## Patrón D — Separador de bloque

### Objetivo
Marcar un cambio de resultado de aprendizaje o sección.

### Composición
- fondo oscuro;
- macroidentificador RA;
- línea vertical naranja;
- título de sección;
- subtítulo descriptivo;
- etiqueta “BLOQUE X DE Y”.

### Uso
Introducir cada bloque principal, nunca contenido denso.

---

## Patrón E — Tres tarjetas categóricas

### Objetivo
Comparar tres conceptos equivalentes.

### Composición
- tres tarjetas de 3,83 in;
- colores naranja, negro y gris;
- título en mayúsculas;
- definición;
- ejemplo breve;
- banda inferior de idea clave.

### Restricciones
- misma cantidad aproximada de texto;
- no superar 35 palabras por tarjeta;
- evitar listas largas.

---

## Patrón F — Protocolo de tres pasos

### Objetivo
Presentar una secuencia memorable.

### Composición
- tres columnas;
- círculo grande con letra o número;
- palabra de acción;
- explicación de 1–2 líneas;
- banda inferior con advertencia.

### Ejemplo estructural
```text
P — PROTEGER
A — AVISAR
S — SOCORRER
```

---

## Patrón G — Cuadrícula 2 × 2 de contenidos

### Objetivo
Organizar cuatro grupos de información.

### Composición
- dos columnas;
- dos filas;
- línea vertical de color en cada módulo;
- título coloreado;
- cuerpo gris oscuro;
- banda inferior contextual.

### Colores
- naranja;
- negro;
- cian;
- rojo.

---

## Patrón H — Comparación dual

### Objetivo
Contraponer dos dimensiones.

### Composición
- dos tarjetas grandes;
- una oscura y una naranja;
- antetítulo en mayúsculas;
- título principal;
- lista breve;
- tarjetas con misma altura.

### Restricciones
- cada lado debe contener una idea central;
- máximo cuatro viñetas;
- no usar tablas tradicionales.

---

## Patrón I — Pregunta + bifurcación

### Objetivo
Representar toma de decisiones.

### Composición
- dos preguntas numeradas a la izquierda;
- dos resultados apilados a la derecha;
- cian para resultado favorable;
- rojo para resultado crítico;
- nota inferior en tarjeta clara.

---

## Patrón J — Cadena de supervivencia / proceso

### Objetivo
Explicar una secuencia temporal.

### Composición
- definición en banda oscura;
- mensaje crítico en banda roja;
- tres flechas inferiores;
- etiqueta del proceso;
- nota docente inferior.

---

## Patrón K — Clasificación en cuatro columnas

### Objetivo
Mostrar taxonomías o familias.

### Composición
- cuatro columnas;
- cabeceras de color;
- cuerpos claros;
- listas de 3–5 elementos;
- banda inferior de alcance o limitación.

### Restricciones
- máximo cinco elementos por columna;
- mantener tamaños de texto homogéneos;
- no reducir el cuerpo por debajo de 14 pt.

---

## Patrón L — Regla general + excepciones

### Objetivo
Presentar una norma y sus excepciones.

### Composición
- gran banda roja para la regla;
- etiqueta de excepciones;
- tres módulos numerados;
- banda oscura inferior con conducta provisional.

---

## Patrón M — Tres principios + mensaje transversal

### Objetivo
Relacionar tres principios con una idea común.

### Composición
- tres columnas;
- línea superior de color;
- círculo numerado;
- título y descripción;
- bloque oscuro inferior a toda anchura.

---

## Patrón N — Cierre / próximos pasos

### Objetivo
Cerrar la sesión y activar la siguiente.

### Composición
- fondo oscuro;
- tarjeta naranja grande a la izquierda;
- tres acciones a la derecha;
- checks naranjas;
- título blanco;
- metadatos en gris.

---

# 9. Animaciones y transiciones

La estética de referencia funciona mejor con movimiento discreto.

## Recomendación

- transición general: Desvanecer, 0,3–0,5 s;
- aparición de tarjetas: por bloques;
- flechas: de izquierda a derecha;
- listas: por párrafo solo cuando el docente deba explicar progresivamente;
- evitar rebotes, giros, zoom agresivo y trayectorias.

## Regla

Una animación debe mejorar la secuencia pedagógica. Si no aporta orden,
eliminarla.

---

# 10. Reglas de contenido

## 10.1. Densidad

- una idea principal por diapositiva;
- entre 15 y 55 palabras totales, salvo taxonomías;
- máximo 4 módulos principales;
- máximo 5 elementos por lista;
- evitar tablas densas;
- dividir contenido complejo en varias diapositivas.

## 10.2. Redacción

- títulos declarativos;
- subtítulos explicativos;
- verbos de acción;
- lenguaje directo;
- terminología técnica consistente;
- destacar la idea operativa;
- cerrar con una conclusión, advertencia o aplicación.

## 10.3. Señalización semántica

- naranja: identidad, secuencia, prioridad;
- rojo: riesgo, error, urgencia;
- cian: respuesta afirmativa o estado seguro;
- amarillo: advertencia;
- negro: autoridad, estructura, contraste;
- gris: tercer nivel o contenido secundario.

---

# 11. Accesibilidad

- tamaño mínimo general: 14 pt;
- títulos: mínimo 28 pt;
- no depender únicamente del color;
- acompañar estados con texto, icono o etiqueta;
- usar frases cortas;
- proporcionar texto alternativo a imágenes;
- evitar fondos fotográficos detrás de texto sin una capa de contraste;
- comprobar contraste y legibilidad en proyector;
- mantener orden lógico de lectura.

---

# 12. Control de calidad obligatorio

Antes de entregar una presentación, verificar:

## Documento
- [ ] Formato 16:9.
- [ ] Todas las diapositivas comparten retícula.
- [ ] No existen elementos fuera del área segura.
- [ ] El pie y la numeración son consistentes.

## Tipografía
- [ ] Solo se usa la familia autorizada.
- [ ] Ningún cuerpo esencial es menor de 14 pt.
- [ ] Los títulos mantienen jerarquía constante.
- [ ] No hay desbordamientos ni líneas huérfanas.

## Color
- [ ] El naranja es el acento dominante.
- [ ] Los colores secundarios tienen significado.
- [ ] El contraste es suficiente.
- [ ] No se han añadido degradados innecesarios.

## Componentes
- [ ] Los radios de tarjetas son coherentes.
- [ ] Los círculos numerados tienen el mismo tamaño.
- [ ] Los iconos comparten estilo.
- [ ] Las bandas inferiores están alineadas.

## Contenido
- [ ] Una idea principal por diapositiva.
- [ ] Máximo cuatro focos visuales.
- [ ] Las listas son breves.
- [ ] El cierre incluye una acción o siguiente paso.

## Revisión técnica
- [ ] Exportación a PDF revisada.
- [ ] Compatibilidad comprobada en PowerPoint.
- [ ] Fuentes disponibles o sustituidas por Arial/Aptos.
- [ ] Imágenes nítidas.
- [ ] No hay elementos accidentalmente desplazados.

---

# 13. Instrucciones operativas para el generador

Cuando se solicite una nueva presentación con esta skill:

1. Analizar el contenido y dividirlo en bloques pedagógicos.
2. Crear una narrativa con portada, mapa, bloques, desarrollo y cierre.
3. Seleccionar para cada diapositiva uno de los patrones A–N.
4. Alternar fondos claros y oscuros para marcar cambios de sección.
5. Mantener la paleta y la jerarquía tipográfica especificadas.
6. Utilizar iconos SVG lineales coherentes.
7. No saturar el lienzo.
8. Generar pie y numeración automáticamente.
9. Revisar solapamientos, desbordamientos y contraste.
10. Exportar el PPTX editable y una copia PDF para revisión.

---

# 14. Prompt interno recomendado para la skill

```text
Actúa como diseñador editorial y especialista en presentaciones educativas.

Crea una presentación PowerPoint 16:9 siguiendo estrictamente el sistema
visual “UD00 FORMDEPOR” descrito en esta skill.

OBJETIVO
Transformar el contenido suministrado en una secuencia formativa clara,
visual, modular y apta para proyección en aula.

SISTEMA VISUAL
- Fondo claro #F2F3F5 y fondo oscuro #14161A.
- Acento principal #FF6A00.
- Colores semánticos: #E63946, #00A8B5, #FFB300 y #6C757D.
- Tipografía Arial; fallback Aptos/Calibri.
- Títulos 32–36 pt; cuerpo 14–16 pt.
- Márgenes laterales de 0,50–0,75 in.
- Tarjetas con esquinas redondeadas y sin sombras fuertes.
- Iconografía lineal SVG.
- Pie constante: programa, ciclo, FORMDEPOR y número de diapositiva.
- Alternar diapositivas claras de contenido con separadores oscuros.

ARQUITECTURA
1. Portada.
2. Bienvenida o mapa de la unidad.
3. Contexto o relevancia.
4. Separador de bloque.
5. Desarrollo mediante tarjetas, procesos o comparaciones.
6. Separadores adicionales cuando cambie el resultado de aprendizaje.
7. Cierre y próximos pasos.

CRITERIOS
- Una idea principal por diapositiva.
- Máximo cuatro focos visuales.
- Evitar texto denso.
- No usar tablas salvo necesidad real.
- Mantener alineación exacta y retícula.
- Revisar accesibilidad y contraste.
- No introducir estilos ajenos al sistema.
```

---

# 15. Variables editables

La skill debe permitir sustituir:

```yaml
course_name: ""
unit_code: ""
unit_title: ""
qualification: ""
date_range: ""
session_count: ""
learning_outcomes: []
block_titles: []
footer_left: ""
brand_name: "FORMDEPOR"
primary_accent: "#FF6A00"
```

`footer_left` es específico de cada asignatura/edición (p. ej. "VCF ·
TSEAS · FORMDEPOR" para VCF, "MET · TSEAS · FORMDEPOR" para MET) — se
rellena al generar, igual que `course_name` o `unit_code`, nunca queda
fijo en la skill.

No modificar sin autorización:

```yaml
aspect_ratio: "16:9"
background_light: "#F2F3F5"
background_dark: "#14161A"
font_family: "Arial"
footer_position: "bottom-fixed"
number_position: "bottom-right"
```

---

# 16. Criterio de fidelidad

Una nueva presentación se considerará fiel al sistema cuando:

- sea reconocible como parte de la misma colección;
- conserve la alternancia clara/oscura;
- mantenga el naranja como eje de identidad;
- utilice módulos redondeados y estructura de columnas;
- aplique jerarquías equivalentes;
- tenga una densidad visual y textual comparable;
- use separadores de bloque con macroidentificador;
- mantenga pie, numeración, iconografía y retícula;
- no dependa de copiar exactamente las diapositivas originales.
