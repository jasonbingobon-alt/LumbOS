#!/usr/bin/env python3
"""
LumbOS i terminalen
Sprog: dansk, engelsk, français, deutsch, español
Kommandoer: file, browser, world, youtube, photo, help/hjælp, exit/quit
"""

import os
import time
import json
import shutil
import subprocess
import webbrowser
from pathlib import Path

# ---------- Indstillinger ----------
DOUBLE_CLICK_INTERVAL = 1.5  # sekunder til at registrere "dobbeltklik"
USER_STORE = Path.home() / ".Lumb_os_user.json"
# Mulige Edge-stier (Windows). Vi forsøger disse før fallback.
EDGE_PATHS_WINDOWS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]

# ---------- Tekster / oversættelser ----------
TEXT = {
    "da": {
        "welcome": "Velkommen til Lumb!",
        "choose_lang": "Vælg sprog / Choose language:\n1) Dansk\n2) English\n3) Français\n4) Deutsch\n5) Español\nSkriv nummeret for sprogvalg:",
        "ask_username": "Skriv dit brugernavn:",
        "prompt": "skriv en kommando (skriv 'hjælp' for at se kommandoer): ",
        "help": "Kommandoer:\n - file : Vis filer i nuværende mappe (skriv nummer for at markere, dobbeltklik for at åbne)\n - browser : Åbn Microsoft Edge\n - youtube : Åbn YouTube i Edge\n - photo : Åbn pixlr.com i Edge\n - world : Skift sprog\n - hjælp eller help : Vis denne hjælp\n - exit eller quit : Afslut programmet",
        "no_files": "Ingen filer i denne mappe.",
        "files_header": "Filer i mappe '{}':",
        "selected": "Valgt: {} (tryk samme nummer igen for at åbne)",
        "opened": "Forsøger at åbne fil: {}",
        "edge_open": "Forsøger at åbne Microsoft Edge...",
        "edge_failed": "Kunne ikke finde Edge — åbner i standardbrowser.",
        "lang_changed": "Sprog ændret.",
        "goodbye": "Farvel!",
        "unknown": "Ukendt kommando.",
        "enter_to_continue": "tryk Enter for at fortsætte..."
    },
    "en": {
        "welcome": "Welcome to Lumb!",
        "choose_lang": "Choose language:\n1) Dansk\n2) English\n3) Français\n4) Deutsch\n5) Español\nType the number:",
        "ask_username": "Enter your username:",
        "prompt": "type a command (type 'help' to list commands): ",
        "help": "Commands:\n - file : List files in current folder (type number to select, double-click to open)\n - browser : Open Microsoft Edge\n - youtube : Open YouTube in Edge\n - photo : Open pixlr.com in Edge\n - world : Change language\n - help or hjælp : Show this help\n - exit or quit : Quit",
        "no_files": "No files in this folder.",
        "files_header": "Files in folder '{}':",
        "selected": "Selected: {} (type same number again to open)",
        "opened": "Attempting to open file: {}",
        "edge_open": "Attempting to open Microsoft Edge...",
        "edge_failed": "Edge not found — opening in default browser.",
        "lang_changed": "Language changed.",
        "goodbye": "Goodbye!",
        "unknown": "Unknown command.",
        "enter_to_continue": "press Enter to continue..."
    },
    "fr": {
        "welcome": "Bienvenue dans Lumb!",
        "choose_lang": "Choisissez la langue:\n1) Dansk\n2) English\n3) Français\n4) Deutsch\n5) Español\nTapez le numéro:",
        "ask_username": "Entrez votre nom d'utilisateur:",
        "prompt": "tapez une commande (tapez 'help' pour la liste des commandes): ",
        "help": "Commandes:\n - file : Lister les fichiers (tapez le numéro pour sélectionner, double-cliquez pour ouvrir)\n - browser : Ouvrir Microsoft Edge\n - youtube : Ouvrir YouTube dans Edge\n - photo : Ouvrir pixlr.com dans Edge\n - world : Changer la langue\n - help ou hjælp : Afficher cette aide\n - exit ou quit : Quitter",
        "no_files": "Aucun fichier dans ce dossier.",
        "files_header": "Fichiers dans le dossier '{}':",
        "selected": "Sélectionné: {} (tapez le même numéro à nouveau pour ouvrir)",
        "opened": "Tentative d'ouverture du fichier: {}",
        "edge_open": "Tentative d'ouverture de Microsoft Edge...",
        "edge_failed": "Edge introuvable — ouverture dans le navigateur par défaut.",
        "lang_changed": "Langue changée.",
        "goodbye": "Au revoir!",
        "unknown": "Commande inconnue.",
        "enter_to_continue": "appuyez sur Entrée pour continuer..."
    },
    "de": {
        "welcome": "Willkommen bei lumb!",
        "choose_lang": "Sprache wählen:\n1) Dansk\n2) English\n3) Français\n4) Deutsch\n5) Español\nGeben Sie die Nummer ein:",
        "ask_username": "Geben Sie Ihren Benutzernamen ein:",
        "prompt": "Geben Sie einen Befehl ein (schreiben Sie 'help' für Befehle): ",
        "help": "Befehle:\n - file : Zeigt Dateien im aktuellen Ordner an (Nummer zum Markieren, Doppel-Klick um zu öffnen)\n - browser : Öffnet Microsoft Edge\n - youtube : Öffnet YouTube in Edge\n - photo : Öffnet pixlr.com in Edge\n - world : Sprache wechseln\n - help oder hjælp : Zeigt diese Hilfe\n - exit oder quit : Beenden",
        "no_files": "Keine Dateien in diesem Ordner.",
        "files_header": "Dateien im Ordner '{}':",
        "selected": "Ausgewählt: {} (geben Sie dieselbe Nummer erneut ein um zu öffnen)",
        "opened": "Versuche, Datei zu öffnen: {}",
        "edge_open": "Versuche, Microsoft Edge zu öffnen...",
        "edge_failed": "Edge nicht gefunden — öffne Standardbrowser.",
        "lang_changed": "Sprache geändert.",
        "goodbye": "Auf Wiedersehen!",
        "unknown": "Unbekannter Befehl.",
        "enter_to_continue": "Drücken Sie die Eingabetaste..."
    },
    "es": {
        "welcome": "¡Bienvenido a lumb!",
        "choose_lang": "Elige idioma:\n1) Dansk\n2) English\n3) Français\n4) Deutsch\n5) Español\nEscribe el número:",
        "ask_username": "Escribe tu nombre de usuario:",
        "prompt": "escribe un comando (escribe 'help' para ver comandos): ",
        "help": "Comandos:\n - file : Lista archivos en la carpeta actual (escribe número para seleccionar, doble clic para abrir)\n - browser : Abre Microsoft Edge\n - youtube : Abre YouTube en Edge\n - photo : Abre pixlr.com en Edge\n - world : Cambiar idioma\n - help o hjælp : Muestra esta ayuda\n - exit o quit : Salir",
        "no_files": "No hay archivos en esta carpeta.",
        "files_header": "Archivos en la carpeta '{}':",
        "selected": "Seleccionado: {} (escribe el mismo número otra vez para abrir)",
        "opened": "Intentando abrir archivo: {}",
        "edge_open": "Intentando abrir Microsoft Edge...",
        "edge_failed": "No se encontró Edge — abriendo en el navegador predeterminado.",
        "lang_changed": "Idioma cambiado.",
        "goodbye": "¡Adiós!",
        "unknown": "Comando desconocido.",
        "enter_to_continue": "pulsa Enter para continuar..."
    }
}

