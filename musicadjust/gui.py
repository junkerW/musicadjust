import os
from pathlib import Path

import PySimpleGUI as sg
from musicadjust import adjust
import glob

import pyperclip


class MusicGUI:

    def __init__(self):
        self.layout = [[sg.Text("Musik Prozessor")],
                       [sg.Input(key="in_file_text"),
                        sg.FolderBrowse('in_browser', key='in_browse', change_submits=True)],
                       [sg.Input(key="out_file_text"),
                        sg.FolderBrowse('out_browser', key='out_browse', change_submits=True)],
                       [sg.Button("Process")]]
        # Create the window
        self.window = sg.Window("Musik Prozessor", self.layout)
        self.supported_types = ['mp3', 'wav']
        self.run()

    def run(self):
        # Create an event loop
        while True:
            event, values = self.window.read()
            # End program if user closes window or
            # presses the OK button
            if event == sg.WIN_CLOSED:
                break
            if event == "Process":
                in_file_path = Path(values['in_file_text'])
                out_file_path = Path(values['out_file_text'])
                if str(in_file_path) != '' and str(out_file_path) != '':
                    print('Processing file: {}'.format(in_file_path))
                    try:
                        self.process(in_folder=in_file_path, out_folder=out_file_path)
                    except Exception as e:
                        self.display_error(str(e))
                    break
                else:
                    print('Need both files')
            if event == 'in_browser':
                values['in_file_text'] = values['in_browse']
            if event == 'out_browser':
                values['out_file_text'] = values['out_browse']
        self.close()

    def close(self):
        self.window.close()

    def process(self, in_folder: Path, out_folder: Path):
        files = glob.glob(str(in_folder) + '/*')
        for in_file in files:
            if self.supported_file(in_file):
                filename = str(Path(in_file).parts[-1])
                audio = adjust.load_sound(in_file)
                audio = adjust.crop_silence(audio)
                audio = adjust.normalize(audio)
                audio = adjust.add_end_silence(audio, 8000)
                audio = adjust.add_start_silence(audio, 4000)
                create_folder(str(out_folder))
                adjust.save_sound(audio, str(out_folder) + '/' + filename)

    def supported_file(self, filename: str):
        ending = filename.split('.')[-1]
        return ending in self.supported_types

    def display_error(self, message: str):
        layout = [[sg.Text(message)],
                  [sg.Button("OK"), sg.Button(button_text='Fehler kopieren')]]

        window = sg.Window("Fehler", layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'OK':
                break
            if event == 'Fehler kopieren':
                pyperclip.copy(message)


def create_folder(folder_name: str):
    try:
        os.mkdir(folder_name)
    except FileExistsError:
        pass
    except Exception as e:
        print('Cannot create folder {}: {}'.format(folder_name, e))


if __name__ == '__main__':
    music_gui = MusicGUI()
