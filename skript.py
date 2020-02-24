import youtube_dl
from loguru import logger


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

if __name__ == '__main__':
    print("What link do you want to download?")
    link = input("Please enter it here: ")  # Dies liest den Link von der Konsole ein.
    print(f"The Link you provided is: {link}")
    print("Okay. Where should I place the file?")
    path = input("Please enter the Path here (and add a / or \\ at the end if there is none): ")  # Dies liest den Pfad von der Konsole ein.
    print(f"The path you provided is: {path}")
    ydl_opts.update({'outtmpl': f'{path}%(title)s.%(ext)s'})
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
