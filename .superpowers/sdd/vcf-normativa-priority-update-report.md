# Informe: aplicación de la nueva política de prioridad de fuentes (`/vcf-normativa`) a horas/horario de VCF

**Fecha:** 2026-07-24
**Tarea:** aplicar el nuevo apartado "Orden de prioridad de fuentes" de
`.claude/skills/vcf-normativa/SKILL.md` al dato de horas totales/semanales
del módulo VCF (1136), resolviendo la discrepancia entre el borrador de
programación (200h/6 semanales) y `ficha.yaml` (110h, mínimo legal del RD).

---

## 1. Resultado: Instrucción 13/2024 verificada

**SÍ, la Instrucción 13/2024 existe, es real, es accesible y confirma
literalmente 200 horas totales / 6 horas semanales / 1º curso para el
módulo 1136 en TSEAS.**

### Búsquedas WebSearch ejecutadas

1. `Instrucción 13/2024 Dirección General Formación Profesional Innovación Inclusión Educativa Extremadura aspectos organizativos currículo grado superior`
   - Resultado clave: enlace directo al PDF oficial en educarex.es:
     `https://www.educarex.es/pub/cont/com/0019/documentos/normativa/formacion-profesional/Instruccion_13_2024_adaptacion_GS(F).pdf`
   - Resultados adicionales: `https://www.educarex.es/dgfpiie/dgfpiie-instrucciones.html` (índice de instrucciones de la Dirección General), CSIF Extremadura (resumen sindical de la instrucción), ANPE Extremadura (resumen sindical), y una noticia de EPALE (Comisión Europea) sobre el nuevo diseño curricular de FP en Extremadura.

2. `"Instrucción 13/2024" Extremadura educarex Formación Profesional`
   - Confirma el mismo PDF, más `https://www.educarex.es/legislacion-sge/instrucciones.html` y `https://www.educarex.es/fp/curriculo-extremeno.html`.

### Acceso al documento

