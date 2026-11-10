#!/usr/bin/env python3
"""Inventario no destructivo para un ensayo de alojamiento independiente.

No despliega nada, no accede a cuentas externas ni modifica contenidos.
"""
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
FAVORITAS = [
    "index.html",
    "prueba-explorandum.html",
    "inmersion-mar-cortes.html",
    "baja-california.html",
    "cabina-video-real-ocho.html",
    "pilotar-submarino.html",
    "aventura.html",
]
OTRAS = [
    "cielo-y-cosmos-baja-california.html",
    "tierra-viva-baja-california.html",
    "oceano-inmersivo-3d.html",
]
ANTIGUO = "prepdiplo-web.github.io/Explorandum"


class Enlaces(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.urls: list[str] = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        for key in ("href", "src", "poster"):
            value = values.get(key)
            if value:
                self.urls.append(value)


def comprobar():
    faltan = [x for x in FAVORITAS + OTRAS if not (ROOT / x).is_file()]
    if faltan:
        raise SystemExit("Faltan páginas esenciales: " + ", ".join(faltan))

    htmls = list(ROOT.glob("*.html"))
    archivos = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
    videos = list((ROOT / "media").rglob("*.mp4")) if (ROOT / "media").exists() else []
    grandes = [str(p.relative_to(ROOT)) for p in archivos if p.stat().st_size > 25 * 1024 * 1024]
    enlaces_rotos: list[str] = []
    menciones_antiguas: list[str] = []
    total_refs = 0

    for html in htmls:
        texto = html.read_text(encoding="utf-8", errors="replace")
        if ANTIGUO in texto:
            menciones_antiguas.append(html.name)
        parser = Enlaces()
        parser.feed(texto)
        for value in parser.urls:
            total_refs += 1
            value = value.strip()
            if not value or value.startswith(("#", "//", "data:", "mailto:", "tel:", "javascript:")):
                continue
            u = urlsplit(value)
            if u.scheme or u.netloc or not u.path:
                continue
            relative = unquote(u.path).lstrip("/")
            if relative.startswith("Explorandum/"):
                relative = relative[len("Explorandum/"):]
            if not relative:
                continue
            # Solo referencias a archivos directos, sin rutas generadas en JavaScript.
            p = ROOT / relative if u.path.startswith("/") else html.parent / relative
            if not p.exists():
                enlaces_rotos.append(f"{html.name}: {value}")

    resumen = {
        "archivos_repositorio": len(archivos),
        "html": len(htmls),
        "videos_mp4": len(videos),
        "tamano_total_mib": round(sum(p.stat().st_size for p in archivos) / (1024 * 1024), 2),
        "video_mayor_mib": round(max((p.stat().st_size for p in videos), default=0) / (1024 * 1024), 2),
        "archivos_mayores_25_mib": grandes,
        "referencias_estaticas": total_refs,
        "referencias_locales_no_encontradas": enlaces_rotos[:30],
        "paginas_con_url_antigua_literal": menciones_antiguas,
        "favoritas_conservadas": FAVORITAS,
        "estado_publicacion_cloudflare": "SIN CREAR / SIN CONECTAR",
        "advertencia_videos": "No confirma autorización de distribuir MP4 por Cloudflare Pages/R2",
    }
    print(json.dumps(resumen, ensure_ascii=False, indent=2))
    if grandes:
        raise SystemExit("Hay activos incompatibles con el límite 25 MiB/archivo de Pages")
    if not videos:
        raise SystemExit("No se detectaron vídeos: revisar el inventario antes de migrar")


if __name__ == "__main__":
    comprobar()
