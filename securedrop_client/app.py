import sys
import os

from pkg_resources import resource_filename, resource_string

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QListWidgetItem, QListWidget, \
    QMainWindow, QScrollArea, QSizePolicy, QVBoxLayout, QWidget
from PyQt5.QtGui import QFontDatabase


def load_css(name):
    return resource_string('resources', 'css/' + name).decode('utf-8')


def load_font(font_folder_name):
    directory = resource_filename('resources', 'fonts/') + font_folder_name
    for filename in os.listdir(directory):
        if filename.endswith(".ttf"):
            QFontDatabase.addApplicationFont(directory + '/' + filename)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        main_view = MainView()
        self.setCentralWidget(main_view)
        self.show()


class MainView(QWidget):
    def __init__(self):
        super().__init__()

        # Set id and styles
        self.setObjectName('MainView')

        # Set layout
        layout = QHBoxLayout(self)
        self.setLayout(layout)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create SourceList widget
        self.source_list = SourceList()
        self.source_list.itemSelectionChanged.connect(self.on_source_changed)

        # Create widgets
        self.view_holder = QWidget()
        self.view_holder.setObjectName('MainView_view_holder')
        self.view_layout = QVBoxLayout()
        self.view_holder.setLayout(self.view_layout)

        # Add widgets to layout
        layout.addWidget(self.source_list)
        layout.addWidget(self.view_holder)

    def on_source_changed(self):
        self.view_layout.takeAt(0)
        self.view_layout.addWidget(SourceConversationWrapper())


class SourceList(QListWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName('SourceList')
        self.setUniformItemSizes(True)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        item1 = QListWidgetItem(self)
        item2 = QListWidgetItem(self)
        self.setItemWidget(item1, QLabel('item 1'))
        self.setItemWidget(item2, QLabel('item 2'))
        self.insertItem(0, item1)
        self.insertItem(1, item2)


class ConversationScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()

        # Set layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.setObjectName('ConversationScrollArea')

        # Create the scroll area's widget
        conversation = QWidget()
        conversation.setObjectName('ConversationScrollArea_conversation')
        conversation.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        conversation_layout = QVBoxLayout()
        conversation.setLayout(conversation_layout)

        # `conversation` is a child of this scroll area
        self.setWidget(conversation)

        conversation_layout.addWidget(QLabel('message 1'), alignment=Qt.AlignLeft)
        conversation_layout.addWidget(QLabel('message 2'), alignment=Qt.AlignRight)


class SourceConversationWrapper(QWidget):
    def __init__(self):
        super().__init__()

        # Set layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create widgets
        self.conversation_title_bar = QLabel('Conversation X')
        self.scroll = ConversationScrollArea()

        # Add widgets
        layout.addWidget(self.conversation_title_bar)
        layout.addWidget(self.scroll)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName('SecureDrop Client')
    app.setDesktopFileName('org.freedomofthepress.securedrop.client')
    app.setApplicationVersion('dev')
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setStyleSheet(load_css('sdclient.css'))

    load_font('Montserrat')
    load_font('Source_Sans_Pro')

    gui = Window()

    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    sys.exit(app.exec_())