`WebFetch` sobre la URL del PDF **falló** (mismo problema que ya se había
documentado para los anexos del Decreto 106/2018: "contenido en formato
binario/codificado, no legible"). Esto es coherente con lo que ya se sabía
de este entorno para PDFs de la Junta de Extremadura.

**Solución aplicada:** descarga directa con `curl` y extracción de texto
local con `pdftotext -layout` (mismo método ya documentado en
`normativa_registro.md` para el RD 653/2017 y el articulado del Decreto
106/2018). Esta vez **sí funcionó**: el PDF de 87 páginas se extrajo
íntegramente y es legible.

```
curl -sL -o instruccion_13_2024.pdf "https://www.educarex.es/pub/cont/com/0019/documentos/normativa/formacion-profesional/Instruccion_13_2024_adaptacion_GS(F).pdf"
pdftotext -layout instruccion_13_2024.pdf instruccion_13_2024.txt
```

`pdfinfo` confirma: `CreationDate: Thu Jun 20 13:14:54 2024 CEST`, 87
páginas, PDF 1.4, sin cifrar.

### Datos confirmados con cita literal

**Título completo** (portada del documento):

> "INSTRUCCIÓN 13/2024, DE LA DIRECCIÓN GENERAL DE FORMACIÓN PROFESIONAL,
> INNOVACIÓN E INCLUSIÓN EDUCATIVA, POR LA QUE SE REGULAN ASPECTOS
> ORGANIZATIVOS DEL CURRÍCULO PARA LOS CICLOS FORMATIVOS DE GRADO SUPERIOR
> DEL SISTEMA EDUCATIVO EN LA COMUNIDAD AUTÓNOMA DE EXTREMADURA."

Firmado por el Director General de Formación Profesional, Innovación e
Inclusión Educativa (Pedro Antonio Pérez Durán); firma electrónica con CSV
`FDJEXEY3JJ6K6RZG2NM4BDBZWDZBGB`, verificable en
`https://sede.gobex.es/SEDE/csv/codSeguroVerificacion.jsf`.

**Apartado "Primero.2.b.i"** — lista el Decreto 106/2018 (TSEAS) dentro de
la familia "Actividades Físicas y Deportivas" como uno de los currículos a
los que aplica esta instrucción — confirma que la instrucción sí es
aplicable a VCF/TSEAS.

**Apartado "Segundo.2"** (vigencia del currículo no modificado):

> "Los resultados de aprendizaje y los criterios de evaluación de los
> módulos profesionales serán los incluidos en los correspondientes
> decretos a los que hace referencia apartado 'Primero - 2' del presente
> documento, teniendo en consideración las modificaciones recogidas para
> cada título en el Real Decreto 500/2024, de 21 de mayo, junto con las
> posibles concreciones curriculares, si las hubiere, que figuren en esta
> instrucción."

Confirma la cita del borrador ("los RA y criterios continúan vigentes...
según confirma el apartado 'Segundo'"). No se detectó ninguna concreción
curricular que modifique RA/criterios de VCF en el resto del documento (87
páginas revisadas con `grep`/lectura de las secciones relevantes).

**Anexo 3 — "ENSEÑANZA Y ANIMACIÓN SOCIO DEPORTIVA AFD3-1"** (tabla de
secuenciación horaria del ciclo TSEAS; cita literal extraída con
`pdftotext -layout`, sin reformatear):

```
                                                                                                    Secuenciación
                                     Módulos                               Horas              1º             2º

                  1136. Valoración de la condición física e                 200               6
                  intervención en accidentes.
```

Es decir: **Horas = 200**, columna **Secuenciación · 1º curso = 6** (2º
curso en blanco). Confirmado dos veces en el documento: también aparece,
con idénticas cifras, en el **Anexo 4 — "ACONDICIONAMIENTO FÍSICO
AFD3-2"** (módulo 1136 compartido entre los dos títulos "Actividades
Físicas y Deportivas" de Extremadura).

**Apartado "Sexto. Calendario de aplicación"**:

> "todas las modificaciones referidas en la presente instrucción deberán
> entrar en vigor, y ser aplicadas, a partir del curso académico 2024/2025,
> para los grupos de primer curso, y a partir del 2025/2026 para los grupos
> de segundo curso."

VCF/1136 es módulo de 1º curso → aplicación desde 2024/2025, plenamente
vigente en 2026/2027.

### Conclusión de la verificación

**Todo lo que citaba el borrador de programación sobre la Instrucción
13/2024 se ha confirmado literalmente**: existencia real, título exacto,
fecha, confirmación de que RA/criterios de VCF no cambian respecto al
Decreto 106/2018, y la cifra de 200 horas totales / 6 semanales / 1º curso
para el módulo 1136 en TSEAS.

---

## 2. Aplicación de la política de prioridad de fuentes

Según `SKILL.md` ("Orden de prioridad de fuentes"), 200h no es un "error
notorio" porque:

- No está por debajo del mínimo legal del RD (200 > 110 — está *por
  encima*, que es justo el caso que la política distingue como NO
  notorio).
- No omite ningún RA del RD ni añade uno inexistente.
- No elimina ningún bloque de contenidos obligatorio del RD.

Y la fuente adicional que cita la programación (Instrucción 13/2024) ha
quedado verificada con WebSearch + lectura directa del documento oficial.

**Por tanto:** 200 horas / 6 semanales pasa a ser la cifra operativa
confirmada en `ficha.yaml`, citada con la Instrucción 13/2024 como fuente
(no "según la programación" a secas), y las 110 horas del RD quedan
registradas aparte como referencia del mínimo legal estatal.

---

## 3. Diff exacto de `ficha.yaml`

```diff
diff --git a/DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml b/DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml
index 2989379..6d55f4c 100644
--- a/DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml
+++ b/DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/00_FICHA/ficha.yaml
@@ -7,11 +7,18 @@ asignatura:
   curso_academico: "2026-2027"
   docente: Mario Pérez Quintero
   horas_totales:
-    valor: 110
-    fuente: "RD 653/2017, Anexo I, módulo profesional 1136 (duración mínima estatal)"
-    confirmado_extremadura: false
-    nota: "110 horas es la duración fijada en el RD estatal para el módulo 1136. No he podido confirmar si el Decreto 106/2018 de Extremadura asigna el mismo total de horas anuales para VCF en el centro: el anexo III de ese decreto no es legible con las herramientas disponibles. Pendiente de verificación manual."
-  horas_semanales: null # no confirmado: el anexo III del Decreto 106/2018 (Extremadura), que fija la distribución horaria semanal por módulo, no se ha podido leer con las herramientas disponibles. Pendiente de verificación manual.
+    valor: 200
+    confirmado_extremadura: true
+    fuente: "Instrucción 13/2024, de la Dirección General de Formación Profesional, Innovación e Inclusión Educativa (Extremadura), de 20 de junio de 2024, Anexo 3 (Enseñanza y Animación Sociodeportiva AFD3-1), módulo 1136 (200 horas totales, 6 semanales, 1er curso); coincide con la portada y el cuerpo del borrador de programación docente real ('Horas: 200 (6 horas semanales)')."
+    minimo_legal_rd:
+      valor: 110
+      fuente: "RD 653/2017, de 23 de junio, Anexo I, módulo profesional 1136 (duración MÍNIMA fijada por el Estado; no es la cifra operativa a usar, ver 'valor' arriba)."
+    nota: "VALOR OPERATIVO REAL A USAR: 200 (no 110). El RD 653/2017 fija 110 horas como mínimo legal estatal para el módulo 1136 (ver horas_totales.minimo_legal_rd), pero la normativa autonómica vigente de Extremadura -Instrucción 13/2024, de la Dirección General de Formación Profesional, Innovación e Inclusión Educativa, Anexo 3- asigna 200 horas totales (6 semanales, 1º curso) al módulo 1136 en el título TSEAS. Verificado literalmente sobre el PDF oficial (educarex.es) descargado y extraído con pdftotext: tabla de secuenciación del Anexo 3, fila '1136. Valoración de la condición física e intervención en accidentes.', columna Horas=200, columna Secuenciación·1º=6. Esta cifra coincide con la que declara el borrador de programación docente real del centro ('Horas: 200 (6 horas semanales)'), que citaba esta misma instrucción como fuente. Por el orden de prioridad de fuentes de /vcf-normativa (ver SKILL.md), 200h está por encima del mínimo legal del RD -no por debajo- y no contradice ningún RA/criterio/contenido del RD, por lo que no es un caso de 'error notorio': se adopta 200h como cifra confirmada. El Anexo III del Decreto 106/2018 sigue sin poder leerse con las herramientas disponibles, pero la Instrucción 13/2024 -norma autonómica posterior, vigente y verificada de forma independiente- resuelve el mismo dato por otra vía. Detalle completo de la verificación en 01_NORMATIVA_CURRICULO/normativa_registro.md."
+  horas_semanales:
+    valor: 6
+    confirmado_extremadura: true
+    fuente: "Instrucción 13/2024, de la Dirección General de Formación Profesional, Innovación e Inclusión Educativa (Extremadura), Anexo 3 (Enseñanza y Animación Sociodeportiva AFD3-1), módulo 1136, columna 'Secuenciación · 1º curso' = 6; coincide con la portada del borrador de programación docente real ('6 horas semanales')."
+    nota: "Sustituye el valor null anterior. La imposibilidad de leer el Anexo III del Decreto 106/2018 (que motivaba el null) queda resuelta por la Instrucción 13/2024, fuente autonómica posterior, legible y verificada, que fija explícitamente la secuenciación horaria semanal por módulo y curso. No confirma el reparto concreto por día/hora/aula (eso sigue pendiente de Jefatura de Estudios, ver 02_PROGRAMACION/programacion_26_27.md y 04_TEMPORALIZACION/calendario_26_27.md)."
 normativa:
   rd_estatal:
     identificador: "Real Decreto 653/2017, de 23 de junio"
```

**Decisión de diseño:** los nombres de las claves de nivel superior
(`asignatura.horas_totales`, `asignatura.horas_semanales`) se mantienen sin
renombrar (el propio plan de diseño del proyecto,
`docs/superpowers/plans/2026-07-23-entorno-docente-vcf-piloto.md`, indica
explícitamente que las tareas `/vcf-*` leen/escriben sobre estas claves
exactas y no deben renombrarse). Dentro de `horas_totales` se añade
`minimo_legal_rd` (con su propio `valor`/`fuente`) para no perder la cifra
del RD, y `valor` pasa a ser la cifra operativa (200), dejando en `nota`
una indicación explícita ("VALOR OPERATIVO REAL A USAR: 200 (no 110)")
para que no haya ambigüedad sobre cuál es el dato a usar.

---

## 4. Texto añadido a `normativa_registro.md`

Se añadió una nueva sección 6 completa ("Instrucción 13/2024 (Extremadura)
— resolución de horas totales y semanales del módulo 1136") con: búsquedas
realizadas, identificación completa de la norma (título, URL, firma, CSV,
fecha, fecha de consulta), método de verificación (curl + pdftotext local,
igual que para el RD/decreto previos), citas literales de los apartados
"Primero.2.b.i", "Segundo.2", Anexo 3 (tabla completa con la fila del
módulo 1136) y "Sexto", y la aplicación explícita del orden de prioridad de
fuentes. También se actualizó el punto 3 de la sección 5 ("Confirmación
pendiente") para reflejar que las horas ya no están pendientes de
verificación manual del Anexo III del decreto (aunque siguen pendientes de
la confirmación explícita final del docente, igual que el resto de datos
de esa lista).

Diff completo: ver `git diff` sobre
`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/01_NORMATIVA_CURRICULO/normativa_registro.md`
(176 líneas añadidas/modificadas). Resumen de la estructura añadida:

- `### Búsquedas realizadas para esta verificación (WebSearch)`
- `### Norma verificada` (título, URL, firma/CSV, fechas, extensión)
- `### Cómo se verificó` (curl + pdftotext, comparación con el fallo de
  WebFetch)
- `### Datos confirmados` (citas literales: Primero.2.b.i, Segundo.2, Anexo
  3, Sexto)
- `### Aplicación del "Orden de prioridad de fuentes" de /vcf-normativa`
  (razonamiento explícito de por qué no es "error notorio" y qué campos de
  `ficha.yaml` cambian)

---

## 5. Texto de reconciliación en `programacion_26_27.md`

Se sustituyó el párrafo "**Discrepancia detectada y no resuelta — horas
totales del módulo.**" por "**Discrepancia resuelta (2026-07-24) — horas
totales del módulo.**", explicando: qué decía el borrador, qué registraba
`ficha.yaml` antes, qué se verificó (Instrucción 13/2024, Anexo 3, cita
literal), por qué no es un "error notorio" según la política del skill, y
los dos campos de `ficha.yaml` que cambiaron, con referencia cruzada a la
sección 6 de `normativa_registro.md`. Se dejó explícito que el reparto
concreto del horario por día/hora/aula **no** queda confirmado por esta vía
(sigue pendiente de Jefatura de Estudios).

También se actualizaron los puntos 1 y 2 de la sección "9. Apartados
pendientes de confirmación": el punto 1 (antes "horas totales/semanales...
discrepancia") pasa a "resuelto (2026-07-24)"; el punto 2 (antes citaba
`asignatura.horas_semanales: null`, que ya no es cierto) se reformuló para
dejar claro que la cifra total (6h) está confirmada pero el reparto
concreto por sesión sigue pendiente.

Diff completo: ver `git diff` sobre
`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/02_PROGRAMACION/programacion_26_27.md`
(71 líneas modificadas, dos bloques: apartado 1 e índice de pendientes,
apartado 9).

---

## 6. Texto de reconciliación en `calendario_26_27.md`

En la sección "2. Horario semanal considerado" se separó el punto que sigue
sin confirmar (horario concreto por día/hora/aula — responsabilidad de
Jefatura de Estudios, sin cambios) del punto que ya se resolvió
(`asignatura.horas_semanales` ya no es `null`, ahora es 6, con fuente
Instrucción 13/2024), añadiendo un párrafo "**Actualización
(2026-07-24)**" con referencias cruzadas a `normativa_registro.md` sección
6 y `programacion_26_27.md` apartado 1, y explicando por qué esto no
constituía un "error notorio" bajo la nueva política del skill.

Diff completo: ver `git diff` sobre
`DEPARTAMENTO_DOCENTE/ASIGNATURAS/VCF_TSEAS/04_TEMPORALIZACION/calendario_26_27.md`
(25 líneas modificadas).

---

## 7. Verificación antes de commitear

- **YAML válido:** `python3 -c "import yaml; yaml.safe_load(open('ficha.yaml'))"`
  → sin errores.
- **`estado: borrador`** sin cambios (verificado leyendo el campo tras la
  carga YAML).
- **RA/criterios/contenidos sin cambios:** verificado por conteo tras
  cargar el YAML → 9 resultados de aprendizaje, 57 criterios de
  evaluación, 9 bloques de contenidos (igual que antes de la
  actualización).
- **`git diff` de `ficha.yaml`:** confirma que el único bloque modificado
  es `asignatura.horas_totales` / `asignatura.horas_semanales` (ver diff
  completo en la sección 3 de este informe); nada más en el archivo
  cambió.
- **`git diff --stat`** general: modifica exactamente 4 archivos —
  `ficha.yaml`, `normativa_registro.md`, `programacion_26_27.md`,
  `calendario_26_27.md` — y ningún otro (256 inserciones, 33 eliminaciones
  en total). No se tocó ningún archivo de `05_UNIDADES/`, exámenes,
  temarios, ni ningún otro archivo del repositorio.

---

## 8. Commit

Ver mensaje de commit en el historial de git (`git log -1`) tras ejecutar
este trabajo; describe exactamente que la Instrucción 13/2024 fue
verificada y que 200h/6 semanales pasa a ser la cifra operativa
confirmada, con 110h conservada como referencia del mínimo legal del RD.
