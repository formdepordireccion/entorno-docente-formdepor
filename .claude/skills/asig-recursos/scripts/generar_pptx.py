#!/usr/bin/env python3
"""Genera un .pptx a partir de un Markdown con secciones `##`.

Uso:
    .venv-recursos/bin/python .claude/skills/asig-recursos/scripts/generar_pptx.py \
        --input RUTA_MARKDOWN --output RUTA_PPTX --titulo "Título de la presentación" \
        [--subtitulo "Subtítulo de la portada (p. ej. '<CODIGO> · <CICLO> · Formdepor')"]

Regla de conversión (deliberadamente simple, sin dependencias de red):
- El primer `#` del archivo (si existe) se ignora como título de sección;
  el título real de la presentación lo da siempre --titulo.
- Cada `##` se convierte en una diapositiva nueva (título = texto del `##`).
- Las líneas de una sección que empiezan por `-`/`*` son viñetas; los
  párrafos sueltos se añaden como una viñeta por párrafo. Los `###` se
  añaden como viñeta en negrita para marcar subapartados sin crear una
  diapositiva nueva.
- Emphasis Markdown (`**negrita**`, `*cursiva*`) se elimina del texto
  (python-pptx no interpreta Markdown) — el énfasis se pierde, no el
  contenido.
"""

import argparse
import re
from pptx import Presentation


def limpiar_markdown(texto: str) -> str:
    texto = re.sub(r"\*\*(.+?)\*\*", r"\1", texto)
    texto = re.sub(r"\*(.+?)\*", r"\1", texto)
    texto = re.sub(r"`(.+?)`", r"\1", texto)
    return texto.strip()


def parsear_secciones(md_texto: str):
    """Devuelve una lista de (titulo_seccion, [lineas_contenido])."""
    secciones = []
    titulo_actual = None
    contenido_actual = []
    for linea in md_texto.splitlines():
        m2 = re.match(r"^##\s+(.*)", linea)
        if m2:
            if titulo_actual is not None:
                secciones.append((titulo_actual, contenido_actual))
            titulo_actual = limpiar_markdown(m2.group(1))
            contenido_actual = []
            continue
        if titulo_actual is None:
            continue  # contenido antes del primer ## (p. ej. el # inicial) se ignora
        m3 = re.match(r"^###\s+(.*)", linea)
        if m3:
            contenido_actual.append(("sub", limpiar_markdown(m3.group(1))))
            continue
        mb = re.match(r"^\s*[-*]\s+(.*)", linea)
        if mb:
            contenido_actual.append(("bullet", limpiar_markdown(mb.group(1))))
            continue
        if linea.strip():
            contenido_actual.append(("bullet", limpiar_markdown(linea.strip())))
    if titulo_actual is not None:
        secciones.append((titulo_actual, contenido_actual))
    return secciones


def construir_pptx(secciones, titulo_presentacion: str, ruta_salida: str, subtitulo: str = "Formdepor", max_bullets_por_diapositiva: int = 8):
    prs = Presentation()

    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = titulo_presentacion
    if len(slide.placeholders) > 1:
        slide.placeholders[1].text = subtitulo

    layout_contenido = prs.slide_layouts[1]

    for titulo_seccion, items in secciones:
        # Trocea en varias diapositivas si hay demasiadas viñetas para una sola
        bloques = [items[i:i + max_bullets_por_diapositiva] for i in range(0, len(items), max_bullets_por_diapositiva)] or [[]]
        for idx, bloque in enumerate(bloques):
            slide = prs.slides.add_slide(layout_contenido)
            sufijo = f" ({idx + 1}/{len(bloques)})" if len(bloques) > 1 else ""
            slide.shapes.title.text = titulo_seccion + sufijo
            cuerpo = slide.placeholders[1].text_frame
            cuerpo.clear()
            primero = True
            for tipo, texto in bloque:
                p = cuerpo.paragraphs[0] if primero else cuerpo.add_paragraph()
                primero = False
                p.text = texto
                if tipo == "sub":
                    p.level = 0
                    p.font.bold = True
                else:
                    p.level = 1 if tipo == "bullet" else 0

    prs.save(ruta_salida)
    return len(prs.slides)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--titulo", required=True)
    ap.add_argument(
        "--subtitulo",
        default="Formdepor",
        help="Subtítulo de la diapositiva de portada (p. ej. '<CODIGO> · <CICLO> · Formdepor')",
    )
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        md_texto = f.read()

    secciones = parsear_secciones(md_texto)
    if not secciones:
        raise SystemExit(f"No se encontraron secciones '##' en {args.input} — nada que convertir.")

    construir_pptx(secciones, args.titulo, args.output, subtitulo=args.subtitulo)
    print(f"OK: {args.output} generado con {len(secciones)} secciones de origen.")


if __name__ == "__main__":
    main()
