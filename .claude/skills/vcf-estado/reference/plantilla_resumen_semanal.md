# Plantilla del resumen semanal — artefacto HTML

Guía de diseño para el artefacto que genera `/vcf-estado` en su modo
"resumen semanal" (ver `SKILL.md`). El objetivo es que cada semana el
artefacto se vea coherente sin tener que rediseñarlo desde cero — esta
plantilla fija las decisiones, el contenido varía.

## Marca

Reutiliza la paleta FORMDEPOR ya definida para las presentaciones
(`.claude/skills/vcf-recursos/reference/FORMDEPOR_especificaciones_tecnicas_powerpoint.md`,
sección 5), adaptada a web:

| Token | HEX | Uso |
|---|---|---|
| `--azul-noche` | `#14142D` | Cabecera, fondo de las tarjetas de asignatura, pie |
| `--azul-formacion` | `#185ADB` | Acento: enlaces, bordes activos, checkbox marcado |
| `--blanco-humo` | `#F6F8FB` | Fondo de página en tema claro |
| `--gris-texto` | `#6B7280` | Texto secundario, metadatos, fechas |
| `--negro-suave` | `#1F2937` | Texto principal sobre fondo claro |
| `--blanco` | `#FFFFFF` | Texto sobre fondo oscuro |

Añade dos tokens semánticos, independientes del acento de marca (no
uses `--azul-formacion` para esto):
- `--urgente` (`#D64545` aprox., un rojo/terracota discreto): hitos que
  caen en los próximos 7 días.
- `--al-dia` (`#2FBF71`, el verde health de la guía): elementos ya
  generados / sin pendientes.

Tema oscuro: invierte fondo/tarjeta (`--azul-noche` como fondo de
página, tarjetas en un tono ligeramente más claro que el fondo, nunca
negro puro) y mantén `--azul-formacion` como acento en ambos temas
— es legible en los dos fondos. Seguir `prefers-color-scheme` y
`data-theme` como marca la skill `artifact-design`.

**Tipografía:** Aptos/Aptos Display (la fuente de marca) no es
embebible como web font — usa una pila de sistema que se le parezca:
`"Aptos", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`
para todo el texto (así, si algún día el sistema del docente sí tiene
Aptos instalada, se usa; si no, cae en una sans de sistema limpia,
nunca en una serif ni en una decorativa). No hace falta `@font-face`:
es un informe interno, no una pieza editorial.

## Estructura de la página

1. **Cabecera** (fondo `--azul-noche`, texto blanco): título "Resumen
   semanal · VCF" (o el nombre que corresponda cuando haya más
   asignaturas), rango de fechas de la semana en curso, fecha de
   generación. Si ninguna asignatura tiene urgencias, una línea
   destacada aquí mismo: "Todo al día esta semana."
2. **Una sección por asignatura**, en el orden de `ASIGNATURAS/*`
   (alfabético). Cada sección es una tarjeta independiente con:
   - Nombre de la asignatura y ciclo (de `ficha.yaml → asignatura`).
   - Sub-bloque **Esta semana** (hoy → +7 días): lista de hitos y
     huecos de contenido con checkbox calculado (marcado = el archivo
     ya existe; sin marcar = falta) y una etiqueta de color
     `--urgente` en los elementos sin marcar de este sub-bloque.
   - Sub-bloque **La semana que viene** (+7 → +14 días): mismo formato,
     sin el color de urgencia (es aviso, no urgencia).
   - Si no hay nada en ninguna de las dos ventanas para esa asignatura,
     una línea con el color `--al-dia`: "Sin pendientes en las próximas
     dos semanas."
3. **Pie**: una frase fija explicando que las casillas se recalculan
   solo a partir de si el archivo existe en el repositorio, que la
   página es estática (marcarlas a mano en el navegador no se guarda
   en ningún sitio) y la fecha/hora de generación.

## Casillas

Renderiza cada elemento como una fila con un icono de casilla (✓ en
`--al-dia` si el archivo existe, ○ en `--urgente` u opaco según la
ventana si no) seguido del texto del elemento y, si aplica, qué comando
lo generaría (`/vcf-unidad`, `/vcf-tema`, etc.) en texto secundario
(`--gris-texto`). No uses `<input type="checkbox">` interactivas de
verdad — son de solo lectura (recalculadas, no clicables), así que un
carácter o icono estático evita sugerir una interactividad que no
existe.

## Responsive y overflow

Una sola columna en móvil, hasta dos columnas de tarjetas de asignatura
en pantallas anchas (`grid`, `gap`, sin márgenes por elemento). Nada de
tablas anchas aquí, así que no debería hacer falta scroll horizontal;
si en el futuro se añade algo tabular (p. ej. una vista comparativa
entre asignaturas), envuélvelo en su propio contenedor con
`overflow-x: auto`.

## Qué NO hacer

- No declares la capacidad `mcp` ni `downloads` en este artefacto: no
  hace falta ninguna (ver decisión registrada en `SKILL.md` — las
  casillas son computadas, no persistidas).
- No repitas el informe completo de `/vcf-estado` (30/45 días,
  incoherencias detalladas) — este artefacto es solo el recorte de "qué
  urge esta semana y la siguiente".
- No inventes datos de alumnado ni toques
  `10_DIVERSIDAD/`/`11_SEGUIMIENTO_RESULTADOS/CALIFICACIONES/` — el
  resumen semanal es contenido curricular, igual que el resto de
  `/vcf-estado`.
