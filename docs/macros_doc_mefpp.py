import mkdocs.plugins
from pathlib import Path
import re

GLOSSAIRE = {}
TERMES_SANS_TRADUCTION = set()

# Créer le fichier vide (glossaire.md) avant le build
#@mkdocs.plugins.event_priority(-50)
def on_config(config):
    # Créer le fichier vide glossaire.md
    glossaire_md = Path("docs/glossaire.md")
    glossaire_md.write_text("", encoding="utf-8")

    # Créer le fichier vide termes_sans_traduction.txt
    termes_sans_traduction_md = Path("docs/termes_sans_traduction.md")
    termes_sans_traduction_md.write_text("", encoding="utf-8")
    a=1
    files=1
    mon_env_eric(a,config,files)

#@mkdocs.plugins.event_priority(-50)
def on_page_markdown(markdown, page, **kwargs):
    global GLOSSAIRE, TERMES_SANS_TRADUCTION

    # Gestion des termes à inclure dans le glossaire
    correspondances = re.findall(r'{{glossaire:(.*?)}}', markdown)
    for correspondance in correspondances:
        GLOSSAIRE[correspondance] = f"# {correspondance}\nDéfinition en attente."

    # Gestion des termes à NE PAS traduire
    correspondances_sans_traduction = re.findall(r'{{glossaire_sans_traduction:(.*?)}}', markdown)
    for correspondance in correspondances_sans_traduction:
        TERMES_SANS_TRADUCTION.add(correspondance)

    # Remplacement dans le texte
    markdown = re.sub(r'{{glossaire:(.*?)}}', r'[\1](glossaire.md#\1)', markdown)
    markdown = re.sub(r'{{glossaire_sans_traduction:(.*?)}}', r'<span class="no-translate">\1</span>', markdown)

    return markdown

#@mkdocs.plugins.event_priority(-50)
def mon_env_eric(env, config, files):
    # Génère le fichier glossaire.md
    glossaire_md = Path("docs/glossaire.md")
    with glossaire_md.open("a", encoding="utf-8") as f:
      f.write("mon glossaire de termes traduits\n\n")
      f.write("\n\n".join(GLOSSAIRE.values()))

    # Génère un fichier des termes à ne pas traduire
    termes_sans_traduction_md = Path("docs/termes_sans_traduction.md")
    with termes_sans_traduction_md.open("a", encoding="utf-8") as f:
      f.write("mon glossaire de termes NON-traduits\n\n")
      f.write("\n".join(TERMES_SANS_TRADUCTION))

