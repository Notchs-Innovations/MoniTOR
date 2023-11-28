import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtWebEngineWidgets import *

from MoniTOR.Browser import AdBlockWebEngineView
from MoniTOR.Browser import AdBlockProfile
from MoniTOR.Browser import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_UseSoftwareOpenGL)

    #customProfile = AdBlockProfile()
    #web_view = AdBlockWebEngineView()

    #webview = QWebEngineView()
    #profile = AdBlockProfile()
    #webpage = QWebEnginePage(profile, webview)
    #web_view.setPage(webpage)

    app.setOrganizationName("Notch's Innovations")
    app.setOrganizationDomain("https://notchxvi.github.io/")
    app.setApplicationName("MoniTOR - Lightweight Private Browser")
    app.setApplicationDisplayName("MoniTOR")
    app.setApplicationVersion(open("version.txt", "r").read())

    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())