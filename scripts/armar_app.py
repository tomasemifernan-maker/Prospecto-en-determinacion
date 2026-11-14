"""Arma prospectos-colegios.html: copia app/plantilla.html y le mete adentro datos/padron-cordoba.json.

Uso:  python3 scripts/armar_app.py
"""
import json, pathlib

raiz = pathlib.Path(__file__).resolve().parent.parent
plantilla = (raiz / "app" / "plantilla.html").read_text(encoding="utf-8")
datos = json.loads((raiz / "datos" / "padron-cordoba.json").read_text(encoding="utf-8"))
js = json.dumps(datos, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
marca = "/*PADRON*/null"
assert plantilla.count(marca) == 1, "La plantilla tiene que tener una sola marca /*PADRON*/null"
salida = raiz / "prospectos-colegios.html"
salida.write_text(plantilla.replace(marca, js), encoding="utf-8")
print(f"Listo: {salida.name} ({salida.stat().st_size // 1024} KB, {len(datos['escuelas'])} escuelas)")
