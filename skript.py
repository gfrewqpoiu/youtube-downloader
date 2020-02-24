import youtube_dl
from loguru import logger
from typing import List, Optional
from pathlib import Path


class MyLogger(object):
    """Dies leitet die Ausgabe von Youtube-dl zu loguru um."""
    def debug(self, msg):
        logger.debug(msg)

    def warning(self, msg):
        logger.warning(msg)

    def error(self, msg):
        logger.error(msg)

    def info(self, msg):
        logger.info(msg)


ydl_opts = {'format': 'best[ext=mp4][height<=720]',
            # Das bedeutet, lade das beste mp4 Video runter, was maximal 720p ist.
            'logger': MyLogger()}


def path_cleanup(path: str) -> str:
    if not path.endswith("/") or path.endswith("\\"):
            path = Path(path).as_posix() # Macht den Pfad immer zu einem POSIX Pfad. Also mit / für Ebenen.
            path_with_slash = str(path) + "/"  # Fügt den fehlenden Slash hinzu.
            path = path_with_slash
    return path  

def main(link: Optional[List[str]] = None, path: str = ""):
    if not link:
        print("What link do you want to download?")
        link = [input("Please enter it here: ")]  # Dies liest den Link von der Konsole ein.
    print(f"The Link you provided is: {link}")
    if not path:
        print("Okay. Where should I place the file?")
        path = input(
            "Please enter the Path here: ")
        path = path_cleanup(path)  # Dies liest den Pfad von der Konsole ein.
    print(f"The path you provided is: {path}")
    ydl_opts.update({'outtmpl': f'{path}%(title)s.%(ext)s'})
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(link)


if __name__ == '__main__':
    # Diese Abfrage überprüft, ob das Skript direkt gestartet wurde (dann wird die main Methode ausgeführt).
    # Oder ob das Skript nur importiert wurde, dann wird main nicht ausgeführt.
    # Dies erlaubt in manchen IDE's auch das direkte Starten des Skripts weil ein Start Knopf hier erscheint.
    main()
