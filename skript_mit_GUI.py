from skript import main, path_cleanup
from pathlib import Path
import PySimpleGUI as Sg
from typing import List


def get_links_window() -> List[str]:
    layout = [[Sg.Text("Please enter the URL(s) you want to download. One per line.")],
              [Sg.Multiline(tooltip="Enter one URL per line.", key="INPUT", size=(100, 12))],
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
        path = path_cleanup(path)

        return path


def video_or_audio() -> str:
    layout = [[Sg.Button("Download Videos", key="VIDEO")],
              [Sg.Button("Download Audios", key="AUDIO")],
              [Sg.Cancel()]]
    window = Sg.Window("Youtube-dl Downloader", layout=layout)
    event, values = window.Read()
    window.Close()
    if event == "Cancel":
        exit(0)
    else:
        return event


def main_mit_gui():
    file_type: str = video_or_audio()
    links: List[str] = get_links_window()
    path: str = get_folder_input_window()
    if file_type == "VIDEO":
        main(links, path)
    elif file_type == "AUDIO":
        options = {'format': 'bestaudio[ext=m4a]/bestaudio/best'}
        main(links, path, ydl_options=options)
    else:
        raise NotImplementedError("Unsupported file type.")


if __name__ == "__main__":
    from loguru import logger
    logger.remove()
    logger.add(lambda msg: Sg.EasyPrint(msg), level='DEBUG', colorize=False, backtrace=True, diagnose=True)
    main_mit_gui()
