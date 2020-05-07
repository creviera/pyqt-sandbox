import sys
import os

from pkg_resources import resource_filename

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QListWidgetItem, QListWidget, \
    QMainWindow, QScrollArea, QSizePolicy, QVBoxLayout, QWidget
from PyQt5.QtGui import QFontDatabase


def load_font(font_folder_name):
    directory = resource_filename('resources', 'fonts/') + font_folder_name
    for filename in os.listdir(directory):
        if filename.endswith(".ttf"):
            QFontDatabase.addApplicationFont(directory + '/' + filename)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Crahser')
        main_view = MainView()
        self.setCentralWidget(main_view)
        self.show()


class MainView(QWidget):
    def __init__(self):
        super().__init__()

        # Set id and styles
        self.setObjectName('MainView')

        # Set layout
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)

        # Set margins and spacing
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Create SourceList widget
        self.source_list = SourceList()

        # Create widgets
        self.view_holder = QWidget()
        self.view_holder.setObjectName('MainView_view_holder')
        self.view_layout = QVBoxLayout()
        self.view_holder.setLayout(self.view_layout)
        self.view_layout.setContentsMargins(0, 0, 0, 0)
        self.view_layout.setSpacing(0)

        # Add widgets to layout
        self.layout.addWidget(self.source_list)
        self.layout.addWidget(self.view_holder)


class SourceListItem(QListWidgetItem):
    def __init__(self):
        super().__init__()
        self.conversation = SourceConversationWrapper()
        self.setText('item')


class SourceList(QListWidget):
    def __init__(self):
        super().__init__()

        self.itemSelectionChanged.connect(self.on_source_changed)

        self.setObjectName('SourceList')
        self.setFixedWidth(200)
        self.setUniformItemSizes(True)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        item0 = SourceListItem()
        item1 = SourceListItem()
        self.insertItem(0, item0)
        self.insertItem(1, item1)

    def on_source_changed(self):
        selected_item = self.selectedItems()[0]
        selected_conversation = selected_item.conversation
        selected_conversation.show()


class ConversationScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()

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


class SourceConversationWrapper(QWidget):
    def __init__(self):
        super().__init__()

        # Set layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create widgets
        self.conversation_title_bar = QLabel('Conversation X')
        self.conversation_view = ConversationScrollArea()

        # Add widgets
        layout.addWidget(self.conversation_title_bar)
        layout.addWidget(self.conversation_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName('SecureDrop Client')
    app.setDesktopFileName('org.freedomofthepress.securedrop.client')
    app.setApplicationVersion('dev')
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    load_font('Montserrat')
    load_font('Source_Sans_Pro')

    gui = Window()

    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    sys.exit(app.exec_())