# Map nummer -> sprog kode
LANG_CODES = { "1": "da", "2": "en", "3": "fr", "4": "de", "5": "es" }

# ---------- Hjælpefunktioner ----------
def load_user():
    if USER_STORE.exists():
        try:
            return json.loads(USER_STORE.read_text())
        except Exception:
            return {}
    return {}

def save_user(data):
    try:
        USER_STORE.write_text(json.dumps(data))
    except Exception:
        pass

def open_with_default(path):
    # cross-platform åbning af fil/URL
    try:
        if os.name == "nt":
            os.startfile(path)
        elif sys_platform_is_mac():
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        return True
    except Exception:
        return False

def sys_platform_is_mac():
    return os.sys.platform == "darwin"

def try_open_edge(url=None):
    """Forsøg at åbne Microsoft Edge; hvis ikke muligt, fallback til standardbrowser."""
    # Prøv Windows-specifikke paths
    if os.name == "nt":
        for p in EDGE_PATHS_WINDOWS:
            if os.path.exists(p):
                try:
                    if url:
                        subprocess.Popen([p, url])
                    else:
                        subprocess.Popen([p])
                    return True
                except Exception:
                    continue
    # ellers prøv at bruge webbrowser med Edge-register hvis muligt
    try:
        # on many systems webbrowser can open "microsoft-edge:" scheme (windows)
        if url and webbrowser.open(url):
            return True
    except Exception:
        pass
    return False

