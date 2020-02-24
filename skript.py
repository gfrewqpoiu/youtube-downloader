import youtube_dl
from loguru import logger
from typing import List, Optional, Dict, Any
from pathlib import Path


class MyLogger(object):
    """Dies leitet die Ausgabe von Youtube-dl zu loguru um."""
    def debug(self, msg: str) -> None:
        logger.debug(msg)

    def warning(self, msg: str) -> None:
        logger.warning(msg)

    def info(self, msg: str) -> None:
        logger.info(msg)

    def error(self, msg: str) -> None:
        """

        :param msg: The message to log.
        """
        logger.error(msg)


ydl_opts: Dict[str, Any] = {'format': 'best[ext=mp4][height<=720]'}
# Das bedeutet, lade das beste mp4 Video runter, was maximal 720p ist.


def path_cleanup(path: str) -> str:
    if not path.endswith("/") or path.endswith("\\"):
            path = Path(path).as_posix() # Macht den Pfad immer zu einem POSIX Pfad. Also mit / für Ebenen.
            path_with_slash = str(path) + "/"  # Fügt den fehlenden Slash hinzu.
            path = path_with_slash
    return path  


def main(links: Optional[List[str]] = None, path: str = "", ydl_options: Optional[Dict[str, Any]] = None):
    if ydl_options is None:
        ydl_options = ydl_opts
    ydl_options.update({'logger': MyLogger()})
    if not links:
        print("What link do you want to download?")
        links = [input("Please enter it here: ")]  # Dies liest den Link von der Konsole ein.
    logger.debug(f"The Links you provided are: {links}")
    if not path:
        print("Okay. Where should I place the file?")
        path = input("Please enter the Path here: ")  # Dies liest den Pfad von der Konsole ein.
        path = path_cleanup(path)
    logger.debug(f"The path you provided is: {path}")
    ydl_options.update({'outtmpl': f'{path}%(title)s.%(ext)s'})
    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        ydl.download(links)


if __name__ == '__main__':
    # Diese Abfrage überprüft, ob das Skript direkt gestartet wurde (dann wird die main Methode ausgeführt).
    # Oder ob das Skript nur importiert wurde, dann wird main nicht ausgeführt.
    # Dies erlaubt in manchen IDE's auch das direkte Starten des Skripts weil ein Start Knopf hier erscheint.
    main()
