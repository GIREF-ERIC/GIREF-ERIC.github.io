import mkdocs.plugins
from pathlib import Path
import re

GLOSSAIRE = {}
TERMES_SANS_TRADUCTION = set()

@mkdocs.plugins.event_priority(-50)
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

@mkdocs.plugins.event_priority(-50)
def on_post_build(config):
    # Génère le fichier glossaire.md
    glossaire_md = Path("docs/glossaire.md")
    glossaire_md.write_text("mon glossaire de termes traduits", encoding="utf-8")
    glossaire_md.write_text("\n\n".join(GLOSSAIRE.values()), encoding="utf-8")

    # Génère un fichier des termes à ne pas traduire
    termes_sans_traduction_md = Path("docs/termes_sans_traduction.txt")
    termes_sans_traduction_md.write_text("mon glossaire de termes NON-traduits", encoding="utf-8")
    termes_sans_traduction_md.write_text("\n".join(TERMES_SANS_TRADUCTION), encoding="utf-8")

