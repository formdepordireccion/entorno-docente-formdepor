#!/usr/bin/env python3
"""Genera 04_TEMPORALIZACION/calendario_visual_<curso>.html a partir de un
JSON de configuración, rellenando la plantilla compartida
templates/calendario_visual_template.html (mismo motor CSS+JS para todas
las asignaturas del departamento).

Uso:
    python3 generar_calendario_visual.py CONFIG.json SALIDA.html

Ver la sección "Formato del JSON de configuración" en el SKILL.md de
/asig-programacion para el esquema completo (campos de texto + data +
unit_color).
"""
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = SCRIPT_DIR.parent / "templates" / "calendario_visual_template.html"


def main():
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} CONFIG.json SALIDA.html", file=sys.stderr)
        sys.exit(1)

    config_path = Path(sys.argv[1])
    salida_path = Path(sys.argv[2])

    config = json.loads(config_path.read_text(encoding="utf-8"))

    campos_texto_requeridos = [
        "titulo_pagina", "eyebrow", "curso_academico", "subtitulo",
        "estado_badge", "rango_curso_largo", "dias_lectivos_texto",
        "fecha_fin_lectivo_larga", "fuente_calendario_oficial",
        "fuente_evaluacion_final", "footer_html",
    ]
    faltantes = [c for c in campos_texto_requeridos if c not in config]
    if faltantes:
        print(f"Faltan campos de texto en el JSON de configuración: {faltantes}", file=sys.stderr)
        sys.exit(1)
    if "data" not in config or "unit_color" not in config:
        print("El JSON de configuración necesita las claves 'data' y 'unit_color'.", file=sys.stderr)
        sys.exit(1)

    trimestres = sorted({u["trimestre"] for u in config["data"]["unidades"] if u.get("trimestre")})
    botones_trimestre = "\n          ".join(
        f'<button class="btn-chip" data-tri="{t}">{t}ª evaluación</button>' for t in trimestres
    )

    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    reemplazos = {
        "{{TITULO_PAGINA}}": config["titulo_pagina"],
        "{{EYEBROW}}": config["eyebrow"],
        "{{ESTADO_BADGE}}": config["estado_badge"],
        "{{CURSO_ACADEMICO}}": config["curso_academico"],
        "{{SUBTITULO}}": config["subtitulo"],
        "{{RANGO_CURSO_LARGO}}": config["rango_curso_largo"],
        "{{BOTONES_TRIMESTRE}}": botones_trimestre,
        "{{FOOTER_HTML}}": config["footer_html"],
        "{{DIAS_LECTIVOS_TEXTO}}": config["dias_lectivos_texto"],
        "{{FECHA_FIN_LECTIVO_LARGA}}": config["fecha_fin_lectivo_larga"],
        "{{FUENTE_CALENDARIO_OFICIAL}}": config["fuente_calendario_oficial"],
        "{{FUENTE_EVALUACION_FINAL}}": config["fuente_evaluacion_final"],
        "{{DATA_JSON}}": json.dumps(config["data"], ensure_ascii=False),
        "{{UNIT_COLOR_JSON}}": json.dumps(config["unit_color"], ensure_ascii=False),
    }

    salida = template
    for marcador, valor in reemplazos.items():
        salida = salida.replace(marcador, valor)

    restantes = [m for m in reemplazos if m in salida]
    if restantes:
        print(f"AVISO: quedan marcadores sin sustituir en la salida: {restantes}", file=sys.stderr)

    salida_path.parent.mkdir(parents=True, exist_ok=True)
    salida_path.write_text(salida, encoding="utf-8")
    print(f"Calendario visual generado: {salida_path}")


if __name__ == "__main__":
    main()
