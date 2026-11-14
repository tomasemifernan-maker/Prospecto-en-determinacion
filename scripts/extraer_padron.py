"""Saca del Padrón Oficial (Excel nacional) las escuelas de Córdoba con secundario.

Uso:  python3 scripts/extraer_padron.py padron.xlsx
Escribe datos/padron-cordoba.json, que después usa scripts/armar_app.py.
"""
import sys, json, re, unicodedata, collections, openpyxl

# Departamentos tal como los nombra la app (con tildes)
DEPTOS = ["Capital", "Colón", "Río Cuarto", "San Justo", "Punilla", "General San Martín",
          "Río Segundo", "Unión", "Santa María", "Tercero Arriba", "Marcos Juárez", "San Javier",
          "Cruz del Eje", "Calamuchita", "Río Primero", "Juárez Celman",
          "Presidente Roque Sáenz Peña", "Ischilín", "San Alberto", "General Roca", "Río Seco",
          "Totoral", "Tulumba", "Minas", "Sobremonte", "Pocho"]

def norm(s):
    s = unicodedata.normalize("NFD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().upper()

DEP_IDX = {norm(d): i for i, d in enumerate(DEPTOS)}
# El padrón viene sin tildes: se agregan en las palabras más comunes
TILDES = {w.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u"): w
          for w in ["Córdoba", "Río", "María", "Jesús", "José", "Martín", "Juárez", "García",
                    "Unión", "Belén", "Ángel", "Pérez", "González", "Rodríguez", "Fernández",
                    "Sáenz", "Peña", "Ramón", "Simón", "Concepción", "Asunción", "Educación",
                    "Técnica", "Bilingüe", "Agrotécnica", "Tecnológico", "Católico", "Nicolás",
                    "Andrés", "Inés", "Lucía", "Mónica", "Dolores", "Ceballos", "Cosquín",
                    "Ischilín", "Huidobro", "Gálvez", "Álvarez", "Sarmiento", "Galíndez"]}
CHICAS = {"de", "del", "la", "las", "los", "y", "e", "el", "en", "con", "a", "al", "para"}

def titulo(s):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    out = []
    for k, w in enumerate(s.lower().split(" ")):
        if k and w in CHICAS:
            out.append(w)
        elif re.fullmatch(r"(ipem|ipet|ipea|cens|cenma|cenpa|fasta|iem|ies|ise|ena|cbu|ii|iii)|([a-z]\.){2,}[a-z]?\.?", w):
            out.append(w.upper())
        else:
            out.append(w[:1].upper() + w[1:])
    return " ".join(TILDES.get(w, w) for w in " ".join(out).split(" "))

def tel(s):
    """Primer número del campo teléfono, en formato 54 + característica + número.
    Si trae el 15 de celular (ej: 0351 15 6250143) lo saca y lo marca como celular."""
    s = str(s or "")
    s = re.split(r"(?i)int", s)[0]
    d = ""
    for parte in re.split(r"[/;,\-]| y ", re.split(r"[/;,]| y ", s)[0]):
        d += re.sub(r"\D", "", parte)
        d = d.lstrip("0")
        if len(d) >= 10:
            break
    if len(d) == 12:
        for a in (2, 3, 4):
            if d[a:a + 2] == "15":
                return "54" + d[:a] + d[a + 2:], 1
    if len(d) == 10:
        return "54" + d, 0
    return "", 0


def main(xlsx, salida):
    ws = openpyxl.load_workbook(xlsx, read_only=True).worksheets[0]
    escuelas, prim = [], collections.Counter()
    fecha = ""
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        if r[0] and str(r[0]).startswith("Fecha de actualizaci"):
            fecha = str(r[0]).split(":", 1)[1].strip(" .")
        if i < 13 or r[0] != "Córdoba":
            continue
        dep = DEP_IDX.get(norm(r[3]))
        if dep is None:
            raise SystemExit("Departamento desconocido: %r" % r[3])
        loc = titulo(r[5])
        sec, tec = r[19] == 1, r[20] == 1
        if r[18] == 1:
            prim[(dep, loc)] += 1
        if not (sec or tec):
            continue
        escuelas.append([str(r[7]), titulo(r[8]), 1 if r[1] == "Privado" else 0,
                         1 if r[2] == "Rural" else 0, dep, loc, titulo(r[9]),
                         *tel(r[11]), str(r[11] or "").strip(), str(r[12] or "").strip().lower(),
                         1 if tec else 0])
    json.dump({"fecha": fecha, "deptos": DEPTOS,
               "campos": ["cue", "nombre", "privado", "rural", "depto", "localidad",
                          "direccion", "tel", "celular", "tel_original", "mail", "tecnica"],
               "escuelas": escuelas,
               "primarias": [[d, l, n] for (d, l), n in sorted(prim.items())]},
              open(salida, "w"), ensure_ascii=False, separators=(",", ":"))
    print(f"Padrón {fecha}: {len(escuelas)} escuelas con secundario en Córdoba -> {salida}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "datos/padron-cordoba.json")
