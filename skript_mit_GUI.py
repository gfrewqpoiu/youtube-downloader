from skript import *
from pathlib import Path
import PySimpleGUI as Sg
from typing import List


def get_links_window() -> List[str]:
    layout = [[Sg.Text("Please enter the URL(s) you want to download. One per line.")],
              [Sg.Multiline(tooltip="Enter one URL per line.", key="INPUT", size=(40, 12))],
              [Sg.Cancel(), Sg.Ok()]]
    window = Sg.Window("Youtube-dl Downloader", layout)
    event, values = window.Read()
    if event == "Cancel":
        exit(0)
    if event == "Ok":
        raw_input: str = values["INPUT"]
        links = raw_input.split("\n")
        if '' in links:
            links.remove('')
        window.Close()
        return links


def get_folder_input_window(title_text: str = "Youtube-dl Downloader", initial_folder: str = str(Path.home())) -> str:
    layout = [[Sg.Text("Select a folder for the download(s):")],
              [Sg.Input(key="PATH"), Sg.FolderBrowse("Select Folder", initial_folder=str(initial_folder))],
              [Sg.OK(), Sg.Cancel()]]
    window = Sg.Window(title_text, layout)
    event, values = window.Read()
    window.Close()
    if event == "Cancel":
        exit(0)
    elif event.upper() == "OK":
        path: str = values["PATH"]
        if not path.endswith("/") or path.endswith("\\"):
            path = Path(path).as_posix() # Macht den Pfad immer zu einem POSIX Pfad. Also mit / für Ebenen.
            path_with_slash = str(path) + "/"  # Fügt den fehlenden Slash hinzu.
            path = path_with_slash  # TODO: Test on Windows whether youtube-dl accepts POSIX Path.

        return path


def main_mit_gui():
    links: List[str] = get_links_window()
    path: str = get_folder_input_window()
    main(links, path)