def open_file_smart(file_path):
    """Åbn fil på platformen."""
    file_path = str(file_path)
    if os.name == "nt":
        try:
            os.startfile(file_path)
            return True
        except Exception:
            pass
    # mac / linux fallback
    try:
        if sys_platform_is_mac():
            subprocess.Popen(["open", file_path])
        else:
            subprocess.Popen(["xdg-open", file_path])
        return True
    except Exception:
        return False

# ---------- Main ----------
def main():
    user_data = load_user()
    lang = user_data.get("lang")
    username = user_data.get("username")

    # 1) sprogvalg hvis ikke gemt
    if not lang:
        print(TEXT["en"]["welcome"])  # neutral welcome i starten
        while True:
            print()
            print(TEXT["en"]["choose_lang"])
            choice = input("> ").strip()
            if choice in LANG_CODES:
                lang = LANG_CODES[choice]
                user_data["lang"] = lang
                save_user(user_data)
                break
            else:
                print("Ugyldigt valg. Prøv igen.")

    T = TEXT[lang]
    print()
    print(T["welcome"])

    # 2) username hvis ikke gemt
    if not username:
        username = input(T["ask_username"] + " ").strip()
        if username == "":
            username = "user"
        user_data["username"] = username
        save_user(user_data)

    # state til file "dobbeltklik"
    last_selected = None
    last_selected_time = 0

    cwd = Path.cwd()

    while True:
        try:
            cmd = input(f"{username}@Lumb-os> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print(T["goodbye"])
            break

        if cmd == "":
            continue

        # tillad både danske og engelske "help"
        if cmd.lower() in ("help", "hjælp", "hjælp()"):
            print()
            print(T["help"])
            print()
            continue

        # exit
        if cmd.lower() in ("exit", "quit"):
            print(T["goodbye"])
            break

        if cmd.lower() == "world":
            # skift sprog: vis menu igen
            print(TEXT["en"]["choose_lang"] if lang == "en" else TEXT[lang]["choose_lang"])
            choice = input("> ").strip()
            if choice in LANG_CODES:
                lang = LANG_CODES[choice]
                user_data["lang"] = lang
                save_user(user_data)
                T = TEXT[lang]
                print(T["lang_changed"])
            else:
                print(T["unknown"])
            continue

        if cmd.lower() == "file":
            entries = list(cwd.iterdir())
            files = [e for e in entries if e.is_file()]
            if not files:
                print(T["no_files"])
                continue
            print(T["files_header"].format(cwd))
            for i, f in enumerate(files, start=1):
                size = f.stat().st_size
                mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(f.stat().st_mtime))
                print(f"{i}) {f.name}  ({size} bytes, {mtime})")
            # interaktiv selection-løkke
            while True:
                sel = input("(skriv nummer for at markere, 'back' for tilbage) > ").strip()
                if sel.lower() in ("back", "tilbage"):
                    break
                if not sel.isdigit():
                    print("Skriv et nummer eller 'back'.")
                    continue
                idx = int(sel) - 1
                if idx < 0 or idx >= len(files):
                    print("Ugyldigt nummer.")
                    continue
                chosen = files[idx]
                now = time.time()
                if last_selected == idx and (now - last_selected_time) <= DOUBLE_CLICK_INTERVAL:
                    # double click: åbn fil
                    print(T["opened"].format(chosen.name))
                    opened = open_file_smart(chosen)
                    if not opened:
                        print(T["edge_failed"])
                    # reset dobbeltklik
                    last_selected = None
                    last_selected_time = 0
                else:
                    print(T["selected"].format(chosen.name))
                    last_selected = idx
                    last_selected_time = now
                # loop videre — brug kan dobbeltklikke
            continue

        if cmd.lower() == "browser":
            print(T["edge_open"])
            success = try_open_edge()
            if not success:
                print(T["edge_failed"])
                webbrowser.open("about:blank")
            continue

        if cmd.lower() == "youtube":
            print(T["edge_open"])
            url = "https://www.youtube.com"
            success = try_open_edge(url)
            if not success:
                print(T["edge_failed"])
                webbrowser.open(url)
            continue

        if cmd.lower() == "photo":
            print(T["edge_open"])
            url = "https://pixlr.com"
            success = try_open_edge(url)
            if not success:
                print(T["edge_failed"])
                webbrowser.open(url)
            continue

        # hvis brugeren skriver direkte et nummer i hovedprompt, tillad at liste åbner igen
        if cmd.isdigit():
            print("Skriv 'file' for at liste filer, eller brug kommandoerne.")
            continue

        # ukendt kommando
        print(T["unknown"])

if __name__ == "__main__":
    main()
