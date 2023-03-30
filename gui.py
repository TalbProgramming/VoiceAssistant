import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("GPT Voice Assistant")
        self.resize(1000, 500)
        self.move(400, 200)
        self.setWindowIcon(QIcon('image.jpg'))

        # Palettes
        main_palette = QPalette()
        main_palette.setColor(QPalette.Background, QColor(65, 69, 68))

        sidebar_palette = QPalette()
        sidebar_palette.setColor(QPalette.Background, QColor(200, 200, 200))

        # Set MainWindow Background color
        self.setPalette(main_palette)

        # Add gray sidebar
        side_bar_background = QWidget(self)
        side_bar_background.setGeometry(800, 0, 200, 500)
        side_bar_background.setAutoFillBackground(True)
        side_bar_background.setPalette(sidebar_palette)

        labelFont = QFont("Ariel", 12, QFont.Bold)
        name_label = QLabel("Name: Greg", self)
        name_label.setFont(labelFont)
        name_label.move(850, 150)

        resetbtn = QPushButton("RESET", self)
        resetbtn.clicked.connect(self.reset_bot)
        resetbtn.resize(100, 50)
        resetbtn.move(850, 20)

        namebtn = QPushButton("Change Name", self)
        namebtn.clicked.connect(self.change_name)
        namebtn.resize(100, 50)
        namebtn.move(850, 200)

        historybtn = QPushButton("History", self)
        historybtn.clicked.connect(self.download_history)
        historybtn.resize(100, 50)
        historybtn.move(850, 400)

    def reset_bot(self):
        print("<RESET> has been clicked... ")
        # reset button function

    def download_history(self):
        print("<History> has been clicked... ")
        # history button function

    def change_name(self):
        print("<ChangeName> has been clicked... ")
        # change name function


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
