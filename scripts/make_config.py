"""Builds web/config.yml (Sveltia CMS) from the victoriasickness-web content files, so every text gets a field.

Run after adding or removing keys in victoriasickness-web/content/i18n/*.json or changing a content file's shape:
    python3 scripts/make_config.py ../victoriasickness-web web/config.yml
(needs: pip install pyyaml). Adapted from ciaVENDAVAL/lasenyal-admin."""
import json, sys, yaml
web, out = sys.argv[1], sys.argv[2]
J = lambda p: json.load(open(f"{web}/{p}", encoding="utf-8"))
ref = J("content/i18n/es.json")            # reference language: every key that exists
site = J("content/site.json")
LOCALES = site["languages"]                # es ca eu en fr it pt de

L = {  # friendly labels for the Texts form (Spanish: tyle and the company work in ES/CA)
 "lang_name": ("Nombre del idioma (no tocar)", "Lo usa el menú de idiomas."),
 "lang_label": ("Código del idioma (no tocar)", None), "locale": ("Locale (no tocar)", None),
 "meta": ("Google y redes · título y descripción", "Lo que aparece en Google y al compartir el enlace."),
 "ui": ("Interfaz · botones y avisos", None), "a11y": ("Interfaz · panel de accesibilidad", None),
 "nav": ("Menú", None), "hero": ("Portada · texto grande", None), "marquee": ("Portada · cinta roja (palabras)", "Una palabra o frase por línea."),
 "labels": ("Títulos pequeños (ficha, apoyos, galería…)", None), "roles": ("Ficha artística · nombres de los roles", "Los créditos de cada espectáculo eligen uno de estos."),
 "shows": ("Espectáculos · textos", "Estado, etiquetas, descripción y técnicas de cada espectáculo. Título, vídeo, créditos y fotos: en «Espectáculos»."),
 "about": ("Sobre mí · bio y cita", None), "contact": ("Contacto", None),
}
human = lambda k: k.replace("_", " ").capitalize()

def field(k, v, top=False):
    lab, hint = L.get(k, (human(k), None)) if top else (human(k), None)
    f = {"name": k, "label": lab}
    if hint: f["hint"] = hint
    if isinstance(v, str):
        f["widget"] = "text" if len(v) > 70 else "string"
    elif isinstance(v, list) and all(isinstance(x, str) for x in v):
        f["widget"] = "list"
    elif isinstance(v, list):
        f.update(widget="list", collapsed=False, fields=[field(a, b) for a, b in v[0].items()])
    elif isinstance(v, dict):
        f.update(widget="object", collapsed=True, fields=[field(a, b) for a, b in v.items()])
    elif isinstance(v, bool):
        f["widget"] = "boolean"
    else:
        raise SystemExit(f"unexpected {k}: {v!r}")
    return f

def mark_i18n(fs):
    for f in fs:
        f["i18n"] = True
        if "fields" in f: mark_i18n(f["fields"])
    return fs

texts = mark_i18n([field(k, v, top=True) for k, v in ref.items()])
for f in texts:   # technical keys: visible but marked, never translated
    if f["name"] in ("lang_name", "lang_label", "locale"): f["required"] = True

roles = [{"label": v, "value": k} for k, v in ref["roles"].items()]
download_keys = [k for k in J("content/downloads.json")]
note = lambda name, text: {"name": name, "label": "Nota (no tocar)", "widget": "hidden", "default": text}

def img(name, label, hint=None, req=True):
    f = {"name": name, "label": label, "widget": "image", "media_folder": "/source-images", "public_folder": "/source-images", "required": req}
    if hint: f["hint"] = hint
    return f

shape = {"name": "o", "label": "Forma", "widget": "select", "default": "p",
         "options": [{"label": "Vertical", "value": "p"}, {"label": "Horizontal", "value": "l"}]}

