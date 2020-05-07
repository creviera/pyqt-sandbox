import os

from PyQt5.QtGui import QFontDatabase


def load_font(font_folder_name):
    directory = 'resources/fonts/' + font_folder_name
    for filename in os.listdir(directory):
        if filename.endswith(".ttf"):
            QFontDatabase.addApplicationFont(directory + '/' + filename)