SITE = site["site"]["preview_url"]
cfg = {
 "app_title": "Cia. Victoria Sickness · web",
 "logo": {"src": "/victoriasickness-admin/favicon.svg"},
 "backend": {"name": "github", "repo": "ciaVENDAVAL/victoriasickness-web", "branch": "main", "auth_methods": ["token"],
             "commit_messages": {"create": "Admin: create {{collection}} “{{slug}}”", "update": "Admin: update {{collection}} “{{slug}}”",
                                 "delete": "Admin: delete {{collection}} “{{slug}}”", "uploadMedia": "Admin: upload “{{path}}”", "deleteMedia": "Admin: delete “{{path}}”"}},
 "site_url": SITE + "/es/",
 "display_url": SITE + "/es/",
 "media_folder": "source-images",
 "public_folder": "/source-images",
 "media_libraries": {"default": {"config": {"slugify_filename": False, "max_file_size": 25000000}}},
 "editor": {"preview": False},
 "output": {"json": {"indent_size": 1}, "omit_empty_optional_fields": True},
 "i18n": {"structure": "multiple_folders", "locales": LOCALES, "default_locale": "es"},
 "asset_collections": [
   {"name": "photos", "label": "Fotos (originales)", "media_folder": "source-images", "public_folder": "/source-images", "icon": "photo_library"},
   {"name": "pdfs", "label": "PDFs", "media_folder": "static/pdf", "public_folder": "/pdf", "icon": "picture_as_pdf"},
 ],
 "singletons": [
   {"name": "downloads", "label": "PDFs: cuál da cada enlace", "icon": "picture_as_pdf", "file": "content/downloads.json",
    "fields": [{"name": k, "label": f"Dossier · {k}", "widget": "object", "collapsed": k != download_keys[0],
                "hint": f"Enlace corto para emails: …/dossier/{k}/<idioma>/ — da siempre el PDF elegido aquí. Si un idioma está vacío, se da el castellano. Nombre: VictoriaSickness-Invocaciones_ES_dossier_2027-01.pdf",
                "fields": [{"name": l, "label": l.upper(), "widget": "file", "media_folder": "/static/pdf", "public_folder": "/pdf", "required": l == "es"} for l in LOCALES]}
               for k in download_keys]},
   {"name": "theme", "label": "Aspecto: colores y letra", "icon": "palette", "file": "content/theme.json", "fields": [
     note("_about", J("content/theme.json")["_about"]),
     {"name": "ink", "label": "Fondo oscuro (negro)", "widget": "color", "default": "#120d11"},
     {"name": "bone", "label": "Fondo claro y texto (crema)", "widget": "color", "default": "#f4eee6"},
     {"name": "lacquer", "label": "Rojo laca (botones, cinta)", "widget": "color", "default": "#e8004f"},
     {"name": "bubble", "label": "Rosa (detalles)", "widget": "color", "default": "#ff8fc7"},
     {"name": "body_font", "label": "Letra del texto", "widget": "select", "default": "Instrument Sans", "dropdown_threshold": 12,
      "options": ["Instrument Sans", "Bricolage Grotesque", "system-ui"],
      "hint": "Servidas desde la propia web (sin Google). Los títulos siguen en Instrument Serif / Bricolage."}]},
   {"name": "about", "label": "Sobre mí: fotos", "icon": "face", "file": "content/about.json", "fields": [
     note("_about", J("content/about.json")["_about"]),
     img("portrait", "Retrato grande (arco)", "Vertical. Se muestra entero, sin recortar."),
     {"name": "images", "label": "Tira de fotos", "widget": "list", "collapsed": True, "thumbnail": "file", "summary": "{{fields.file}}",
      "label_singular": "foto", "hint": "4 fotos verticales, en orden.", "fields": [img("file", "Foto"), shape]}]},
   {"name": "photos", "label": "Créditos de las fotos", "icon": "copyright", "file": "content/photos.json", "fields": [
     note("_about", J("content/photos.json")["_about"]),
     {"name": "camera_files", "label": "Nombre original de cada foto (no tocar)", "widget": "keyvalue", "required": False},
     {"name": "credits", "label": "Fotógrafa/o de cada foto", "widget": "keyvalue", "required": False,
      "hint": "Izquierda: nombre de la foto sin .jpg (p. ej. circografia-1). Derecha: quién la hizo."}]},
 ],
 "collections": [
   {"name": "texts", "label": "Textos (8 idiomas)", "icon": "translate", "i18n": True,
    "description": "Todos los textos de la web. Cambia un idioma y guarda: los demás se traducen solos en unos minutos (traductor libre de Softcatalà). Revisa siempre la traducción.",
    "files": [{"name": "all", "label": "Todos los textos", "file": "content/i18n/{{locale}}.json", "i18n": True, "fields": texts}]},
   {"name": "shows", "label": "Espectáculos", "icon": "theater_comedy",
    "files": [{"name": "list", "label": "Espectáculos", "file": "content/shows.json", "fields": [
      note("_about", J("content/shows.json")["_about"]),
      {"name": "shows", "label": "Espectáculos", "widget": "list", "collapsed": True, "summary": "{{fields.title}}", "label_singular": "espectáculo",
       "hint": "En orden (el primero sale primero). Los textos de cada uno (descripción, estado…) están en Textos → Espectáculos.", "fields": [
        {"name": "id", "label": "Código (no tocar)", "widget": "string", "hint": "Une este espectáculo con sus textos en cada idioma."},
        {"name": "title", "label": "Título", "widget": "string"},
        {"name": "video", "label": "Vídeo (enlace PeerTube o YouTube)", "widget": "string",
         "hint": "Pega el enlace normal del vídeo: PeerTube (https://…/w/…) o YouTube. PeerTube mejor (sin Google)."},
        img("video_cover", "Foto de portada del vídeo"),
        {"name": "download", "label": "Dossier (botón)", "widget": "select", "required": False, "dropdown_threshold": 12,
         "options": download_keys, "hint": "Qué PDF da el botón «Dossier» de este espectáculo."},
        {"name": "credits", "label": "Ficha artística", "widget": "list", "collapsed": True, "summary": "{{fields.name}}", "label_singular": "crédito", "fields": [
          {"name": "role", "label": "Rol", "widget": "select", "options": roles, "dropdown_threshold": 12, "hint": "Los nombres de los roles están en Textos → Ficha artística."},
          {"name": "name", "label": "Nombre", "widget": "string"},
          {"name": "url", "label": "Enlace (opcional)", "widget": "string", "required": False}]},
        {"name": "support", "label": "Con el apoyo de", "widget": "list", "hint": "Un nombre por línea."},
        {"name": "images", "label": "Galería", "widget": "list", "collapsed": True, "thumbnail": "file", "summary": "{{fields.file}}",
         "label_singular": "foto", "hint": "En orden: forman el mosaico. Las fotos nunca se recortan.", "fields": [img("file", "Foto"), shape]}]}]}]},
 ],
}
# phones: short selects as radio buttons (a searchable dropdown opens and closes the keyboard)
def radios(x):
    if isinstance(x, dict):
        if x.get("widget") == "select": x.setdefault("dropdown_threshold", 12)
        for v in x.values(): radios(v)
    elif isinstance(x, list):
        for v in x: radios(v)
radios(cfg)

class D(yaml.SafeDumper): pass
D.add_representer(str, lambda d, s: d.represent_scalar("tag:yaml.org,2002:str", s, style='"' if s in ("on", "off", "yes", "no") else None))
head = "# Sveltia CMS config for victoriasickness-web — generated by scripts/make_config.py — edit that script, not this file.\n# Docs: https://sveltiacms.app/en/docs\n"
open(out, "w").write(head + yaml.dump(cfg, Dumper=D, sort_keys=False, allow_unicode=True, width=200))
print("ok", len(texts), "text groups,", len(LOCALES), "languages")
